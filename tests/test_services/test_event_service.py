import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from app.models.models import User, Event
from app.services.event_service import create_event, get_event, get_events, update_event, delete_event
from app.services.user_service import create_user
# Adjust the following import based on your actual User model location

@pytest.mark.asyncio
async def test_create_event(db_session, sample_event_data):
    event = await create_event(db_session, **sample_event_data)
    assert event.id is not None
    assert event.title == sample_event_data['title']

@pytest.mark.asyncio
async def test_get_event(db_session, sample_event_data):
    created_event = await create_event(db_session, **sample_event_data)
    retrieved_event = await get_event(db_session, created_event.id)
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == created_event.title

@pytest.mark.asyncio
async def test_get_events(db_session, sample_event_data):
    await create_event(db_session, **sample_event_data)
    await create_event(db_session, **{**sample_event_data, "title": "Another Event"})
    events = await get_events(db_session)  # Adjusted to directly receive returned events list
    assert len(events) >= 2

@pytest.mark.asyncio
async def test_update_event(db_session, sample_event_data):
    event = await create_event(db_session, **sample_event_data)
    updated_title = "Updated Event Title"
    updated_event = await update_event(db_session, event.id, title=updated_title)
    assert updated_event.title == updated_title

@pytest.mark.asyncio
async def test_delete_event(db_session, sample_event_data):
    event = await create_event(db_session, **sample_event_data)
    result = await delete_event(db_session, event.id)
    assert result is True
    deleted_event = await get_event(db_session, event.id)
    assert deleted_event is None
