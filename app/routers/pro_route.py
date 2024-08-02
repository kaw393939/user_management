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
from app.utils.minio_client import upload_profile_picture, get_profile_picture_url
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

@router.get("/users/me/check-profile-completion", response_model=UserResponse, tags=["User Management Requires (Authenticated User)"])
async def check_profile_completion(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    _=Depends(require_role(["ADMIN", "MANAGER", "AUTHENTICATED"]))
):
    user_id = current_user["user_id"]
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.profile_complete = is_profile_complete(user)

    return user

@router.post("/users/me/request-pro-role", tags=["User Management Requires (Authenticated User)"])
async def request_pro_role(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    _=Depends(require_role(["ADMIN", "MANAGER", "AUTHENTICATED"]))
):
    user_id = current_user["user_id"]
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not is_profile_complete(user):
        raise HTTPException(status_code=400, detail="Profile is not complete")

    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        return {"message": "User already has a high-level role and cannot be assigned a pro role"}

    user.role = UserRole.PRO
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message": "User role updated to pro successfully", "new_role": user.role}