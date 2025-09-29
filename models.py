from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Draft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt: str
    content: str
    recipient: str
    tone: str = Field(default="friendly")
    status: str = Field(default="draft")  # draft, sent, failed
    type: str = Field(default="general")  # general, meeting
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sent_at: Optional[datetime] = Field(default=None)
    subject: Optional[str] = Field(default=None)
