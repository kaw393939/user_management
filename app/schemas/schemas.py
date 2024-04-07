import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint

# QR Code Models
class QRCodeRequest(BaseModel):
    url: HttpUrl = Field(..., description="The URL to encode into the QR code.")
    fill_color: str = Field(default="red", description="Color of the QR code.", example="black")
    back_color: str = Field(default="white", description="Background color of the QR code.", example="yellow")
    size: conint(ge=1, le=40) = Field(default=10, description="Size of the QR code from 1 to 40.", example=20)

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "fill_color": "black",
                "back_color": "yellow",
                "size": 20
            }
        }

class QRCodeResponse(BaseModel):
    message: str = Field(..., description="A message related to the QR code request.")
    qr_code_url: HttpUrl = Field(..., description="The URL to the generated QR code.")
    links: List['Link'] = Field(default=[], description="HATEOAS links related to the QR code.")

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

# Link Model
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

# Pagination Model
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

# Token Models
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

# Event Models
class EventBase(BaseModel):
    title: str = Field(..., description="Title of the event.")
    description: str = Field(..., description="Description of the event.")
    status: str = Field("pending", description="Current status of the event.")
    is_public: bool = Field(True, description="Indicates if the event is public.")

class EventCreate(EventBase):
   pass

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    id: UUID = Field(..., description="Unique identifier of the event.")
    creator_id: UUID = Field(..., description="Unique identifier of the user who created the event.")
    location: Optional[str] = Field(None, description="Location of the event.")
    qr_code_path: Optional[str] = Field(None, description="Path to the QR code image for the event.")
    created_at: datetime
    updated_at: datetime
    links: List[Link] = Field(default=[], description="HATEOAS links related to this event.")

class EventList(BaseModel):
    items: List[EventResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True

# Tag Models
class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the tag")

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagResponse(TagBase):
    id: UUID = Field(..., description="Unique identifier of the tag")

class TagList(BaseModel):
    items: List[TagResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True

# Event Section Models
class EventSectionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the event section")
    start_date: datetime = Field(..., description="Start date and time of the event section")
    end_date: datetime = Field(..., description="End date and time of the event section")
    location: Optional[str] = Field(None, description="Location of the event section")
    capacity: int = Field(..., gt=0, description="Capacity of the event section")
    registration_deadline: Optional[datetime] = Field(None, description="Registration deadline for the event section")
    additional_info: Optional[str] = Field(None, description="Additional information about the event section")

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be greater than or equal to start date')
        return v

class EventSectionCreate(EventSectionBase):
    pass

class EventSectionUpdate(EventSectionBase):
    pass

class EventSectionResponse(EventSectionBase):
    id: UUID = Field(..., description="Unique identifier of the event section")
    event_id: UUID = Field(..., description="Unique identifier of the event")
    qr_code_path: Optional[str] = Field(None, description="Path to the QR code image for the event section.")
    links: List[Link] = Field(default=[], description="HATEOAS links related to the event section")

class EventSectionList(BaseModel):
    items: List[EventSectionResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True

# Event Approval Models
class EventApprovalBase(BaseModel):
    approved: bool = Field(False, description="Indicates if the event is approved")
    approval_reason: Optional[str] = Field(None, description="Reason for approving the event")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejecting the event")
    submitted_at: datetime = Field(..., description="Timestamp of when the event was submitted for approval")
    reviewed_at: Optional[datetime] = Field(None, description="Timestamp of when the event was reviewed")

class EventApprovalCreate(EventApprovalBase):
    pass

class EventApprovalUpdate(EventApprovalBase):
    pass

class EventApprovalResponse(EventApprovalBase):
    id: UUID = Field(..., description="Unique identifier of the event approval")
    event_id: UUID = Field(..., description="Unique identifier of the event")
    reviewed_by_id: Optional[UUID] = Field(None, description="Unique identifier of the user who reviewed the event")

class EventApprovalList(BaseModel):
    items: List[EventApprovalResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True

# Event Review Models
class EventReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating given to the event or section")
    comment: Optional[str] = Field(None, description="Comment associated with the review")

class EventReviewCreate(EventReviewBase):
    pass

class EventReviewUpdate(EventReviewBase):
    pass

class EventReviewResponse(EventReviewBase):
    id: UUID = Field(..., description="Unique identifier of the event review")
    event_id: UUID = Field(..., description="Unique identifier of the event")
    event_section_id: Optional[UUID] = Field(None, description="Unique identifier of the event section")
    reviewer_id: UUID = Field(..., description="Unique identifier of the user who provided the review")
    created_at: datetime = Field(..., description="Timestamp of when the review was created")

class EventReviewList(BaseModel):
    items: List[EventReviewResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True

# Event Registration Models
class EventRegistrationBase(BaseModel):
    attended: bool = Field(False, description="Indicates if the user attended the event section")
    attended_time: Optional[datetime] = Field(None, description="Timestamp of when the user attended the event section")

class EventRegistrationCreate(EventRegistrationBase):
    pass

class EventRegistrationUpdate(EventRegistrationBase):
    pass

class EventRegistrationResponse(EventRegistrationBase):
    id: UUID = Field(..., description="Unique identifier of the event registration")
    user_id: UUID = Field(..., description="Unique identifier of the user")
    event_section_id: UUID = Field(..., description="Unique identifier of the event section")
    registered_at: datetime = Field(..., description="Timestamp of when the user registered for the event section")

class EventRegistrationList(BaseModel):
    items: List[EventRegistrationResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True

# Notification Models
class NotificationBase(BaseModel):
    message: str = Field(..., description="Notification message")

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: UUID = Field(..., description="Unique identifier of the notification")
    user_id: UUID = Field(..., description="Unique identifier of the user")
    event_id: UUID = Field(..., description="Unique identifier of the event")
    created_at: datetime = Field(..., description="Timestamp of when the notification was created")

class NotificationList(BaseModel):
    items: List[NotificationResponse]
    pagination: Pagination
    links: List[Link] = Field(..., alias="_links")

    class Config:
        from_attributes = True
        populate_by_name = True