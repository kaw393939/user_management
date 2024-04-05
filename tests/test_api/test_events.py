import pytest
from httpx import AsyncClient
from sqlalchemy import select
from app.models.models import Event

@pytest.mark.asyncio
async def test_create_event(client, user, sample_event_data):
    response = await client.post("/events/", json=sample_event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_event_data["title"]
    assert data["creator_id"] == str(user.id)  # Assuming JSON returns stringified UUID

@pytest.mark.asyncio
async def test_get_event(client, db_session, user, sample_event_data):
    # First, create an event to ensure there's one to get
    response = await client.post("/events/", json=sample_event_data)
    assert response.status_code == 200
    event_id = response.json()["id"]

    # Now, try to retrieve the created event
    get_response = await client.get(f"/events/{event_id}")
    assert get_response.status_code == 200
    event_data = get_response.json()
    assert event_data["id"] == event_id
    assert event_data["title"] == sample_event_data["title"]

@pytest.mark.asyncio
async def test_get_events(client, db_session, sample_event_data):
    # Create multiple events
    await client.post("/events/", json=sample_event_data)
    another_event_data = sample_event_data.copy()
    another_event_data["title"] = "Another Sample Event"
    await client.post("/events/", json=another_event_data)

    # Get the list of events
    response = await client.get("/events/")
    assert response.status_code == 200
    events = response.json()
    assert len(events) >= 2

@pytest.mark.asyncio
async def test_update_event(client, db_session, user, sample_event_data):
    # Create an event
    create_response = await client.post("/events/", json=sample_event_data)
    event_id = create_response.json()["id"]

    # Update the event
    updated_data = {"title": "Updated Title", "description": "Updated Description"}
    update_response = await client.put(f"/events/{event_id}", json=updated_data)
    assert update_response.status_code == 200

    # Verify update
    get_response = await client.get(f"/events/{event_id}")
    event_data = get_response.json()
    assert event_data["title"] == "Updated Title"
    assert event_data["description"] == "Updated Description"

@pytest.mark.asyncio
async def test_delete_event(client, db_session, user, sample_event_data):
    # Create an event to delete
    create_response = await client.post("/events/", json=sample_event_data)
    event_id = create_response.json()["id"]

    # Delete the event
    delete_response = await client.delete(f"/events/{event_id}")
    assert delete_response.status_code == 200

    # Verify deletion
    get_response = await client.get(f"/events/{event_id}")
    assert get_response.status_code == 404
