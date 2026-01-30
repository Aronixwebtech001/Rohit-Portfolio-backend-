import json
import os
from typing import Optional

from cryptography.fernet import Fernet
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.
    Uses ONLY encrypted Google service account stored in app/security/.
    """

    # --------------------------------------------------
    # General
    # --------------------------------------------------
    APP_NAME: str = "Portfolio API"
    ENV: str = "development"

    # --------------------------------------------------
    # File Upload
    # --------------------------------------------------
    MAX_UPLOAD_SIZE_MB: int = 10

    # --------------------------------------------------
    # Timezone & Working Hours
    # --------------------------------------------------
    TIMEZONE: str = "Asia/Kolkata"
    WORK_START_TIME: str = "10:00"
    WORK_END_TIME: str = "23:00"

    # --------------------------------------------------
    # MongoDB
    # --------------------------------------------------
    MONGO_URI: str
    MONGO_DB_NAME: str

    # --------------------------------------------------
    # Email (SMTP)
    # --------------------------------------------------
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_USE_SSL: bool = False

    # --------------------------------------------------
    # Razorpay
    # --------------------------------------------------
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str

    # --------------------------------------------------
    # Google Calendar
    # --------------------------------------------------
    GOOGLE_CALENDAR_ID: str

    # --------------------------------------------------
    # Google Service Account (Encrypted)
    # --------------------------------------------------
    SERVICE_ACCOUNT_FILE: str = "app/security/service_account.enc"
    SERVICE_ACCOUNT_ENCRYPTION_KEY: str  # must be present in env
    
    # --------------------------------------------------
    # Admin auth
    # --------------------------------------------------
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    # --------------------------------------------------
    #  Cloudinary credential
    # --------------------------------------------------
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # --------------------------------------------------
    # Pydantic config
    # --------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --------------------------------------------------
    # Decrypt Service Account
    # --------------------------------------------------
    def get_service_account_dict(self) -> dict:
        """
        Decrypts service_account.enc and returns JSON dict.
        """

        if not os.path.exists(self.SERVICE_ACCOUNT_FILE):
            raise FileNotFoundError(
                f"Encrypted service account not found: {self.SERVICE_ACCOUNT_FILE}"
            )

        key = self.SERVICE_ACCOUNT_ENCRYPTION_KEY.encode()
        fernet = Fernet(key)

        with open(self.SERVICE_ACCOUNT_FILE, "rb") as f:
            encrypted_data = f.read()

        decrypted_json = fernet.decrypt(encrypted_data).decode("utf-8")
        return json.loads(decrypted_json)


# 🔥 Singleton
settings = Settings()
