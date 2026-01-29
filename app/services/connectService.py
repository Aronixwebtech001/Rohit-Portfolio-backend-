from datetime import datetime

from app.schema.connectSchema import ConnectCreateRequestSchema
from app.util.email_service import EmailService
from app.core.config import settings
from app.repository.connect_repository import ConnectRepository


class ConnectService:

    @staticmethod
    async def connect_create_service(payload: ConnectCreateRequestSchema):
        """
        Handles sending emails and saving Connect submission.
        """

        timestamp = datetime.now()

        # 1️⃣ Email to USER
        EmailService.send_email(
            to_email=payload.email,
            subject="Thanks for connecting with us 🙌",
            template_name="connect_user.html",
            name=payload.name,
            purpose=payload.purpose,
        )

        # 2️⃣ Email to ADMIN
        EmailService.send_email(
            to_email=settings.EMAIL_FROM,
            subject="New Connect Request",
            template_name="connect_admin.html",
            **payload.model_dump(),
        )

        # 3️⃣ Save data to database
        connect = await ConnectRepository.connect_create_repository(payload)

        # 4️⃣ Response
        return {
            "id": str(connect.id),
            "created_at": connect.created_at,
        }
