from builtins import ValueError, bool, dict, int, str
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
from app.models.user_model import EventType

class EventBase(BaseModel):
    title: str = Field(..., example="Company Tour", min_length=1)
    description: Optional[str] = Field(None, example="A tour of our company's facilities.")
    start_datetime: datetime = Field(..., example="2023-06-01T10:00:00")
    end_datetime: datetime = Field(..., example="2023-06-01T12:00:00")
    published: bool = Field(default=False, example=True)
    event_type: EventType = Field(..., example=EventType.COMPANY_TOUR)

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Title must not be empty")
        return v

    @validator('end_datetime')
    def validate_end_datetime(cls, end_datetime, values):
        start_datetime = values.get('start_datetime')
        if start_datetime and end_datetime < start_datetime:
            raise ValueError("End datetime must be after start datetime.")
        return end_datetime

class EventCreate(EventBase):
    creator_id: uuid.UUID = Field(..., example=uuid.uuid4())
    pass

class EventUpdate(EventBase):
    title: Optional[str] = Field(None, example="Updated Company Tour")
    description: Optional[str] = Field(None, example="An updated description of the company tour.")
    start_datetime: Optional[datetime] = Field(None, example="2023-06-02T10:00:00")
    end_datetime: Optional[datetime] = Field(None, example="2023-06-02T12:00:00")
    published: Optional[bool] = Field(None, example=False)
    event_type: Optional[EventType] = Field(None, example=EventType.GUEST_LECTURE)

class EventResponse(EventBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    creator_id: uuid.UUID = Field(..., example=uuid.uuid4())
    created_at: datetime = Field(..., example="2023-05-30T09:00:00")
    updated_at: datetime = Field(..., example="2023-05-30T09:00:00")
    links: List[dict] = Field([], example=[
        {"rel": "self", "href": "/events/{id}"},
        {"rel": "creator", "href": "/users/{creator_id}"}
    ])

class EventListResponse(BaseModel):
    items: List[EventResponse] = Field(..., example=[{
        "id": uuid.uuid4(),
        "title": "Company Tour",
        "description": "A tour of our company's facilities.",
        "start_datetime": "2023-06-01T10:00:00",
        "end_datetime": "2023-06-01T12:00:00",
        "published": True,
        "event_type": EventType.COMPANY_TOUR,
        "creator_id": uuid.uuid4(),
        "created_at": "2023-05-30T09:00:00",
        "updated_at": "2023-05-30T09:00:00",
        "links": [
            {"rel": "self", "href": "/events/{id}"},
            {"rel": "creator", "href": "/users/{creator_id}"}
        ]
    }])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
    links: List[dict] = Field([], example=[
        {"rel": "self", "href": "/events?page=1&size=10"},
        {"rel": "next", "href": "/events?page=2&size=10"},
        {"rel": "prev", "href": None},
        {"rel": "first", "href": "/events?page=1&size=10"},
        {"rel": "last", "href": "/events?page=10&size=10"}
    ])