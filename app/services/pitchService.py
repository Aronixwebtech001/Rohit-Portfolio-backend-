from datetime import datetime
from typing import Optional

from app.schema.pitchSchema import PitchCreateSchema
from app.util.email_service import EmailService
from app.core.config import settings
from app.repository.pitchRepository import PitchRepository
from app.models.pitchModel import Pitch


class PitchService:

    @staticmethod
    async def create_pitch_service(
        payload: PitchCreateSchema,
        proposal_file_url: Optional[str] = None,
    ) -> dict:
        """
        Create pitch:
        - Send emails (no attachment, only link)
        - Store pitch in DB with proposal_file_url
        """
        has_file=False
        if proposal_file_url:
            has_file = True
        
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

        # 1️⃣ Send email to USER (confirmation)
        EmailService.send_email(
            to_email=payload.email,
            subject="Pitch Submitted Successfully 🚀",
            template_name="pitch_submitted_user.html",
            name=payload.name,
            timestamp=timestamp,
        )

        # 2️⃣ Send email to ADMIN (with proposal link)
        EmailService.send_email(
            to_email=settings.EMAIL_FROM,
            subject="New Pitch Received 🚀",
            template_name="pitch_submitted_admin.html",
            **payload.model_dump(exclude={"proposal_file_url"}),
            proposal_file_url=proposal_file_url,  # 🔥 LINK ONLY
            timestamp=timestamp,
        )

        # 3️⃣ Save pitch in database
        pitch_data = payload.model_dump()
        pitch_data["proposal_file_url"] = proposal_file_url

        # 3️⃣ 🔥 Convert payload → MODEL-ALIGNED data
        pitch_model = Pitch(
            **payload.model_dump(exclude={"proposal_file_url"}),
            proposal_file_url=proposal_file_url,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Repository should ONLY deal with DB ops
        pitch = await PitchRepository.create_pitch_repository(pitch_model)

        # 4️⃣ Return response
        return {
            "id": str(pitch.id),
            "email": pitch.email,
            "has_file":has_file,
            "created_at": pitch.created_at,
        }
