from fastapi import UploadFile
from typing import Optional

from app.schema.pitchSchema import (
    PitchCreateSchema,
    PitchCreateResponseSchema,
    PitchGetSchema,
    PitchListResponseSchema
)
from app.services.pitchService import PitchService
from app.repository.pitchRepository import PitchRepository


class PitchController:
    """
    Pitch Controller
    Handles HTTP-level request/response transformation
    """

    @staticmethod
    async def create_pitch_controller(
        payload: PitchCreateSchema,
        proposal_file: Optional[UploadFile] = None,
    ) -> PitchCreateResponseSchema:
        """
        Create a new pitch
        """

        file_bytes = None
        file_name = None
        file_size = None

        if proposal_file:
            file_bytes = await proposal_file.read()
            file_name = proposal_file.filename
            file_size = f"{len(file_bytes) / 1024:.2f} KB"

        result = await PitchService.create_pitch_service(
            payload=payload,
            file_bytes=file_bytes,
            file_name=file_name,
            file_size=file_size,
        )

        return PitchCreateResponseSchema(**result)

    @staticmethod
    async def get_all_pitches_controller(
        skip: int = 0,
        limit: int = 10
    ) -> PitchListResponseSchema:

        docs = await PitchRepository.get_all_pitch_repository(skip, limit)

        data = [
            PitchGetSchema(
                id=str(doc.id),
                name=doc.name,
                company_name=doc.company_name,
                sector=doc.sector,
                investment_required=doc.investment_required,
                email=doc.email,
                contact_number=doc.contact_number,
                pitch_summary=doc.pitch_summary,
                proposal_file_url=doc.proposal_file_url,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
            for doc in docs
        ]

        return PitchListResponseSchema(
            success=True,
            limit=limit,
            skip=skip,
            count=len(data),
            data=data
        )