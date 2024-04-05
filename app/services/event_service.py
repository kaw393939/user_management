from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Event
from uuid import UUID

async def create_event(db: AsyncSession, creator_id: UUID, title: str, description: str, qr_code_path: str = None) -> Event:
    """
    Asynchronously create a new event.
    """
    new_event = Event(
        title=title,
        description=description,
        creator_id=creator_id,
        qr_code_path=qr_code_path
    )
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

async def get_events(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Event]:
    """
    Asynchronously retrieve a list of events, with pagination.
    """
    stmt = select(Event).offset(skip).limit(limit)
    result = await db.execute(stmt)
    events = result.scalars().all()
    return events

async def get_event(db: AsyncSession, event_id: UUID) -> Event:
    """
    Asynchronously retrieve an event by its ID.
    """
    stmt = select(Event).filter(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalars().first()
    return event

async def update_event(db: AsyncSession, event_id: UUID, title: str = None, description: str = None, qr_code_path: str = None) -> Event:
    """
    Asynchronously update event details.
    """
    stmt = select(Event).filter(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalars().first()
    if event:
        if title is not None:
            event.title = title
        if description is not None:
            event.description = description
        if qr_code_path is not None:
            event.qr_code_path = qr_code_path
        await db.commit()
        return event
    return None

async def delete_event(db: AsyncSession, event_id: UUID) -> bool:
    """
    Asynchronously delete an event by its ID.
    """
    stmt = select(Event).filter(Event.id == event_id)
    result = await db.execute(stmt)
    event = result.scalars().first()
    if event:
        await db.delete(event)
        await db.commit()
        return True
    return False
