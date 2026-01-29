from app.models.pitchModel import Pitch
from app.schema.pitchSchema import PitchCreateSchema
from typing import List


class PitchRepository:
    """
    Data Access Layer for Pitch collection.
    """

    @staticmethod
    async def create_pitch_repository(data: PitchCreateSchema):
        pitch = Pitch(**data.model_dump())
        return await pitch.insert()

    @staticmethod
    async def get_all_pitch_repository(skip: int, limit: int) -> List[Pitch]:
        return (
            await Pitch.find_all()
            .sort(-Pitch.created_at)   # latest first
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    @staticmethod
    async def get_by_email_repository(email: str) -> Pitch | None:
        return await Pitch.find_one(Pitch.email == email)
