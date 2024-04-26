from builtins import len
import logging
import pytest
from sqlalchemy import select
from app.models.user_model import Event, EventType, User
from app.services.event_service import EventService
from uuid import UUID

pytestmark = pytest.mark.asyncio
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

# Test creating an event with valid data
async def test_create_event_with_valid_data(db_session, verified_user):
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "start_datetime": "2023-06-01T10:00:00",
        "end_datetime": "2023-06-01T12:00:00",
        "published": False,
        "event_type": EventType.COMPANY_TOUR,
        "creator_id": verified_user.id  # Add this line
    }
    
    event = await EventService.create(db_session, event_data)

    assert event is not None
    assert event.title == event_data["title"]
    assert event.description == event_data["description"]
    assert event.creator_id == verified_user.id
    
# Test creating an event with invalid data
async def test_create_event_with_invalid_data(db_session):
    event_data = {
        "title": "",  # Invalid empty title
        "start_datetime": "2023-06-01T10:00:00",
        "end_datetime": "2023-06-01T09:00:00",  # Invalid end_datetime before start_datetime
        "published": False,
        "event_type": "INVALID_EVENT_TYPE"  # Invalid event_type
    }
    event = await EventService.create(db_session, event_data)
    assert event is None

# Test fetching an event by ID when the event exists
async def test_get_by_id_event_exists(db_session, company_tour_event):
    retrieved_event = await EventService.get_by_id(db_session, company_tour_event.id)
    assert retrieved_event is not None
    assert retrieved_event.id == company_tour_event.id

# Test fetching an event by ID when the event does not exist
async def test_get_by_id_event_does_not_exist(db_session):
    non_existent_event_id = UUID("00000000-0000-0000-0000-000000000000")
    retrieved_event = await EventService.get_by_id(db_session, non_existent_event_id)
    assert retrieved_event is None

# Test fetching an event by title when the event exists
async def test_get_by_title_event_exists(db_session, company_tour_event):
    retrieved_event = await EventService.get_by_title(db_session, company_tour_event.title)
    assert retrieved_event is not None
    assert retrieved_event.title == company_tour_event.title

# Test fetching an event by title when the event does not exist
async def test_get_by_title_event_does_not_exist(db_session):
    retrieved_event = await EventService.get_by_title(db_session, "Non-existent Event")
    assert retrieved_event is None

# Test updating an event with valid data
async def test_update_event_valid_data(db_session, company_tour_event):
    update_data = {
        "title": "Updated Company Tour",
        "description": "An updated description of the company tour"
    }
    updated_event = await EventService.update(db_session, company_tour_event.id, update_data)
    assert updated_event is not None
    assert updated_event.title == update_data["title"]
    assert updated_event.description == update_data["description"]

# Test updating an event with invalid data
async def test_update_event_invalid_data(db_session, company_tour_event):
    update_data = {
        "title": "",  # Invalid empty title
        "end_datetime": "2023-06-01T09:00:00"  # Invalid end_datetime before start_datetime
    }
    updated_event = await EventService.update(db_session, company_tour_event.id, update_data)
    assert updated_event is None

# Test deleting an event that exists
async def test_delete_event_exists(db_session, company_tour_event):
    deletion_success = await EventService.delete(db_session, company_tour_event.id)
    assert deletion_success is True

# Test attempting to delete an event that does not exist
async def test_delete_event_does_not_exist(db_session):
    non_existent_event_id = UUID("00000000-0000-0000-0000-000000000000")
    deletion_success = await EventService.delete(db_session, non_existent_event_id)
    assert deletion_success is False

# Test listing events with pagination
async def test_list_events_with_pagination(db_session, company_tour_event, mock_interview_event, guest_lecture_event):
    events_page_1 = await EventService.list_events(db_session, skip=0, limit=2)
    events_page_2 = await EventService.list_events(db_session, skip=2, limit=2)
    assert len(events_page_1) == 2
    assert len(events_page_2) == 1
    assert events_page_1[0].id != events_page_2[0].id

# Test publishing an event
async def test_publish_event(db_session, company_tour_event):
    assert company_tour_event.published is False
    published_event = await EventService.publish_event(db_session, company_tour_event.id)
    assert published_event is not None
    assert published_event.published is True

# Test unpublishing an event
async def test_unpublish_event(db_session, mock_interview_event):
    mock_interview_event.published = True
    await db_session.commit()
    unpublished_event = await EventService.unpublish_event(db_session, mock_interview_event.id)
    assert unpublished_event is not None
    assert unpublished_event.published is False

# Test listing events by creator
async def test_list_events_by_creator(db_session, verified_user, manager_user, company_tour_event, mock_interview_event):
    events_by_verified_user = await EventService.list_events_by_creator(db_session, verified_user.id)
    events_by_manager_user = await EventService.list_events_by_creator(db_session, manager_user.id)
    assert len(events_by_verified_user) == 2  # Update this line
    assert len(events_by_manager_user) == 0

# Test listing published events
async def test_list_published_events(db_session, company_tour_event, mock_interview_event):
    mock_interview_event.published = True
    await db_session.commit()
    published_events = await EventService.list_published_events(db_session)
    assert len(published_events) == 1
    assert published_events[0].id == mock_interview_event.id

# Test listing events by type
async def test_list_events_by_type(db_session, company_tour_event, mock_interview_event, guest_lecture_event):
    company_tour_events = await EventService.list_events_by_type(db_session, EventType.COMPANY_TOUR)
    mock_interview_events = await EventService.list_events_by_type(db_session, EventType.MOCK_INTERVIEW)
    guest_lecture_events = await EventService.list_events_by_type(db_session, EventType.GUEST_LECTURE)
    assert len(company_tour_events) == 1
    assert len(mock_interview_events) == 1
    assert len(guest_lecture_events) == 1

# Test counting events
async def test_count_events(db_session, company_tour_event, mock_interview_event, guest_lecture_event):
    event_count = await EventService.count_events(db_session)
    assert event_count == 3