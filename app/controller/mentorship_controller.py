# Packages
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pytz
from fastapi import HTTPException

# Custom Code imports
from app.services.calender_service import CalenderService
from app.services.payment_service import PaymentService
from app.util.email_service import EmailService
from app.core.config import settings
from app.repository.mentorship_repository import MentorshipRepository
from app.models.mentorship_model import Mentorship, PaymentDetails, CalendarEventDetails
from app.schema.mentorship_schema import (
    AvailabilityRequest,
    AvailabilityResponse,
    TimeSlot,
    MentorshipCreateSchema,
    MentorshipResponseSchema
)
from app.schema.payment_schema import PaymentVerificationRequestSchema


class MentorshipController:

    # ---------------------------------------------------------
    # 1️⃣ Compute available slots
    # ---------------------------------------------------------
    @staticmethod
    def get_available_slots(request: AvailabilityRequest) -> AvailabilityResponse:
        tz = pytz.timezone(settings.TIMEZONE)
        meeting_date = request.meeting_date
        meeting_date_str = meeting_date.strftime("%Y-%m-%d")

        now = datetime.now(tz)
        today = now.date()

        earliest_start = None
        if meeting_date == today:
            earliest_start = (now + timedelta(minutes=30)).replace(second=0, microsecond=0)

        busy_slots = CalenderService.fetch_busy_slots(meeting_date_str)

        work_start = tz.localize(datetime.strptime(
            f"{meeting_date_str} {settings.WORK_START_TIME}", "%Y-%m-%d %H:%M"
        ))
        work_end = tz.localize(datetime.strptime(
            f"{meeting_date_str} {settings.WORK_END_TIME}", "%Y-%m-%d %H:%M"
        ))

        effective_start = max(work_start, earliest_start) if earliest_start else work_start
        if effective_start >= work_end:
            return AvailabilityResponse(slots=[])

        duration_td = timedelta(minutes=request.duration_minutes)
        slot_start = effective_start
        available_slots: List[TimeSlot] = []

        while slot_start + duration_td <= work_end:
            slot_end = slot_start + duration_td
            overlap = False

            for busy in busy_slots:
                busy_start = datetime.fromisoformat(busy["start"]).astimezone(tz)
                busy_end = datetime.fromisoformat(busy["end"]).astimezone(tz)
                if slot_start < busy_end and slot_end > busy_start:
                    overlap = True
                    break

            if not overlap:
                available_slots.append(TimeSlot(
                    start=slot_start.strftime("%H:%M"),
                    end=slot_end.strftime("%H:%M")
                ))

            slot_start += duration_td

        return AvailabilityResponse(slots=available_slots)

    # ---------------------------------------------------------
    # 2️⃣ Book mentorship session
    # ---------------------------------------------------------
    @staticmethod
    async def book_mentorship(request: MentorshipCreateSchema) -> MentorshipResponseSchema:
        
        # -------------------------------
        # Payment verification
        # -------------------------------
        if request.payment_method.lower() == "razorpay":
            payment_payload = PaymentVerificationRequestSchema(
                razorpay_order_id=request.razorpay_order_id,
                razorpay_payment_id=request.razorpay_payment_id,
                razorpay_signature=request.razorpay_signature
            )

            payment_result = PaymentService.verify_payment_service(payment_payload)

            if not payment_result.success:
                raise HTTPException(
                    status_code=400,
                    detail=f"Payment verification failed: {payment_result.message}"
                )

            payment_details = PaymentDetails(
                method="razorpay",
                amount=request.price,
                currency="INR",
                verified=True,
                razorpay_order_id=request.razorpay_order_id,
                razorpay_payment_id=request.razorpay_payment_id,
                razorpay_signature=request.razorpay_signature,
                payment_timestamp=datetime.utcnow()
            )
        else:
            payment_details = PaymentDetails(
                method=request.payment_method,
                verified=False
            )

        # -------------------------------
        # Google Calendar booking
        # -------------------------------
        calendar_result = CalenderService.book_meeting(
            date=request.selected_date.strftime("%Y-%m-%d"),
            start_time=request.selected_start_time,
            duration=request.duration_minutes,
            title=f"Mentorship: {request.plan_name}",
            description=request.topic or "No topic specified",
        )

        if calendar_result.get("status") != "success":
            raise HTTPException(
                status_code=500,
                detail="Failed to schedule mentorship session"
            )

        calendar_event = CalendarEventDetails(
            event_id=calendar_result["event_id"],
            calendar_link=calendar_result["calendar_link"],
            meet_link=calendar_result.get("meet_link"),
            start_datetime=calendar_result["start"],
            end_datetime=calendar_result["end"]
        )

        # -------------------------------
        # Save in DB
        # -------------------------------
        mentorship = Mentorship(
            full_name=request.full_name,
            contact=request.contact,
            email=request.email,
            plan_name=request.plan_name,
            price=request.price,
            duration_minutes=request.duration_minutes,
            selected_date=request.selected_date,
            selected_start_time=request.selected_start_time,
            topic=request.topic,
            payment_method=request.payment_method,
            payment=payment_details,
            calendar_event=calendar_event,
            status="scheduled"
        )

        await MentorshipRepository.create_mentorship(mentorship)

        # -------------------------------
        # 📧 USER EMAIL
        # -------------------------------
        EmailService.send_email(
            to_email=request.email,
            subject="Mentorship Session Confirmed",
            template_name="mentorship_requested_user.html",
            full_name=request.full_name,
            plan_name=request.plan_name,
            session_date=request.selected_date.strftime("%d %b %Y"),
            session_time=request.selected_start_time,
            duration_minutes=request.duration_minutes,
            topic=request.topic or "General Discussion",
            platform_name="Rohit Mentorship"
        )

        # -------------------------------
        # 📧 ADMIN EMAIL
        # -------------------------------
        EmailService.send_email(
            to_email=settings.EMAIL_FROM,
            subject="New Mentorship Session Booked",
            template_name="mentorship_requested_admin.html",
            user_name=request.full_name,
            user_email=request.email,
            contact=request.contact,
            plan_name=request.plan_name,
            price=request.price,
            session_date=request.selected_date.strftime("%d %b %Y"),
            session_time=request.selected_start_time,
            duration_minutes=request.duration_minutes,
            topic=request.topic or "General Discussion",
            payment_method=request.payment_method,
            platform_name="Rohit Mentorship"
        )

        # -------------------------------
        # Response
        # -------------------------------
        return MentorshipResponseSchema(
            success=True,
            event_link=calendar_result["calendar_link"],
            status="confirmed"
        )

    
    @staticmethod
    async def get_all_mentorships_controller(
        skip: int,
        limit: int
    ) -> Dict[str, Any]:
        """
        Controller layer:
        - calls repository
        - converts data to admin dashboard response format
        """

        mentorships = await MentorshipRepository.get_all_mentorships(
            skip=skip,
            limit=limit
        )

        return {
            "success": True,
            "limit": limit,
            "skip": skip,
            "count": len(mentorships),
            "data": [
                {
                    "id": str(m.id),
                    "full_name": m.full_name,
                    "email": m.email,
                    "contact": m.contact,
                    "plan_name": m.plan_name,
                    "price": m.price,
                    "duration_minutes": m.duration_minutes,
                    "selected_date": m.selected_date,
                    "selected_start_time": m.selected_start_time,
                    "timezone": m.timezone,
                    "topic": m.topic,
                    "status": m.status,

                    # payment (safe fields only)
                    "payment": {
                        "method": m.payment.method if m.payment else None,
                        "amount": m.payment.amount if m.payment else None,
                        "verified": m.payment.verified if m.payment else None,
                    } if m.payment else None,

                    # calendar
                    "calendar_event": {
                        "meet_link": m.calendar_event.meet_link,
                        "start_datetime": m.calendar_event.start_datetime,
                        "end_datetime": m.calendar_event.end_datetime,
                    } if m.calendar_event else None,

                    "created_at": m.created_at,
                    "updated_at": m.updated_at,
                }
                for m in mentorships
            ]
        }