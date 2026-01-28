from app.services.connectService import ConnectService
from app.repository.connect_repository import ConnectRepository
from app.schema.connectSchema import *

async def connect_create_controller(payload: ConnectCreateRequestSchema) -> ConnectCreateResponseSchema:
    result = await ConnectService.connect_create_service(payload)
    return result

async def connect_fetch_controller(
    skip: int = 0,
    limit: int = 20
) -> ConnectFetchResponseSchema:
    
    docs = await ConnectRepository.connect_get_all_repository(
        skip=skip,
        limit=limit
    )

    data = [
        ConnectFormEntry(
            name=doc.name,
            email=doc.email,
            purpose=doc.purpose,
            message=doc.message,
            created_at=doc.created_at
        )
        for doc in docs
    ]

    return ConnectFetchResponseSchema(
        success=True,
        limit=limit,
        skip=skip,
        count=len(data),
        data=data
    )