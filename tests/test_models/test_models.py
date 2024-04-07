import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from app.models.models import (
    Event, EventApproval, EventRegistration,
    EventReview, EventSection, Notification
)
from app.models.user_model import User

pytestmark = pytest.mark.asyncio


# Event Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_event(db_session, user):
    event_data = {
        "creator_id": user.id,
        "title": "Test Event",
        "description": "A test event",
        "location": "Test Location",
        "status": "pending",
        "is_public": True
    }
    event = Event(**event_data)
    db_session.add(event)
    await db_session.commit()

    assert event.id is not None

    # Test deletion
    await db_session.delete(event)
    await db_session.commit()

    deleted_event = await db_session.get(Event, event.id)
    assert deleted_event is None

# Event Section Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_event_section(db_session, event):
    section_data = {
        "event_id": event.id,
        "title": "Test Section",
        "start_date": datetime.utcnow(),
        "end_date": datetime.utcnow() + timedelta(hours=2),
        "location": "Test Section Location",
        "capacity": 100
    }
    section = EventSection(**section_data)
    db_session.add(section)
    await db_session.commit()

    assert section.id is not None

    # Test deletion
    await db_session.delete(section)
    await db_session.commit()

    deleted_section = await db_session.get(EventSection, section.id)
    assert deleted_section is None

# Event Approval Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_event_approval(db_session, event, user):
    approval_data = {
        "event_id": event.id,
        "approved": True,
        "reviewed_by_id": user.id,
        "reviewed_at": datetime.utcnow()
    }
    approval = EventApproval(**approval_data)
    db_session.add(approval)
    await db_session.commit()

    assert approval.id is not None

    # Test deletion
    await db_session.delete(approval)
    await db_session.commit()

    deleted_approval = await db_session.get(EventApproval, approval.id)
    assert deleted_approval is None

# Event Review Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_event_review(db_session, event, event_section, user):
    review_data = {
        "event_id": event.id,
        "event_section_id": event_section.id,
        "reviewer_id": user.id,
        "rating": 4,
        "comment": "Test review comment"
    }
    review = EventReview(**review_data)
    db_session.add(review)
    await db_session.commit()

    assert review.id is not None

    # Test deletion
    await db_session.delete(review)
    await db_session.commit()

    deleted_review = await db_session.get(EventReview, review.id)
    assert deleted_review is None

# Event Registration Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_event_registration(db_session, user, event_section):
    registration_data = {
        "user_id": user.id,
        "event_section_id": event_section.id,
        "attended": True,
        "attended_time": datetime.utcnow()
    }
    registration = EventRegistration(**registration_data)
    db_session.add(registration)
    await db_session.commit()

    assert registration.id is not None

    # Test deletion
    await db_session.delete(registration)
    await db_session.commit()

    deleted_registration = await db_session.get(EventRegistration, registration.id)
    assert deleted_registration is None

# Notification Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_notification(db_session, user, event):
    notification_data = {
        "user_id": user.id,
        "event_id": event.id,
        "message": "Test notification message"
    }
    notification = Notification(**notification_data)
    db_session.add(notification)
    await db_session.commit()

    assert notification.id is not None

    # Test deletion
    await db_session.delete(notification)
    await db_session.commit()

    deleted_notification = await db_session.get(Notification, notification.id)
    assert deleted_notification is None

@pytest.mark.asyncio
async def test_create_user_with_invalid_data(db_session):
    user_data = {
        "username": "",  # Invalid data: username cannot be empty
        "email": "invalid_email@example.com",
        "hashed_password": "fake_hashed_password",
    }
    user = User(**user_data)
    db_session.add(user)
    
    with pytest.raises(IntegrityError):
        await db_session.commit()

@pytest.mark.asyncio
async def test_cascade_delete_event_deletes_sections(db_session, event):
    # Assuming `event` fixture creates an event with one or more associated sections
    event_id = event.id
    
    await db_session.delete(event)
    await db_session.commit()

    # Verify the event is deleted
    deleted_event = await db_session.get(Event, event_id)
    assert deleted_event is None
    
    # Verify related event sections are also deleted
    related_sections = await db_session.execute(select(EventSection).where(EventSection.event_id == event_id))
    assert related_sections.scalars().first() is None


