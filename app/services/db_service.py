from builtins import classmethod
import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
logger = logging.getLogger(__name__)

class DbService:
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

    