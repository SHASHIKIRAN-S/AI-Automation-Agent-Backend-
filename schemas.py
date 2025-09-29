from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class ToneEnum(str, Enum):
    formal = "formal"
    friendly = "friendly"
    casual = "casual"
    persuasive = "persuasive"


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="What the user wants to say")
    tone: ToneEnum
    recipient: EmailStr


class GenerateResponse(BaseModel):
    subject: str
    body: str


class DraftResponse(GenerateResponse):
    id: int


class SendRequest(BaseModel):
    subject: str
    body: str
