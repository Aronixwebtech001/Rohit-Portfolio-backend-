from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.core.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCredentials:
    """
    Centralized Google Service Account credential loader
    Uses encrypted service_account.enc via settings
    (lazy + cached)
    """

    _credentials = None
    _calendar_service = None

    @classmethod
    def get_credentials(cls):
        """
        Load and cache Google service account credentials
        from encrypted service_account.enc
        """
        if cls._credentials is not None:
            return cls._credentials

        service_account_info = settings.get_service_account_dict()

        if not service_account_info:
            raise RuntimeError(
                "Google service account credentials could not be loaded"
            )

        cls._credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES,
        )

        return cls._credentials

    @classmethod
    def get_calendar_service(cls):
        """
        Build and cache Google Calendar service
        """
        if cls._calendar_service is not None:
            return cls._calendar_service

        credentials = cls.get_credentials()

        cls._calendar_service = build(
            "calendar",
            "v3",
            credentials=credentials,
            cache_discovery=False,  # important for prod / serverless
        )

        return cls._calendar_service
