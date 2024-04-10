from datetime import datetime, timezone
from typing import Optional, Dict, List
from pydantic import ValidationError
from sqlalchemy import update, select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_settings
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password
from uuid import UUID
import logging

settings = get_settings()  # Ensure settings are appropriately configured for max login attempts, etc.
logger = logging.getLogger(__name__)

class UserService:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        return await cls._fetch_one(session, User, id=user_id)

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str) -> Optional[User]:
        return await cls._fetch_one(session, User, username=username)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        return await cls._fetch_one(session, User, email=email)

    @classmethod
    async def create(cls, session: AsyncSession, user_data: Dict[str, str]) -> Optional[User]:
        try:
            validated_data = UserCreate(**user_data).dict(exclude_unset=True)
            # Check for existing username or email
            existing_user = await session.execute(select(User).where(
                or_(User.email == validated_data['email'], User.username == validated_data['username'])))
            if existing_user.scalars().first():
                logger.error("User with given email or username already exists.")
                return None
            validated_data['hashed_password'] = hash_password(validated_data.pop('password'))
            new_user = User(**validated_data)
            session.add(new_user)
            await session.commit()
            return new_user
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Failed to create user: {e}")
            await session.rollback()
            return None

    @classmethod
    async def update(cls, session: AsyncSession, user_id: UUID, update_data: Dict[str, str]) -> Optional[User]:
        try:
            validated_data = UserUpdate(**update_data).model_dump(exclude_unset=True)
            if 'password' in validated_data:
                validated_data['hashed_password'] = hash_password(validated_data.pop('password'))
            await cls._update_user_fields(session, user_id, **validated_data)
            user = await cls.get_by_id(session, user_id)
            return user
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            await session.rollback()
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID) -> bool:
        user = await cls.get_by_id(session, user_id)
        if not user:
            logger.info(f"User {user_id} not found for deletion.")
            return False
        try:
            await session.delete(user)
            await session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            await session.rollback()
            return False

    @classmethod
    async def list_users(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
        try:
            results = await session.execute(select(User).offset(skip).limit(limit))
            return results.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to list users: {e}")
            return []

    @classmethod
    async def register_user(cls, session: AsyncSession, user_data: Dict[str, str]) -> Optional[User]:
        return await cls.create(session, user_data)

    @classmethod
    async def login_user(cls, session: AsyncSession, username: str, password: str) -> Optional[User]:
        # logging.debug(f"username: {username} and password {password}")
        user = await cls.get_by_username(session, username)
        # logging.debug(f"username Found: {user.username}")
        # logging.debug(f"password Found: {user.hashed_password}")
        # logging.debug(f"hashed input password Found: {hash_password(password)}")
        # logging.debug(f"verify password results {verify_password(password, user.hashed_password)}")

        if user and verify_password(password, user.hashed_password):
            await cls._update_user_fields(session, user.id, last_login_at=datetime.now(timezone.utc), failed_login_attempts=0)
            return user
        elif user:
            failed_attempts = user.failed_login_attempts + 1
            await cls._update_user_fields(session, user.id, failed_login_attempts=failed_attempts)
        return None

    @classmethod
    async def is_account_locked(cls, session: AsyncSession, username: str) -> bool:
        user = await cls.get_by_username(session, username)
        return user.failed_login_attempts >= settings.max_login_attempts if user else False

    # Utility Methods
    @classmethod
    async def _fetch_one(cls, session: AsyncSession, model, **filters) -> Optional[User]:
        try:
            result = await session.execute(select(model).filter_by(**filters))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Query execution error: {e}")
            return None

    @classmethod
    async def _update_user_fields(cls, session: AsyncSession, user_id: UUID, **fields):
        try:
            if not fields:
                return
            await session.execute(update(User).where(User.id == user_id).values(**fields))
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Failed to update user fields for user {user_id}: {e}")
            await session.rollback()
