from fastapi import APIRouter, Query
from app.controller.connectController import *
from app.schema.connectSchema import *

router = APIRouter()

@router.post("/", response_model=ConnectCreateResponseSchema, summary="Submit Connect Form")
async def connect_create(payload: ConnectCreateRequestSchema):
    return await connect_create_controller(payload)


@router.get("/", summary="To get the data for admin dashbaord", response_model=ConnectFetchResponseSchema)
async def connect_fetch(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to fetch")
):
    result =  await connect_fetch_controller(skip, limit)
    return result
