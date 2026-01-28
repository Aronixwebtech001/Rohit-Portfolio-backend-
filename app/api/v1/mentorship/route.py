from fastapi import APIRouter, Query
from app.schema.mentorship_schema import AvailabilityRequest, MentorshipCreateSchema, AvailabilityResponse
from app.controller.mentorship_controller import MentorshipController

router = APIRouter()

@router.get("/availability", response_model=AvailabilityResponse)
async def availability(request: AvailabilityRequest):
    return MentorshipController.get_available_slots(request)

@router.post("/book")
async def book(request: MentorshipCreateSchema):
    return await MentorshipController.book_mentorship(request)

@router.get("/")
async def get_all_mentorships(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to fetch")
):
    """
    Admin Dashboard:
    - Get all mentorship bookings
    - Sorted by creation (latest first)
    - Paginated
    """
    return await MentorshipController.get_all_mentorships_controller(
        skip=skip,
        limit=limit
    )