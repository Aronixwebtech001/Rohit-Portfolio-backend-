from fastapi import APIRouter, Form, UploadFile, File, Query
from typing import Optional

from app.schema.pitchSchema import (
    PitchCreateSchema,
    PitchCreateResponseSchema,
    PitchListResponseSchema
)
from app.controller.pitchController import PitchController

router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check():
    return {"status": "OK"}


@router.post("/", summary="Create Pitch", response_model=PitchCreateResponseSchema)
async def create_pitch(name: str = Form(...), company_name: str = Form(...), sector: str = Form(...), investment_required: str = Form(...), email: str = Form(...), contact_number: str = Form(...), pitch_summary: str = Form(...), proposal_file: Optional[UploadFile] = File(None)):
    """
    Create a new pitch (multipart/form-data)

    - Text fields via Form
    - Optional file via UploadFile
    """

    payload = PitchCreateSchema(
        name=name,
        company_name=company_name,
        sector=sector,
        investment_required=investment_required,
        email=email,
        contact_number=contact_number,
        pitch_summary=pitch_summary,
    )

    return await PitchController.create_pitch_controller(
        payload=payload,
        proposal_file=proposal_file,
    )


@router.get(
    "/",
    response_model=PitchListResponseSchema,
    summary="Get all startup pitches (paginated)",
    description="Fetch all startup pitches sorted by creation date (latest first)"
)
async def get_all_pitch(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch"),
):
    """
    Returns a paginated list of pitches.

    - **skip**: Offset (default 0)
    - **limit**: Page size (default 10, max 100)
    """
    return await PitchController.get_all_pitches_controller(skip=skip, limit=limit)
