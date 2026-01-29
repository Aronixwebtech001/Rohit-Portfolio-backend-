import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.core.config import settings


# 🔹 configure once
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


async def upload_file_to_cloudinary(
    file: UploadFile,
    folder: str,
    resource_type: str = "auto",  # image / video / raw / auto
) -> dict:
    """
    Uploads file to Cloudinary and returns important metadata
    """

    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            resource_type=resource_type,
        )

        return {
            "public_id": result["public_id"],
            "url": result["secure_url"],
            "resource_type": result["resource_type"],
            "format": result.get("format"),
            "bytes": result.get("bytes"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary upload failed: {str(e)}"
        )
