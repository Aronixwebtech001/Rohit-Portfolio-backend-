from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


class PitchCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    company_name: str = Field(..., min_length=2, max_length=150)
    sector: str = Field(..., min_length=2, max_length=100)
    investment_required: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    contact_number: str = Field(..., min_length=8, max_length=15)
    pitch_summary: str = Field(..., min_length=10, max_length=2000)
    proposal_file_url: Optional[str] = None


class PitchCreateResponseSchema(BaseModel):
    id: str
    created_at: datetime
    has_file: bool


class PitchGetSchema(BaseModel):
    id: str = Field(..., example="65a8f1c9e9b4e71c4f9a1234")

    name: str
    company_name: str
    sector: str
    investment_required: str
    email: EmailStr
    contact_number: str

    pitch_summary: Optional[str]
    proposal_file_url: Optional[str]

    created_at: datetime
    updated_at: datetime

class PitchListResponseSchema(BaseModel):
    success: bool = True
    limit: int          # page size requested
    count: int          # records returned in this response
    skip: int
    data: List[PitchGetSchema]