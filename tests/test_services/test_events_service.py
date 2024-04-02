import pytest
from datetime import datetime, timedelta
from app.services.events_service import create_event, get_event, get_events, update_event, delete_event
from app.models import Event

@pytest.fixture(scope="function")
def sample_event_data():
    return {
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=1),
    }

def test_create_event(db_session, sample_event_data):
    # Create a new event using the sample data
    event = create_event(db_session, **sample_event_data)
    assert event.id is not None
    assert event.title == sample_event_data['title']

def test_get_event(db_session, sample_event_data):
    # First, create a new event
    created_event = create_event(db_session, **sample_event_data)
    # Retrieve the event by ID
    retrieved_event = get_event(db_session, created_event.id)
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == created_event.title

def test_get_events(db_session, sample_event_data):
    # Create multiple events
    create_event(db_session, **sample_event_data)
    create_event(db_session, **{**sample_event_data, "title": "Another Event"})
    # Retrieve all events
    events = get_events(db_session)
    assert len(events) >= 2

def test_update_event(db_session, sample_event_data):
    # Create a new event
    event = create_event(db_session, **sample_event_data)
    # Update the event
    updated_title = "Updated Event Title"
    update_event(db_session, event.id, title=updated_title)
    # Retrieve the updated event
    updated_event = get_event(db_session, event.id)
    assert updated_event.title == updated_title

def test_delete_event(db_session, sample_event_data):
    # Create a new event
    event = create_event(db_session, **sample_event_data)
    # Delete the event
    delete_event(db_session, event.id)
    # Try to retrieve the deleted event
    deleted_event = get_event(db_session, event.id)
    assert deleted_event is None
