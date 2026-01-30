"""
database.py
-------------
MongoDB connection setup using Motor + Beanie ODM.

Responsibilities:
- Create async MongoDB client
- Initialize Beanie with document models
- Provide clean startup integration for FastAPI

Used by:
- app/main.py (startup event)
- All Beanie models automatically
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import os

# Import all Beanie models here
# IMPORTANT: Every Document must be imported
from app.models.pitchModel import Pitch
from app.models.connect_model import Connect
from app.models.mentorship_model import Mentorship
from app.core.config import settings


class MongoDatabase:
    """
    MongoDatabase handles MongoDB lifecycle.
    Singleton-like usage recommended.
    """

    client: Optional[AsyncIOMotorClient] = None

    @classmethod
    async def connect(cls):
        """
        Initialize MongoDB connection and Beanie ODM.

        Called ONCE during FastAPI startup.
        """
        mongo_uri = settings.MONGO_URI
        db_name = settings.MONGO_DB_NAME
        # print(f"Connecting to MongoDB at {mongo_uri}, DB: {db_name}")

        if not mongo_uri or not db_name:
            raise ValueError("MongoDB environment variables not set")

        cls.client = AsyncIOMotorClient(mongo_uri)

        await init_beanie(
            database=cls.client[db_name],
            document_models=[
                Pitch,  # register all models here
                Connect,
                Mentorship
            ],
        )

        print("✅ MongoDB connected successfully")

    @classmethod
    async def close(cls):
        """
        Gracefully close MongoDB connection.

        Called during FastAPI shutdown.
        """
        if cls.client:
            cls.client.close()
            print("🛑 MongoDB connection closed")
