from builtins import Exception, bool, classmethod, int, str
from datetime import datetime, timezone
from typing import Optional, Dict, List
from pydantic import ValidationError
from sqlalchemy import func, null, update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import Event, EventType, User
from app.schemas.event_schema import EventCreate, EventUpdate
from app.services.db_service import DbService
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class EventService(DbService):
    @classmethod
    async def _fetch_event(cls, session: AsyncSession, **kwargs) -> Optional[Event]:
        query = select(Event).filter_by(**kwargs)
        result = await cls._execute_query(session, query)
        return result.scalars().first()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, event_id: UUID) -> Optional[Event]:
        return await cls._fetch_event(session, id=event_id)

    @classmethod
    async def get_by_title(cls, session: AsyncSession, title: str) -> Optional[Event]:
        return await cls._fetch_event(session, title=title)

    @classmethod
    async def create(cls, session: AsyncSession, event_data: Dict[str, str]) -> Optional[Event]:
        try:
            validated_data = EventCreate(**event_data).model_dump()
            logging.info(f"My validated data is: {validated_data}")
            new_event = Event(**validated_data)
            session.add(new_event)
            await session.commit()
            return new_event
        except ValidationError as e:
            logger.error(f"Validation error during event creation: {e}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, event_id: UUID, update_data: Dict[str, str]) -> Optional[Event]:
        try:
            validated_data = EventUpdate(**update_data).model_dump(exclude_unset=True)
            query = update(Event).where(Event.id == event_id).values(**validated_data).execution_options(synchronize_session="fetch")
            await cls._execute_query(session, query)
            updated_event = await cls.get_by_id(session, event_id)
            if updated_event:
                session.refresh(updated_event)
                logger.info(f"Event {event_id} updated successfully.")
                return updated_event
            else:
                logger.error(f"Event {event_id} not found after update attempt.")
                return None
        except ValidationError as e:  # Add this block to handle validation errors
            logger.error(f"Validation error during event update: {e}")
            return None
        except Exception as e:
            logger.error(f"Error during event update: {e}")
            return None
        
    @classmethod
    async def delete(cls, session: AsyncSession, event_id: UUID) -> bool:
        event = await cls.get_by_id(session, event_id)
        if not event:
            logger.info(f"Event with ID {event_id} not found.")
            return False
        await session.delete(event)
        await session.commit()
        return True

    @classmethod
    async def list_events(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[Event]:
        query = select(Event).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def publish_event(cls, session: AsyncSession, event_id: UUID) -> Optional[Event]:
        event = await cls.get_by_id(session, event_id)
        if event:
            event.publish_event()
            session.add(event)
            await session.commit()
            return event
        return None

    @classmethod
    async def unpublish_event(cls, session: AsyncSession, event_id: UUID) -> Optional[Event]:
        event = await cls.get_by_id(session, event_id)
        if event:
            event.unpublish_event()
            session.add(event)
            await session.commit()
            return event
        return None

    @classmethod
    async def list_events_by_creator(cls, session: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 10) -> List[Event]:
        query = select(Event).where(Event.creator_id == creator_id).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def list_published_events(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[Event]:
        query = select(Event).where(Event.published == True).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def list_events_by_type(cls, session: AsyncSession, event_type: EventType, skip: int = 0, limit: int = 10) -> List[Event]:
        query = select(Event).where(Event.event_type == event_type).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def count_events(cls, session: AsyncSession) -> int:
        query = select(func.count()).select_from(Event)
        result = await session.execute(query)
        count = result.scalar()
        return count