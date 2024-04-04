import pytest
from app.services.event_service import create_event, get_event, get_events, update_event, delete_event
from app.services.user_service import create_user  # Assuming you have this service
from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from app.database import Base  # Adjust this import as necessary

# Your test functions remain largely unchanged, but now they correctly use a valid creator_id
def test_create_event(db_session, sample_event_data):
    event = create_event(db_session, **sample_event_data)
    assert event.id is not None
    assert event.title == sample_event_data['title']
    assert event.creator_id == sample_event_data['creator_id']

def test_get_event(db_session, sample_event_data):
    created_event = create_event(db_session, **sample_event_data)
    retrieved_event = get_event(db_session, created_event.id)
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == created_event.title

def test_get_events(db_session, sample_event_data):
    create_event(db_session, **sample_event_data)
    another_event_data = sample_event_data.copy()
    another_event_data["title"] = "Another Event"
    create_event(db_session, **another_event_data)
    events, total = get_events(db_session)
    assert len(events) >= 2
    assert total >= 2

def test_update_event(db_session, sample_event_data):
    event = create_event(db_session, **sample_event_data)
    updated_title = "Updated Event Title"
    updated_description = "Updated Description"
    update_event(db_session, event.id, title=updated_title, description=updated_description)
    updated_event = get_event(db_session, event.id)
    assert updated_event.title == updated_title
    assert updated_event.description == updated_description

def test_delete_event(db_session, sample_event_data):
    event = create_event(db_session, **sample_event_data)
    delete_event(db_session, event.id)
    deleted_event = get_event(db_session, event.id)
    assert deleted_event is None
