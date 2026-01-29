from typing import List, Optional
from datetime import date
from beanie import PydanticObjectId
from app.models.mentorship_model import Mentorship, PaymentDetails, CalendarEventDetails


class MentorshipRepository:
    """
    MongoDB repository for Mentorship documents.
    Handles all DB interactions.
    """

    # ---------------------------
    # CREATE / INSERT
    # ---------------------------
    @staticmethod
    async def create_mentorship(mentorship: Mentorship) -> Mentorship:
        """
        Save a new mentorship booking in MongoDB.
        """
        await mentorship.insert()
        return mentorship
    
    
    # ---------------------------
    # GET ALL (ADMIN DASHBOARD)
    # ---------------------------
    @staticmethod
    async def get_all_mentorships(
        skip: int = 0,
        limit: int = 50,
    ) -> List[Mentorship]:
        """
        Fetch all mentorship bookings for admin dashboard
        sorted by creation time (latest first).
        """
        return (
            await Mentorship.find_all()
            .sort("-created_at")
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    # ---------------------------
    # GET BY ID
    # ---------------------------
    @staticmethod
    async def get_mentorship_by_id(mentorship_id: str) -> Optional[Mentorship]:
        """
        Fetch a mentorship by its ObjectId.
        """
        mentorship = await Mentorship.get(PydanticObjectId(mentorship_id))
        return mentorship

    # ---------------------------
    # GET ALL BOOKINGS BY EMAIL
    # ---------------------------
    @staticmethod
    async def get_mentorships_by_email(email: str) -> List[Mentorship]:
        """
        Fetch all mentorships for a given user email.
        """
        return await Mentorship.find(Mentorship.email == email).to_list()

    # ---------------------------
    # UPDATE STATUS / NOTES / PAYMENT / CALENDAR
    # ---------------------------
    @staticmethod
    async def update_status(
        mentorship_id: str, status: str, notes: Optional[str] = None
    ) -> Optional[Mentorship]:
        mentorship = await Mentorship.get(PydanticObjectId(mentorship_id))
        if mentorship:
            mentorship.status = status
            if notes:
                mentorship.notes = notes
            mentorship.updated_at = mentorship.updated_at  # will auto-update if using triggers
            await mentorship.save()
        return mentorship

    @staticmethod
    async def update_payment(
        mentorship_id: str, payment: PaymentDetails
    ) -> Optional[Mentorship]:
        mentorship = await Mentorship.get(PydanticObjectId(mentorship_id))
        if mentorship:
            mentorship.payment = payment
            mentorship.updated_at = mentorship.updated_at
            await mentorship.save()
        return mentorship

    @staticmethod
    async def update_calendar_event(
        mentorship_id: str, event: CalendarEventDetails
    ) -> Optional[Mentorship]:
        mentorship = await Mentorship.get(PydanticObjectId(mentorship_id))
        if mentorship:
            mentorship.calendar_event = event
            mentorship.updated_at = mentorship.updated_at
            await mentorship.save()
        return mentorship

    # ---------------------------
    # DELETE
    # ---------------------------
    @staticmethod
    async def delete_mentorship(mentorship_id: str) -> bool:
        mentorship = await Mentorship.get(PydanticObjectId(mentorship_id))
        if mentorship:
            await mentorship.delete()
            return True
        return False

    # ---------------------------
    # FILTER BOOKINGS BY DATE
    # ---------------------------
    @staticmethod
    async def get_mentorships_by_date(selected_date: date) -> List[Mentorship]:
        return await Mentorship.find(Mentorship.selected_date == selected_date).to_list()
