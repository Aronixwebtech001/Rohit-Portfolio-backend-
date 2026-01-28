from datetime import datetime
from typing import Optional

from app.schema.pitchSchema import PitchCreateSchema
from app.util.email_service import EmailService
from app.core.config import settings
from app.repository.pitchRepository import PitchRepository


class PitchService:

    @staticmethod
    async def create_pitch_service(
        payload: PitchCreateSchema,
        file_bytes: Optional[bytes],
        file_name: Optional[str],
        file_size: Optional[str],
    ) -> dict:
        has_file = file_bytes is not None
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

        # 1️⃣ Send email to USER
        EmailService.send_email(
            to_email=payload.email,
            subject="Pitch Submitted Successfully 🚀",
            template_name="pitch_submitted_user.html",
            name=payload.name,
            timestamp=timestamp,
        )

        # 2️⃣ Send email to ADMIN
        EmailService.send_email(
            to_email=settings.EMAIL_FROM,
            subject="New Pitch Received 🚀",
            template_name="pitch_submitted_admin.html",
            **payload.model_dump(),
            has_file=has_file,
            file_name=file_name,
            file_size=file_size,
            timestamp=timestamp,
            attachment_bytes=file_bytes,
            attachment_name=file_name,
        )

        # 3️⃣ Save pitch in database
        pitch = await PitchRepository.create_pitch_repository(payload)

        # 4️⃣ Return response
        return {
            "id": str(pitch.id),
            "email": pitch.email,
            "has_file": has_file,
            "created_at": pitch.created_at,
        }
