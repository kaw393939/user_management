from datetime import datetime, timezone
from typing import Optional, Dict, List
from pydantic import ValidationError
from sqlalchemy import update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_settings
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password
from uuid import UUID
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class UserService:
    """
    Service class for managing user-related database operations.
    """

    @classmethod
    async def _execute_query(cls, session: AsyncSession, query):
        """
        Helper method to execute a query and handle database errors.

        :param session: The AsyncSession instance.
        :param query: The query to be executed.
        :return: The result of the query execution.
        """
        try:
            result = await session.execute(query)
            await session.commit()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            raise e

    @classmethod
    async def _fetch_user(cls, session: AsyncSession, **filters) -> Optional[User]:
        """
        Helper method to fetch a user based on the provided filters.

        :param session: The AsyncSession instance.
        :param filters: The filters to apply to the user query.
        :return: The user instance if found, None otherwise.
        """
        query = select(User).filter_by(**filters)
        try:
            result = await cls._execute_query(session, query)
            return result.scalars().first()
        except SQLAlchemyError:
            return None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by their ID.

        :param session: The AsyncSession instance.
        :param user_id: The ID of the user.
        :return: The user instance if found, None otherwise.
        """
        return await cls._fetch_user(session, id=user_id)

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.

        :param session: The AsyncSession instance.
        :param username: The username of the user.
        :return: The user instance if found, None otherwise.
        """
        return await cls._fetch_user(session, username=username)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.

        :param session: The AsyncSession instance.
        :param email: The email of the user.
        :return: The user instance if found, None otherwise.
        """
        return await cls._fetch_user(session, email=email)

    @classmethod
    async def create(cls, session: AsyncSession, user_data: Dict[str, str]) -> Optional[User]:
        """
        Create a new user.

        :param session: The AsyncSession instance.
        :param user_data: The data for creating the user.
        :return: The created user instance if successful, None otherwise.
        """
        try:
            validated_data = UserCreate(**user_data).dict(exclude_unset=True)
            if (await cls.get_by_username(session, validated_data['username'])) or (await cls.get_by_email(session, validated_data['email'])):
                logger.error("User with given email or username already exists.")
                return None
            validated_data['hashed_password'] = hash_password(validated_data.pop('password'))
            new_user = User(**validated_data)
            session.add(new_user)
            await session.commit()  # Ensure changes are committed to the database.
            return new_user
        except ValidationError as e:
            logger.error(f"Failed to create user: {e}")
            await session.rollback()
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating user: {e}")
            raise e

    @classmethod
    async def update(cls, session: AsyncSession, user_id: UUID, update_data: Dict[str, str]) -> Optional[User]:
        """
        Update an existing user.

        :param session: The AsyncSession instance.
        :param user_id: The ID of the user to update.
        :param update_data: The data to update the user with.
        :return: The updated user instance if successful, None otherwise.
        """
        try:
            validated_data = UserUpdate(**update_data).dict(exclude_unset=True)
            query = update(User).where(User.id == user_id).values(**validated_data)
            await cls._execute_query(session, query)
            return await cls.get_by_id(session, user_id)
        except ValidationError as e:
            logger.error(f"Failed to update user: {e}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating user: {e}")
            raise e

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID) -> bool:
        """
        Delete a user.

        :param session: The AsyncSession instance.
        :param user_id: The ID of the user to delete.
        :return: True if the user was deleted successfully, False otherwise.
        """
        try:
            user = await cls.get_by_id(session, user_id)
            if not user:
                logger.info(f"User with ID {user_id} not found.")
                return False
            await session.delete(user)
            await session.commit()
            logger.info(f"User with ID {user_id} deleted successfully.")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete user with ID {user_id}: {e}")
            await session.rollback()
            raise e

    @classmethod
    async def list_users(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
        """
        Retrieve a list of users with pagination.

        :param session: The AsyncSession instance.
        :param skip: The number of users to skip.
        :param limit: The maximum number of users to retrieve.
        :return: The list of users.
        """
        query = select(User).offset(skip).limit(limit)
        try:
            result = await cls._execute_query(session, query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve user list: {e}")
            raise e

    @classmethod
    async def register_user(cls, session: AsyncSession, user_data: Dict[str, str]) -> Optional[User]:
        """
        Register a new user.

        :param session: The AsyncSession instance.
        :param user_data: The data for registering the user.
        :return: The registered user instance if successful, None otherwise.
        """
        return await cls.create(session, user_data)

    @classmethod
    async def login_user(cls, session: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user and update their login details.

        :param session: The AsyncSession instance.
        :param username: The username of the user.
        :param password: The password of the user.
        :return: The authenticated user instance if successful, None otherwise.
        """
        user = await cls.get_by_username(session, username)
        if user:
            if user.is_locked or not verify_password(password, user.hashed_password):
                # Increment failed login attempts and check if account should be locked
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= settings.max_login_attempts:
                    user.is_locked = True
                session.add(user)
                await session.commit()
                return None  # Return None if the account is locked or password is incorrect

            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.last_login_at = datetime.now(timezone.utc)
            session.add(user)
            await session.commit()
            return user

        return None

    

    @classmethod
    async def is_account_locked(cls, session: AsyncSession, username: str) -> bool:
        """
        Check if a user's account is locked.

        :param session: The AsyncSession instance.
        :param username: The username of the user.
        :return: True if the account is locked, False otherwise.
        """
        user = await cls.get_by_username(session, username)
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
    async def verify_email(cls, session: AsyncSession, user_id: UUID) -> bool:
        user = await cls.get_by_id(session, user_id)
        if user:
            user.email_verified = True
            session.add(user)
            await session.commit()
            return True
        return False


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
