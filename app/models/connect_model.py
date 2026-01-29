from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime


class Connect(Document):
    name: str
    email: EmailStr
    purpose: str
    message: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "connect" # MongoDB collection name