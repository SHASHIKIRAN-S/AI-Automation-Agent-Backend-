from fastapi import FastAPI, HTTPException, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from collections import Counter
import logging
import os

from models import Draft
from email_generator import EmailGenerator
from mailer import send_email
from config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Database Setup
# ----------------------------
backend_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(backend_dir, "database.db")
engine = create_engine(f"sqlite:///{database_path}", echo=False)

def ensure_aware(dt):
    """Ensure datetime is timezone-aware in UTC"""
    if dt is None:
        return dt
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

# ----------------------------
# FastAPI App with Lifespan
# ----------------------------
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    masked_key = settings.email_api_key[:10] + "..." if settings.email_api_key else "MISSING"
    logger.info(f"Email API loaded: {masked_key}")
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
email_generator = EmailGenerator()

# ----------------------------
# CORS
# ----------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://insta-mailer-email-automation-inter.vercel.app",
    "https://your-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Pydantic Models
# ----------------------------
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str
    recipient: str
    tone: str = "friendly"
    type: str = "general"

class EmailDraftResponse(BaseModel):
    id: int
    prompt: str
    content: str
    recipient: str
    tone: str
    status: str
    type: str
    created_at: datetime
    sent_at: Optional[datetime] = None
    subject: Optional[str] = None

# ----------------------------
# Routes
# ----------------------------
@app.get("/")
def root():
    return {"message": "InstaMailer Backend is running."}

@app.post("/generate", response_model=EmailDraftResponse)
def generate(request: GenerateRequest):
    """Generate email draft and save to DB"""
    try:
        email_data = email_generator.generate_email_with_subject(request.prompt, request.tone)
        draft = Draft(
            prompt=request.prompt,
            content=email_data["content"],
            recipient=request.recipient,
            tone=request.tone,
            type=request.type,
            subject=email_data.get("subject")
        )
        with Session(engine) as session:
            session.add(draft)
            session.commit()
            session.refresh(draft)
        return draft
    except Exception as e:
        logger.error(f"Error generating email: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating email")

@app.post("/send/{draft_id}")
def send(draft_id: int):
    """Send email using SMTP"""
    try:
        with Session(engine) as session:
            draft = session.get(Draft, draft_id)
            if not draft:
                raise HTTPException(status_code=404, detail="Draft not found")

            subject = draft.subject or draft.content.split("\n")[0][:50] if draft.content else "Email"

            success = send_email(
                to_email=draft.recipient,
                subject=subject,
                content=draft.content
            )

            if success:
                draft.status = "sent"
                draft.sent_at = datetime.now(timezone.utc)
                session.commit()
                return {"status": "sent", "message": "Email sent successfully"}
            else:
                draft.status = "failed"
                session.commit()
                raise HTTPException(status_code=500, detail="Failed to send email")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending email: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/emails", response_model=List[EmailDraftResponse])
def get_emails():
    """Fetch all email drafts"""
    try:
        with Session(engine) as session:
            drafts = session.exec(select(Draft).order_by(Draft.created_at.desc())).all()
            return drafts
    except Exception as e:
        logger.error(f"Error fetching emails: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching emails")

@app.get("/stats")
def get_stats():
    """Get email sending statistics"""
    try:
        with Session(engine) as session:
            drafts = session.exec(select(Draft)).all()

            total_sent = sum(1 for d in drafts if d.status == "sent")
            total_drafts = sum(1 for d in drafts if d.status == "draft")
            total_failed = sum(1 for d in drafts if d.status == "failed")
            total_emails = len(drafts)
            success_rate = (total_sent / total_emails * 100) if total_emails else 0

            week_ago = datetime.now(timezone.utc) - timedelta(days=7)
            recent_activity = sum(1 for d in drafts if ensure_aware(d.created_at) >= week_ago)

            tone_counter = Counter(d.tone for d in drafts)
            popular_tones = dict(tone_counter.most_common())

            monthly_stats = []
            for i in range(6):
                month_start = datetime.now(timezone.utc).replace(day=1) - timedelta(days=30*i)
                month_end = month_start.replace(day=1) + timedelta(days=32)
                month_end = month_end.replace(day=1) - timedelta(days=1)
                month_drafts = [d for d in drafts if month_start <= ensure_aware(d.created_at) <= month_end]
                monthly_stats.append({
                    "month": month_start.strftime("%b"),
                    "sent": sum(1 for d in month_drafts if d.status == "sent"),
                    "drafts": sum(1 for d in month_drafts if d.status == "draft")
                })
            monthly_stats.reverse()

            return {
                "total_sent": total_sent,
                "total_drafts": total_drafts,
                "total_failed": total_failed,
                "success_rate": round(success_rate, 1),
                "recent_activity": recent_activity,
                "popular_tones": popular_tones,
                "monthly_stats": monthly_stats
            }
    except Exception as e:
        logger.error(f"Error calculating stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error calculating stats")

@app.delete("/emails/{draft_id}")
def delete_email(draft_id: int):
    """Delete a draft"""
    try:
        with Session(engine) as session:
            draft = session.get(Draft, draft_id)
            if not draft:
                raise HTTPException(status_code=404, detail="Draft not found")
            session.delete(draft)
            session.commit()
            return {"message": "Email deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting email: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error deleting email")

@app.post("/update_draft/{draft_id}")
def update_draft(draft_id: int, content: str = Body(...)):
    """Update draft content"""
    try:
        with Session(engine) as session:
            draft = session.get(Draft, draft_id)
            if not draft:
                raise HTTPException(status_code=404, detail="Draft not found")
            draft.content = content
            session.commit()
            return {"message": "Draft updated"}
    except Exception as e:
        logger.error(f"Error updating draft: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error updating draft")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
