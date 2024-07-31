from builtins import Exception, bool, classmethod, int, str
from datetime import datetime, timezone
import secrets
from typing import Optional, Dict, List
from pydantic import ValidationError
from fastapi import HTTPException
from settings.config import Settings
from sqlalchemy import func, null, update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_email_service, get_settings
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.nickname_gen import generate_nickname
from app.utils.security import generate_verification_token, hash_password, verify_password
from uuid import UUID
from app.services.email_service import EmailService
from app.models.user_model import UserRole
import logging
from dotenv import load_dotenv
import os
load_dotenv()

settings = get_settings()
logger = logging.getLogger(__name__)

from minio import Minio
from minio.error import InvalidResponseError

minio_access_key = os.getenv("MINIO_ACCESS_KEY", "default_access_key")
minio_secret_key = os.getenv("MINIO_SECRET_KEY", "default_secret_key")

minio_client = Minio(
    endpoint='127.0.0.1:9000',  # Update this to your MinIO endpoint
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False,  # Set to True if your MinIO server uses HTTPS
)

class UserService:
    @classmethod
    async def _execute_query(cls, session: AsyncSession, query):
        try:
            result = await session.execute(query)
            await session.commit()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            return None

    @classmethod
    async def _fetch_user(cls, session: AsyncSession, **filters) -> Optional[User]:
        query = select(User).filter_by(**filters)
        result = await cls._execute_query(session, query)
        return result.scalars().first() if result else None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        return await cls._fetch_user(session, id=user_id)

    @classmethod
    async def get_by_nickname(cls, session: AsyncSession, nickname: str) -> Optional[User]:
        return await cls._fetch_user(session, nickname=nickname)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        return await cls._fetch_user(session, email=email)

    @classmethod
    async def create(cls, session: AsyncSession, user_data: Dict[str, str], email_service: EmailService) -> Optional[User]:
        try:
            validated_data = UserCreate(**user_data).model_dump()
            existing_user = await cls.get_by_email(session, validated_data['email'])
            if existing_user:
                logger.error("User with given email already exists.")
                return None
            validated_data['hashed_password'] = hash_password(validated_data.pop('password'))
            new_user = User(**validated_data)
            new_nickname = generate_nickname()
            while await cls.get_by_nickname(session, new_nickname):
                new_nickname = generate_nickname()
            new_user.nickname = new_nickname
            logger.info(f"User Role: {new_user.role}")
            user_count = await cls.count(session)
            new_user.role = UserRole.ADMIN if user_count == 0 else UserRole.ANONYMOUS            
            if new_user.role == UserRole.ADMIN:
                new_user.email_verified = True

            new_user.verification_token = generate_verification_token()

            session.add(new_user)
            await session.commit()
            await email_service.send_verification_email(new_user)
            return new_user
        except ValidationError as e:
            logger.error(f"Validation error during user creation: {e}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, user_id: UUID, update_data: Dict[str, str]) -> Optional[User]:
        try:
            # validated_data = UserUpdate(**update_data).dict(exclude_unset=True)
            validated_data = UserUpdate(**update_data).model_dump(exclude_unset=True)

            if 'password' in validated_data:
                validated_data['hashed_password'] = hash_password(validated_data.pop('password'))
            query = update(User).where(User.id == user_id).values(**validated_data).execution_options(synchronize_session="fetch")
            await cls._execute_query(session, query)
            updated_user = await cls.get_by_id(session, user_id)
            if updated_user:
                session.refresh(updated_user)  # Explicitly refresh the updated user object
                logger.info(f"User {user_id} updated successfully.")
                return updated_user
            else:
                logger.error(f"User {user_id} not found after update attempt.")
            return None
        except Exception as e:  # Broad exception handling for debugging
            logger.error(f"Error during user update: {e}")
            return None

    @staticmethod
    async def update_professional_status(db_session: AsyncSession, user_id: int, status_update: dict, request_user) -> None:
        # Check if the requesting user has the required role
        if request_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
            raise HTTPException(status_code=403, detail="Unauthorized to change professional status")

        # Find the user in the database
        statement = select(User).where(User.id == user_id)
        result = await db_session.execute(statement)
        user = result.scalars().first()

        # Check if the user exists
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the professional status
        user.is_professional = status_update['is_professional']
        user.professional_status_updated_at = func.now()
        await db_session.commit()

        return user

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID) -> bool:
        user = await cls.get_by_id(session, user_id)
        if not user:
            logger.info(f"User with ID {user_id} not found.")
            return False
        await session.delete(user)
        await session.commit()
        return True

    @classmethod
    async def list_users(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def register_user(cls, session: AsyncSession, user_data: Dict[str, str], get_email_service) -> Optional[User]:
        return await cls.create(session, user_data, get_email_service)
    

    @classmethod
    async def login_user(cls, session: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await cls.get_by_email(session, email)
        if user:
            if user.email_verified is False:
                return None
            if user.is_locked:
                return None
            if verify_password(password, user.hashed_password):
                user.failed_login_attempts = 0
                user.last_login_at = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                return user
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= settings.max_login_attempts:
                    user.is_locked = True
                session.add(user)
                await session.commit()
        return None

    @classmethod
    async def is_account_locked(cls, session: AsyncSession, email: str) -> bool:
        user = await cls.get_by_email(session, email)
        return user.is_locked if user else False


    @classmethod
    async def reset_password(cls, session: AsyncSession, user_id: UUID, new_password: str) -> bool:
        hashed_password = hash_password(new_password)
        user = await cls.get_by_id(session, user_id)
        if user:
            user.hashed_password = hashed_password
            user.failed_login_attempts = 0  # Resetting failed login attempts
            user.is_locked = False  # Unlocking the user account, if locked
            session.add(user)
            await session.commit()
            return True
        return False

    @classmethod
    async def verify_email_with_token(cls, session: AsyncSession, user_id: UUID, token: str) -> bool:
        user = await cls.get_by_id(session, user_id)
        if user and user.verification_token == token:
            user.email_verified = True
            user.verification_token = None  # Clear the token once used
            if user.role == UserRole.ANONYMOUS:
                user.role = UserRole.AUTHENTICATED
            session.add(user)
            await session.commit()
            return True
        return False

    @classmethod
    async def count(cls, session: AsyncSession) -> int:
        """
        Count the number of users in the database.

        :param session: The AsyncSession instance for database access.
        :return: The count of users.
        """
        query = select(func.count()).select_from(User)
        result = await session.execute(query)
        count = result.scalar()
        return count
    
    @classmethod
    async def unlock_user_account(cls, session: AsyncSession, user_id: UUID) -> bool:
        user = await cls.get_by_id(session, user_id)
        if user and user.is_locked:
            user.is_locked = False
            user.failed_login_attempts = 0  # Optionally reset failed login attempts
            session.add(user)
            await session.commit()
            return True
        return False
    
    @classmethod
    async def upload_profile_picture(cls, user_id: UUID, file_data: bytes) -> Optional[str]:
        try:
            file_name = f"profile_picture_{user_id}.jpg"
            minio_client.put_object(
                "demo",  # Bucket name
                file_name,
                file_data,
                len(file_data),
            )
            return file_name
        except InvalidResponseError as e:
            logger.error(f"Error uploading profile picture to MinIO: {e}")
            return None
        
    @classmethod
    async def update_profile_picture_url(cls, session: AsyncSession, user_id: UUID, picture_url: str) -> Optional[User]:
        try:
            query = update(User).where(User.id == user_id).values(profile_picture_url=picture_url).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await session.commit()
            updated_user = await session.execute(select(User).where(User.id == user_id))
            updated_user = updated_user.scalars().first()
            if updated_user:
                logger.info(f"User {user_id} profile picture URL updated successfully.")
                return updated_user
            else:
                logger.error(f"User {user_id} not found after updating profile picture URL.")
                return None
        except Exception as e:  # Broad exception handling for debugging
            logger.error(f"Error updating user profile picture URL: {e}")
            return None