
from builtins import ValueError, hasattr, len
from datetime import datetime, timedelta
import pytest
import logging

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.models.user_model import Event, EventType, User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event_details(event: Event):
    logging.info(f"Event Title: {event.title}")
    logging.info(f"Event Start: {event.start_datetime}")
    logging.info(f"Event End: {event.end_datetime}")
    logging.info(f"Event Published: {event.published}")
    logging.info(f"Event Type: {event.event_type.name}")
    if event.creator:
        logging.info(f"Creator Nickname: {event.creator.nickname}")
        logging.info(f"Creator Email: {event.creator.email}")


async def log_user_event_details(user: User, db_session: AsyncSession):
    logging.info(f"User ID: {user.id}")
    logging.info(f"User Nickname: {user.nickname}")
    
    await db_session.refresh(user, ['events'])
    
    if user.events:
        for event in user.events:
            logging.info(f"Event ID: {event.id} Title: {event.title}")
    else:
        logging.info("No events found for this user.")

@pytest.mark.asyncio
async def test_event_creation(db_session: AsyncSession, verified_user):
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "start_datetime": datetime.now(),
        "end_datetime": datetime.now() + timedelta(hours=2),
        "published": False,
        "event_type": EventType.COMPANY_TOUR,
        "creator_id": verified_user.id
    }
    event = Event(**event_data)
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)

    assert event.title == "Test Event"
    assert event.description == "This is a test event"
    assert event.published is False
    assert event.event_type == EventType.COMPANY_TOUR
    assert event.creator_id == verified_user.id

@pytest.mark.asyncio
async def test_event_update(db_session: AsyncSession, company_tour_event):
    company_tour_event.title = "Updated Company Tour"
    company_tour_event.published = True
    await db_session.commit()
    await db_session.refresh(company_tour_event)

    assert company_tour_event.title == "Updated Company Tour"
    assert company_tour_event.published is True

@pytest.mark.asyncio
async def test_event_delete(db_session: AsyncSession, mock_interview_event):
    await db_session.delete(mock_interview_event)
    await db_session.commit()

    deleted_event = await db_session.get(Event, mock_interview_event.id)
    assert deleted_event is None

@pytest.mark.asyncio
async def test_user_events_relationship(db_session: AsyncSession, verified_user):
    event1 = Event(
        title="Event 1",
        description="Test event 1",
        start_datetime=datetime.now(),
        end_datetime=datetime.now() + timedelta(hours=1),
        published=True,
        event_type=EventType.COMPANY_TOUR,
        creator=verified_user,
    )
    event2 = Event(
        title="Event 2",
        description="Test event 2",
        start_datetime=datetime.now() + timedelta(days=1),
        end_datetime=datetime.now() + timedelta(days=1, hours=1),
        published=False,
        event_type=EventType.MOCK_INTERVIEW,
        creator=verified_user,
    )
    db_session.add_all([event1, event2])
    await db_session.commit()

    user_events = await db_session.scalars(select(Event).where(Event.creator_id == verified_user.id))
    assert len(user_events.all()) == 2

@pytest.mark.asyncio
async def test_event_creator_relationship(db_session: AsyncSession, guest_lecture_event):
    creator = await db_session.get(User, guest_lecture_event.creator_id)
    assert creator is not None
    assert creator.role == UserRole.MANAGER

@pytest.mark.asyncio
async def test_event_publish_unpublish(db_session: AsyncSession, company_tour_event):
    assert company_tour_event.published is False

    company_tour_event.publish_event()
    await db_session.commit()
    await db_session.refresh(company_tour_event)
    assert company_tour_event.published is True

    company_tour_event.unpublish_event()
    await db_session.commit()
    await db_session.refresh(company_tour_event)
    assert company_tour_event.published is False

@pytest.mark.asyncio
async def test_event_validate_dates(db_session: AsyncSession, verified_user):
    with pytest.raises(ValueError):
        event = Event(
            title="Invalid Event",
            description="Event with invalid dates",
            start_datetime=datetime.now() + timedelta(hours=2),
            end_datetime=datetime.now(),
            published=False,
            event_type=EventType.COMPANY_TOUR,
            creator=verified_user,
        )
        event.validate_event_dates()

@pytest.mark.asyncio
async def test_user_deletion_cascades_to_events(db_session: AsyncSession, user_with_events):
    await db_session.delete(user_with_events)
    await db_session.commit()

    event_count = await db_session.scalar(select(func.count(Event.id)))
    assert event_count == 0