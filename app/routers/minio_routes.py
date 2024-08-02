from builtins import dict, int, len, str
from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, UploadFile, File, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, get_db, get_email_service, require_role
from app.schemas.pagination_schema import EnhancedPagination
from app.schemas.token_schema import TokenResponse
from app.schemas.user_schemas import LoginRequest, UserBase, UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.services.jwt_service import create_access_token
from app.utils.link_generation import create_user_links, generate_pagination_links
from app.dependencies import get_settings
from sqlalchemy import inspect, text
from app.services.email_service import EmailService
from app.utils.minio_client import get_profile_picture_stream, upload_profile_picture
from sqlalchemy.future import select
from io import BytesIO
from app.models.user_model import User, UserRole
import logging
import csv
from io import StringIO
from typing import List
from app.services.user_service import is_profile_complete

logger = logging.getLogger(__name__)

router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
settings = get_settings()

@router.post("/users/me/upload-profile-picture", tags = ["User Management Requires (Authenticated User)"])
async def upload_profile_picture_endpoint(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    _=Depends(require_role(["ADMIN", "MANAGER", "AUTHENTICATED"]))
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    file_data = await file.read()
    data_stream = BytesIO(file_data)
    user_id = current_user["user_id"]
    file_extension = file.filename.split('.')[-1]
    secure_filename = f"{user_id}.{file_extension}"

    try:
        # Replace this with actual MinIO upload logic and URL retrieval
        url = upload_profile_picture(data_stream, secure_filename)

        # Update the current user's profile picture URL in the database
        user_id = current_user["user_id"]  # Accessing the user_id from the current_user dictionary
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.profile_picture_url = url
        db.add(user)
        await db.commit()
        await db.refresh(user)

        logger.debug(f"Profile picture URL updated for user: {user.id}, URL: {user.profile_picture_url}")

        return {"message": "Profile picture uploaded successfully.", "profile_picture_url": url}
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@router.get("/users/me/profile-picture", tags=["User Management Requires (Authenticated User)"])
async def get_profile_picture(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role(["ADMIN", "MANAGER", "AUTHENTICATED"]))
):
    user_id = current_user["user_id"]
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or user.profile_picture_url is None:
        raise HTTPException(status_code=404, detail="Profile picture not found")

    file_name = user.profile_picture_url.split("/")[-1]

    try:
        file_stream = get_profile_picture_stream(file_name)
        return StreamingResponse(file_stream, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")