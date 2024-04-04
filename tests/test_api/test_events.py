import pytest
from uuid import uuid4
from app.services.event_service import create_event, get_event, get_events, update_event, delete_event

@pytest.fixture(scope="function")
def sample_event_data(creator_id):
    # Mock a creator_id passed from another fixture or setup
    return {
        "creator_id": creator_id,
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "qr_code_path": None,  # Assuming no QR code for the basic test setup
    }

@pytest.fixture(scope="session")
def creator_id():
    return uuid4()  # This would represent the UUID of a user in your system

def test_create_event(db_session, sample_event_data):
    # Create a new event using the sample data
    event = create_event(db_session, **sample_event_data)
    assert event.id is not None
    assert event.title == sample_event_data['title']
    assert event.creator_id == sample_event_data['creator_id']

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
    another_event_data = sample_event_data.copy()
    another_event_data["title"] = "Another Event"
    create_event(db_session, **another_event_data)
    # Retrieve all events
    events, total = get_events(db_session)
    assert len(events) >= 2
    assert total >= 2

def test_update_event(db_session, sample_event_data):
    # Create a new event
    event = create_event(db_session, **sample_event_data)
    # Update the event
    updated_title = "Updated Event Title"
    updated_description = "Updated Description"
    update_event(db_session, event.id, title=updated_title, description=updated_description)
    # Retrieve the updated event
    updated_event = get_event(db_session, event.id)
    assert updated_event.title == updated_title
    assert updated_event.description == updated_description

def test_delete_event(db_session, sample_event_data):
    # Create a new event
    event = create_event(db_session, **sample_event_data)
    # Delete the event
    delete_event(db_session, event.id)
    # Try to retrieve the deleted event
    deleted_event = get_event(db_session, event.id)
    assert deleted_event is None
