import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta
from app.schemas.event_schema import EventBase, EventCreate, EventUpdate, EventResponse, EventListResponse
from app.models.user_model import EventType

# Fixtures for common test data
@pytest.fixture
def event_base_data():
    return {
        "title": "Company Tour",
        "description": "A tour of our company's facilities.",
        "start_datetime": datetime.now(),
        "end_datetime": datetime.now() + timedelta(hours=2),
        "published": False,
        "event_type": EventType.COMPANY_TOUR
    }

@pytest.fixture
def event_create_data(event_base_data, verified_user):
    event_base_data["creator_id"] = verified_user.id
    return event_base_data

@pytest.fixture
def event_update_data():
    return {
        "title": "Updated Company Tour",
        "description": "An updated description of the company tour.",
        "start_datetime": datetime.now() + timedelta(days=1),
        "end_datetime": datetime.now() + timedelta(days=1, hours=2),
        "published": True,
        "event_type": EventType.GUEST_LECTURE
    }

@pytest.fixture
def event_response_data(event_base_data):
    return {
        "id": uuid.uuid4(),
        "creator_id": uuid.uuid4(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "links": [
            {"rel": "self", "href": f"/events/{uuid.uuid4()}"},
            {"rel": "creator", "href": f"/users/{uuid.uuid4()}"}
        ],
        **event_base_data
    }

# Tests for EventBase
def test_event_base_valid(event_base_data):
    event = EventBase(**event_base_data)
    assert event.title == event_base_data["title"]
    assert event.description == event_base_data["description"]
    assert event.start_datetime == event_base_data["start_datetime"]
    assert event.end_datetime == event_base_data["end_datetime"]
    assert event.published == event_base_data["published"]
    assert event.event_type == event_base_data["event_type"]

def test_event_base_invalid_end_datetime(event_base_data):
    event_base_data["end_datetime"] = event_base_data["start_datetime"] - timedelta(hours=1)
    with pytest.raises(ValidationError):
        EventBase(**event_base_data)

# Tests for EventCreate
def test_event_create_valid(event_create_data):
    event_create = EventCreate(**event_create_data)
    assert event_create.title == event_create_data["title"]
    assert event_create.description == event_create_data["description"]
    assert event_create.start_datetime == event_create_data["start_datetime"]
    assert event_create.end_datetime == event_create_data["end_datetime"]
    assert event_create.published == event_create_data["published"]
    assert event_create.event_type == event_create_data["event_type"]

# Tests for EventUpdate
def test_event_update_valid(event_update_data):
    event_update = EventUpdate(**event_update_data)
    assert event_update.title == event_update_data["title"]
    assert event_update.description == event_update_data["description"]
    assert event_update.start_datetime == event_update_data["start_datetime"]
    assert event_update.end_datetime == event_update_data["end_datetime"]
    assert event_update.published == event_update_data["published"]
    assert event_update.event_type == event_update_data["event_type"]

# Tests for EventResponse
def test_event_response_valid(event_response_data):
    event_response = EventResponse(**event_response_data)
    assert event_response.id == event_response_data["id"]
    assert event_response.title == event_response_data["title"]
    assert event_response.description == event_response_data["description"]
    assert event_response.start_datetime == event_response_data["start_datetime"]
    assert event_response.end_datetime == event_response_data["end_datetime"]
    assert event_response.published == event_response_data["published"]
    assert event_response.event_type == event_response_data["event_type"]
    assert event_response.creator_id == event_response_data["creator_id"]
    assert event_response.created_at == event_response_data["created_at"]
    assert event_response.updated_at == event_response_data["updated_at"]
    assert event_response.links == event_response_data["links"]

# Tests for EventListResponse
def test_event_list_response_valid(event_response_data):
    event_list_response_data = {
        "items": [event_response_data],
        "total": 1,
        "page": 1,
        "size": 10,
        "links": [
            {"rel": "self", "href": "/events?page=1&size=10"},
            {"rel": "next", "href": None},
            {"rel": "prev", "href": None},
            {"rel": "first", "href": "/events?page=1&size=10"},
            {"rel": "last", "href": "/events?page=1&size=10"}
        ]
    }
    event_list_response = EventListResponse(**event_list_response_data)
    assert event_list_response.items[0].id == event_response_data["id"]
    assert event_list_response.total == event_list_response_data["total"]
    assert event_list_response.page == event_list_response_data["page"]
    assert event_list_response.size == event_list_response_data["size"]
    assert event_list_response.links == event_list_response_data["links"]