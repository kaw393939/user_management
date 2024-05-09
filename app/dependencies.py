from builtins import Exception, dict, list, str
import uuid
from fastapi import Depends, HTTPException, Header, Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Database
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import decode_token
from settings.config import Settings
from sqlalchemy.exc import SQLAlchemyError

def get_settings() -> Settings:
    """Return application settings."""
    return Settings()

def get_email_service() -> EmailService:
    template_manager = TemplateManager()
    return EmailService(template_manager=template_manager)

async def get_db() -> AsyncSession:
    """Dependency that provides a database session for each request."""
    async_session_factory = Database.get_session_factory()
    async with async_session_factory() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error: " + str(e))



async def get_current_user(
    access_token: str = Cookie(None),
    authorization: str = Header(None)
):
    print(f"Access token: {access_token}")
    print(f"Authorization header: {authorization}")

    if access_token is None and authorization is None:
        return None

    if access_token is None:
        # Extract the token from the Authorization header
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() != "bearer":
            return None
        access_token = param

    try:
        payload = decode_token(access_token)
        print(f"Decoded payload: {payload}")
        if payload is None:
            return None
        user_role: str = payload.get("role")
        user_id_string = payload.get("user_id")
        user_id = uuid.UUID(user_id_string) 
        user_email: str = payload.get("sub")
        print(f"User ID in the payload is: {user_id}")
        if user_role is None or user_id is None:
            return None
        return {"sub": user_email, "role": user_role, "user_id": user_id}
    except Exception as e:
        print(f"Error decoding token: {str(e)}") 
        return None

def require_role(roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return current_user
    return role_checker