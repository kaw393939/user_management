from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint
from typing import Dict, List, Optional
from datetime import datetime

class QRCodeRequest(BaseModel):
    url: HttpUrl = Field(..., description="The URL to encode into the QR code.")
    fill_color: str = Field(default="red", description="Color of the QR code.", example="black")
    back_color: str = Field(default="white", description="Background color of the QR code.", example="yellow")
    size: conint(ge=1, le=40) = Field(default=10, description="Size of the QR code from 1 to 40.", example=20) # type: ignore

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "fill_color": "black",
                "back_color": "yellow",
                "size": 20
            }
        }

class Link(BaseModel):
    rel: str = Field(..., description="Relation type of the link.")
    href: HttpUrl = Field(..., description="The URL of the link.")
    action: str = Field(..., description="HTTP method for the action this link represents.")
    type: str = Field(default="application/json", description="Content type of the response for this link.")

    class Config:
        json_schema_extra = {
            "example": {
                "rel": "self",
                "href": "https://api.example.com/qr/123",
                "action": "GET",
                "type": "application/json"
            }
        }

class QRCodeResponse(BaseModel):
    message: str = Field(..., description="A message related to the QR code request.")
    qr_code_url: HttpUrl = Field(..., description="The URL to the generated QR code.")
    links: List[Link] = Field(default=[], description="HATEOAS links related to the QR code.")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "QR code created successfully.",
                "qr_code_url": "https://api.example.com/qr/123",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://api.example.com/qr/123",
                        "action": "GET",
                        "type": "application/json"
                    }
                ]
            }
        }

class Token(BaseModel):
    access_token: str = Field(..., description="The access token for authentication.")
    token_type: str = Field(default="bearer", description="The type of the token.")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "jhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    username: Optional[str] = Field(None, description="The username that the token represents.")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com"
            }
        }

class EventBase(BaseModel):
    title: str = Field(..., description="Title of the event.")
    description: str = Field(..., description="Description of the event.")

class EventCreate(EventBase):
    start_date: datetime = Field(..., description="Start date and time of the event.")
    end_date: datetime = Field(..., description="End date and time of the event.")

class Event(EventBase):
    id: int = Field(..., description="Unique identifier of the event.")
    start_date: datetime
    end_date: datetime
    links: List[Link] = Field(default=[], description="HATEOAS links related to this event.")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Sample Event",
                "description": "This is a sample event.",
                "start_date": "2024-01-01T09:00:00",
                "end_date": "2024-01-01T17:00:00",
                "links": [
                    {
                        "rel": "self",
                        "href": "https://api.example.com/events/1",
                        "action": "GET",
                        "type": "application/json"
                    },
                    {
                        "rel": "update",
                        "href": "https://api.example.com/events/1",
                        "action": "PUT",
                        "type": "application/json"
                    },
                    {
                        "rel": "delete",
                        "href": "https://api.example.com/events/1",
                        "action": "DELETE",
                        "type": "application/json"
                    }
                ]
            }
        }

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title of the event.")
    description: Optional[str] = Field(None, description="Updated description of the event.")
    start_date: Optional[datetime] = Field(None, description="Updated start date and time of the event.")
    end_date: Optional[datetime] = Field(None, description="Updated end date and time of the event.")

    class Config:
        from_attributes = True

class Pagination(BaseModel):
    page: int = Field(..., description="Current page number.")
    per_page: int = Field(..., description="Number of items per page.")
    total_items: int = Field(..., description="Total number of items.")
    total_pages: int = Field(..., description="Total number of pages.")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "per_page": 10,
                "total_items": 50,
                "total_pages": 5
            }
        }

class EventList(BaseModel):
    items: List[Event]  # Your EventResponse model
    pagination: Pagination  # Your Pagination model
    links: List[Link] = Field(..., alias='_links')  # Use alias for the external representation



    class Config:
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
            "example": {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "title": "Sample Event",
                        "description": "This is a sample event.",
                        "start_date": "2024-01-01T09:00:00",
                        "end_date": "2024-01-01T17:00:00",
                        "links": [
                            {
                                "rel": "self",
                                "href": "https://api.example.com/events/1",
                                "action": "GET",
                                "type": "application/json"
                            }
                        ]
                    }
                ],
                "pagination": {
                    "page": 1,
                    "per_page": 10,
                    "total_items": 50,
                    "total_pages": 5
                },
                "links": [
                    {
                        "rel": "self",
                        "href": "https://api.example.com/events?page=1&per_page=10",
                        "action": "GET",
                        "type": "application/json"
                    },
                    {
                        "rel": "next",
                        "href": "https://api.example.com/events?page=2&per_page=10",
                        "action": "GET",
                        "type": "application/json"
                    },
                    {
                        "rel": "last",
                        "href": "https://api.example.com/events?page=5&per_page=10",
                        "action": "GET",
                        "type": "application/json"
                    }
                ]
            }
        }
    }
        
class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Custom Validators
def validate_username(username: str) -> str:
    if not re.match(r"^\w+$", username):
        raise ValueError('Username must be alphanumeric')
    return username

def validate_password(password: str) -> str:
    pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )
    if not pattern.match(password):
        raise ValueError(
            'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character')
    return password

# User Models
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr

    _validate_username = validator('username', allow_reuse=True)(validate_username)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    _validate_password = validator('password', allow_reuse=True)(validate_password)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=8)
    profile_picture_url: Optional[HttpUrl]

    _username_validator = validator('username', allow_reuse=True)(validate_username)
    _password_validator = validator('password', allow_reuse=True)(validate_password)

class UserResponse(UserBase):
    id: UUID
    profile_picture_url: Optional[HttpUrl]
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime