from datetime import datetime, date
from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field

class PaymentDetails(BaseModel):
    method: str
    amount: float
    currency: str = "INR"
    verified: bool = False
    razorpay_order_id: Optional[str]
    razorpay_payment_id: Optional[str]
    razorpay_signature: Optional[str]
    payment_timestamp: Optional[datetime]

class CalendarEventDetails(BaseModel):
    event_id: Optional[str]
    calendar_link: Optional[str]
    meet_link: Optional[str]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    created_at: datetime = Field(default_factory=datetime.now)

class Mentorship(Document):
    # --- User Info ---
    full_name: str
    email: EmailStr  # ✅ Corrected
    contact: str

    # --- Plan Info ---
    plan_name: str
    price: float
    duration_minutes: int

    # --- Session Info ---
    selected_date: date
    selected_start_time: str  # "HH:MM"
    topic: Optional[str] = None
    timezone: str = "Asia/Kolkata"

    # --- Payment Info ---
    payment: Optional[PaymentDetails]

    # --- Calendar/Event Info ---
    calendar_event: Optional[CalendarEventDetails]

    # --- Status & Metadata ---
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None

    class Settings:
        name = "mentorships"

    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "John Doe",
                "email": "john@example.com",
                "contact": "+919876543210",
                "plan_name": "Premium Mentorship",
                "price": 1999.0,
                "duration_minutes": 60,
                "selected_date": "2026-01-25",
                "selected_start_time": "14:00",
                "topic": "Career Guidance",
                "timezone": "Asia/Kolkata",
                "payment": {
                    "method": "Razorpay",
                    "amount": 1999.0,
                    "currency": "INR",
                    "verified": True,
                    "razorpay_order_id": "order_xyz",
                    "razorpay_payment_id": "pay_xyz",
                    "razorpay_signature": "sig_xyz",
                    "payment_timestamp": "2026-01-22T12:30:00+05:30"
                },
                "calendar_event": {
                    "event_id": "abc123",
                    "calendar_link": "https://www.google.com/calendar/event?eid=...",
                    "meet_link": "https://meet.google.com/xyz-abc-def",
                    "start_datetime": "2026-01-25T14:00:00+05:30",
                    "end_datetime": "2026-01-25T15:00:00+05:30"
                },
                "status": "confirmed",
                "notes": "User prefers Zoom if Google Meet fails."
            }
        }
    }
