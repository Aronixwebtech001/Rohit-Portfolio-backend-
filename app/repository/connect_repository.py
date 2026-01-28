from typing import List, Optional
from app.models.connect_model import Connect
from app.schema.connectSchema import ConnectCreateRequestSchema


class ConnectRepository:
    """
    Data Access Layer for Connect collection
    """

    @staticmethod
    async def connect_create_repository(
        payload: ConnectCreateRequestSchema,
    ) -> Connect:
        connect = Connect(**payload.model_dump())
        return await connect.insert()

    @staticmethod
    async def connect_get_all_repository(skip: int, limit: int):
        return await (
            Connect
            .find_all()
            .sort(-Connect.created_at)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

    @staticmethod
    async def connect_get_by_email_repository(
        email: str,
    ) -> Optional[Connect]:
        return await Connect.find_one(Connect.email == email)
