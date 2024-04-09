"""
This Python file serves as a comprehensive guide to implementing CRUD (Create, Read, Update, Delete) operations 
on a User model in a FastAPI application using SQLAlchemy with asynchronous operations. It demonstrates best practices 
for structuring service layer logic that interacts with the database asynchronously, ensuring non-blocking database 
operations. This approach enhances the application's performance, especially under high load, by allowing it to handle 
other tasks while awaiting database responses.

The UserService class contains methods for managing User records, including fetching by ID, username, email, creating, 
updating, deleting users, and listing users with basic pagination. Each method showcases asynchronous handling of 
database sessions, queries, and transactions, with added error handling and logging for robustness and easier debugging.

Key concepts covered include:
- Asynchronous session management in SQLAlchemy.
- Executing CRUD operations asynchronously.
- Using transactions and rolling back in case of errors.
- Securely handling sensitive information like passwords.
- Implementing pagination in database queries.
"""

from typing import List, Optional, Dict
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from app.models.user_model import User
from app.utils.security import hash_password
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class UserService:
    @classmethod
    async def _execute_query(cls, session: AsyncSession, query):
        """Helper method to execute a query with error handling.
        
        Args:
            session (AsyncSession): The database session.
            query: The SQLAlchemy query object.
            
        Returns:
            The result of the query execution or None if an error occurred.
        """
        try:
            result = await session.execute(query)
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            return None

    @classmethod
    async def _fetch_one(cls, session: AsyncSession, model, **filters) -> Optional[User]:
        """Generic method to fetch a single record based on filters.
        
        Args:
            session (AsyncSession): The database session.
            model: The SQLAlchemy model class to query.
            **filters: Keyword arguments representing filter conditions.
            
        Returns:
            The first result based on the filter conditions or None if no results found.
        """
        query = select(model).filter_by(**filters)
        result = await cls._execute_query(session, query)
        return result.scalars().first() if result else None
    @classmethod
    async def count(cls, db_session: AsyncSession) -> int:
        """
        Count the total number of users in the database.

        :param db_session: The database session.
        :return: The total number of users.
        """
        async with db_session as session:
            total = await session.execute(select(func.count(User.id)))
            return total.scalar()
        
    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        """Fetch a user by ID without relationships.
        
        Args:
            session (AsyncSession): The database session.
            user_id (UUID): The unique identifier of the user.
            
        Returns:
            The User object if found, otherwise None.
        """
        return await cls._fetch_one(session, User, id=user_id)

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str) -> Optional[User]:
        """Fetch a user by username.
        
        Args:
            session (AsyncSession): The database session.
            username (str): The username of the user.
            
        Returns:
            The User object if found, otherwise None.
        """
        return await cls._fetch_one(session, User, username=username)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        """Fetch a user by email.
        
        Args:
            session (AsyncSession): The database session.
            email (str): The email of the user.
            
        Returns:
            The User object if found, otherwise None.
        """
        return await cls._fetch_one(session, User, email=email)

    @classmethod
    async def create(cls, session: AsyncSession, user_data: Dict) -> Optional[User]:
        """Create a new user with the given data.
        
        Args:
            session (AsyncSession): The database session.
            user_data (Dict): A dictionary containing the user's data.
            
        Returns:
            The newly created User object or None if the creation failed.
        """
        try:
            if 'password' in user_data:
                user_data['hashed_password'] = hash_password(user_data.pop('password'))
            user = User(**user_data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            logger.error(f"Failed to create user {user_data.get('username', '')}: {e}")
            await session.rollback()
            return None

    @classmethod
    async def update(cls, session: AsyncSession, user_id: UUID, update_data: Dict[str, str]) -> Optional[User]:
        """Update an existing user's information.

        Args:
            session (AsyncSession): The database session.
            user_id (UUID): The ID of the user to update.
            update_data (Dict[str, str]): A dictionary of fields to update.

        Returns:
            Optional[User]: The updated user object, or None if the update failed.
        """
        try:
            # Fetch the user to be updated
            user = await cls.get_by_id(session, user_id)
            if not user:
                logger.info(f"User {user_id} not found.")
                return None

            # Update the user attributes
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    logger.warning(f"Attempted to update unknown attribute '{key}' for user {user_id}.")
            
            # Commit the transaction
            await session.commit()

            # Refresh and return the updated user object
            await session.flush()
            await session.refresh(user)
            return user
        except SQLAlchemyError as e:
            # Log the exception and rollback the transaction
            logger.error(f"Failed to update user {user_id}: {e}")
            await session.rollback()
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID) -> bool:
        """Delete a user by ID.
        
        Args:
            session (AsyncSession): The database session.
            user_id (UUID): The ID of the user to delete.
            
        Returns:
            True if the user was successfully deleted, False otherwise.
        """
        try:
            user = await cls.get_by_id(session, user_id)
            if user:
                await session.delete(user)
                await session.commit()
                return True
            else:
                logger.info(f"User {user_id} not found for deletion.")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            await session.rollback()
            return False

    @classmethod
    async def list_users(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
        """
        List users with basic pagination.

        Parameters:
        - session (AsyncSession): The database session to use for the query.
        - skip (int): Number of records to skip (for pagination).
        - limit (int): Maximum number of records to return.

        Returns:
        - List[User]: A list of users.
        """
        try:
            # Prepare query with pagination
            query = select(User).offset(skip).limit(limit)
            result = await cls._execute_query(session, query)
            # Fetch all results
            return result.scalars().all() if result else []
        except SQLAlchemyError as e:
            logger.error(f"Failed to list users: {e}")
            return []
