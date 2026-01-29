from fastapi import UploadFile
from typing import Optional

from app.util.cloudinary_upload import upload_file_to_cloudinary
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

        file_url = None
        if proposal_file:
            upload_result = await upload_file_to_cloudinary(
                file=proposal_file,
                folder="pitch/proposals",
                resource_type="raw",  # pdf/doc/ppt
            )

            # ✅ ONLY public URL
            file_url = upload_result["url"]

        result = await PitchService.create_pitch_service(
            payload=payload,
            proposal_file_url=file_url,
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