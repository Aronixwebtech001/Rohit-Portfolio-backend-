from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List


# ==================================================
# Mentorship Booking (Create)
# ==================================================

class MentorshipCreateSchema(BaseModel):
    # -------------------------------
    # User details
    # -------------------------------
    full_name: str = Field(..., example="Anuj Kumar")
    contact: str = Field(..., example="+919876543210")
    email: EmailStr = Field(..., example="anuj@example.com")

    # -------------------------------
    # Plan details
    # -------------------------------
    plan_name: str = Field(..., example="Premium Mentorship")
    price: float = Field(..., example=1999.0)
    duration_minutes: int = Field(..., example=60)

    # -------------------------------
    # Session details
    # -------------------------------
    selected_date: date = Field(..., example="2026-01-25")
    selected_start_time: str = Field(..., example="14:00")
    topic: Optional[str] = Field(None, example="Career Guidance")

    # -------------------------------
    # Payment details
    # -------------------------------
    payment_method: str = Field(..., example="razorpay")

    razorpay_order_id: str = Field(..., example="order_xyz")
    razorpay_payment_id: str = Field(..., example="pay_xyz")
    razorpay_signature: str = Field(..., example="sig_xyz")


# ==================================================
# Mentorship Booking (User Response)
# ==================================================

class MentorshipResponseSchema(BaseModel):
    success: bool = True
    message: str = "Mentorship booked successfully"
    event_link: Optional[str] = Field(
        None, example="https://meet.google.com/xyz-abc-def"
    )
    status: str = Field(..., example="confirmed")


# ==================================================
# Mentorship GET (Admin / Dashboard)
# ==================================================

class MentorshipPaymentSchema(BaseModel):
    method: str
    amount: float
    currency: str = "INR"
    verified: bool
    razorpay_order_id: Optional[str]
    razorpay_payment_id: Optional[str]
    razorpay_signature: Optional[str]
    payment_timestamp: Optional[datetime]


class MentorshipCalendarSchema(BaseModel):
    event_id: Optional[str]
    calendar_link: Optional[str]
    meet_link: Optional[str]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]


class MentorshipGetSchema(BaseModel):
    id: str = Field(..., example="65a8f1c9e9b4e71c4f9a1234")

    # User info
    full_name: str
    email: EmailStr
    contact: str

    # Plan info
    plan_name: str
    price: float
    duration_minutes: int

    # Session info
    selected_date: date
    selected_start_time: str
    topic: Optional[str]
    timezone: str

    # Payment & Calendar
    payment: Optional[MentorshipPaymentSchema]
    calendar_event: Optional[MentorshipCalendarSchema]

    # Status & Meta
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class MentorshipListResponseSchema(BaseModel):
    success: bool = True
    limit: int
    count: int
    skip: int
    data: List[MentorshipGetSchema]


# ==================================================
# Availability / Slots
# ==================================================

class AvailabilityRequest(BaseModel):
    meeting_date: date = Field(..., example="2026-01-25")
    duration_minutes: int = Field(..., example=60)


class TimeSlot(BaseModel):
    start: str = Field(..., example="14:00")
    end: str = Field(..., example="15:00")


class AvailabilityResponse(BaseModel):
    success: bool = True
    slots: List[TimeSlot]
