import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from app.models.models import User
from app.services.event_service import create_event, get_event, get_events, update_event, delete_event
from app.services.user_service import create_user
# Adjust the following import based on your actual User model location

@pytest.fixture(scope="function")
def user(db_session):
    # Mock user data according to the User model fields
    user_data = {
        "username": "test_user_" + str(uuid4()),  # Ensure unique username
        "email": "test_user_" + str(uuid4()) + "@example.com",  # Ensure unique email
        "hashed_password": "fake_hashed_password"  # Assuming you have a mechanism to hash the password
    }
    # Directly instantiate and add the User model to the session to bypass any custom logic in create_user
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()  # Make sure to commit so the user is saved in the DB
    return user

@pytest.fixture(scope="function")
def sample_event_data(user):
    return {
        "creator_id": user.id,  # Use the created user's ID as the creator_id for the event
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "qr_code_path": None,  # Assuming no QR code for the basic test
    }

def test_create_event(db_session, sample_event_data):
    event = create_event(db_session, **sample_event_data)
    assert event.id is not None
    assert event.title == sample_event_data['title']

def test_get_event(db_session, sample_event_data):
    created_event = create_event(db_session, **sample_event_data)
    retrieved_event = get_event(db_session, created_event.id)
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == created_event.title

def test_get_events(db_session, sample_event_data):
    create_event(db_session, **sample_event_data)
    create_event(db_session, **{**sample_event_data, "title": "Another Event"})
    events, total = get_events(db_session)  # Adjusted to unpack returned tuple
    assert len(events) >= 2
    assert total >= 2  # Ensure total count is consistent with the number of created events

def test_update_event(db_session, sample_event_data):
    event = create_event(db_session, **sample_event_data)
    updated_title = "Updated Event Title"
    update_event(db_session, event.id, title=updated_title)
    updated_event = get_event(db_session, event.id)
    assert updated_event.title == updated_title

def test_delete_event(db_session, sample_event_data):
    event = create_event(db_session, **sample_event_data)
    delete_event(db_session, event.id)
    deleted_event = get_event(db_session, event.id)
    assert deleted_event is None
