from builtins import Exception, dict, str
from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Database
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import decode_token
from app.models.user_model import UserRole
from settings.config import Settings

def get_settings() -> Settings:
    """Return application settings."""
    return Settings()

def get_email_service() -> EmailService:
    """function gets email service"""
    template_manager = TemplateManager()
    return EmailService(template_manager=template_manager)

async def get_db() -> AsyncSession:
    """Dependency that provides a database session for each request."""
    async_session_factory = Database.get_session_factory()
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """function gets current user info"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    user_email: str = payload.get("sub")
    user_role: str = payload.get("role")
    user_id: str = payload.get("id")
    if user_email is None or user_role is None or user_id is None:
        raise credentials_exception
    return {"user_email": user_email, "role": user_role, "user_id": user_id}

def require_role(role: str):
    """function requires role"""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in role:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return role_checker

async def get_user_role(current_user: dict = Depends(get_current_user)):
    """function gets user role"""
    # Extract the role from the current user dictionary
    user_role = current_user.get("role")

    # Check if the role is valid
    if user_role not in [role.value for role in UserRole]:
        raise HTTPException(status_code=403, detail="Invalid user role")

    return user_role
