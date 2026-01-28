from fastapi import APIRouter, HTTPException, status
from app.core.config import settings
from app.schema.admin_schema import AdminLoginRequest

router = APIRouter()

@router.post("/login")
def admin_login(payload: AdminLoginRequest):
    if payload.username != settings.ADMIN_USERNAME and payload.password != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {
        "success": True,
        "message": "Admin login successful"
    }
