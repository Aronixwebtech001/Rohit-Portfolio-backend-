from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime


class Pitch(Document):
    name: str
    company_name: str
    sector: str
    investment_required: str
    email: EmailStr
    contact_number: str
    pitch_summary: Optional[str] = None
    proposal_file_url: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "pitch"  # MongoDB collection name
