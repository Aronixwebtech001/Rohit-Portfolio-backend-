from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List

class ConnectCreateRequestSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    purpose: str = Field(..., min_length=3, max_length=100)
    message: str = Field(..., min_length=10, max_length=2000)


class ConnectCreateResponseSchema(BaseModel):
    id: str
    created_at: datetime
    
    

class ConnectFormEntry(BaseModel):
    name: str
    email: EmailStr
    purpose: str
    message: str
    created_at: datetime


class ConnectFetchResponseSchema(BaseModel):
    success: bool = True
    limit: int
    count: int
    skip: int
    data: List[ConnectFormEntry]

