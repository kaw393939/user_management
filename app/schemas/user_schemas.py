from datetime import datetime, timezone
from urllib.parse import urlparse
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import List, Optional
from app.schemas.link_schema import Link
from app.schemas.pagination_schema import EnhancedPagination
import re
import uuid

class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The unique username of the user. Must be 3-50 characters long. Only letters, numbers, underscores, and hyphens are allowed.",
        example="john_doe_123"
    )
    email: EmailStr = Field(
        ...,
        description="The email address of the user.",
        example="john.doe@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="The full name of the user, if available. Should contain only letters, spaces, hyphens, or apostrophes.",
        example="John Doe"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="A short biography or description of the user.",
        example="I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript."
    )
    profile_picture_url: Optional[str] = Field(
        None,
        description="The URL to the user's profile picture. Must point to a valid image file (e.g., JPEG, PNG).",
        example="https://example.com/profile_pictures/john_doe.jpg"
    )

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
        return v

    @validator('full_name')
    def validate_full_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("Full name can only contain letters, spaces, hyphens, or apostrophes.")
        return v

    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is None:
            return v  # If the URL is optional, allow None values
        parsed_url = urlparse(v)
        if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
            raise ValueError("Profile picture URL must point to a valid image file (JPEG, PNG).")
        return v

    class Config:
        json_schema_extra = {
            "description": "Base model for user information.",
            "example": {
                "username": "john_doe_123",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "bio": "I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript.",
                "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg"
            }
        }

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="A strong password for the user's account. Must be at least 8 characters long and include uppercase and lowercase letters, a digit, and a special character.",
        example="StrongPassword123!"
    )

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        return v

    class Config:
        json_schema_extra = {
            "description": "Model for creating a new user account.",
            "example": {
                "username": "jane_smith_456",
                "email": "jane.smith@example.com",
                "password": "SecurePassword123!",
                "full_name": "Jane Smith",
                "bio": "I am a data scientist passionate about machine learning and big data analytics.",
                "profile_picture_url": "https://example.com/profile_pictures/jane_smith.jpg"
            }
        }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(
        None,
        description="A new email address for the user.",
        example="john.doe.new@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="An updated full name for the user.",
        example="John H. Doe"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="An updated biography or description of the user.",
        example="I am a senior software engineer specializing in backend development with Python and Node.js."
    )
    profile_picture_url: Optional[HttpUrl] = Field(
        None,
        description="An updated URL to the user's profile picture.",
        example="https://example.com/profile_pictures/john_doe_updated.jpg"
    )
 
    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is not None:
            parsed_url = urlparse(str(v))  # Convert the URL object to a string before parsing
            # Ensure the validation logic only runs when parsed_url is defined
            if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
                raise ValueError("Profile picture URL must point to a valid image file (JPEG, PNG).")
        return v

    class Config:
        json_schema_extra = {
            "description": "Model for updating user information.",
            "example": {
                "email": "john.doe.new@example.com",
                "full_name": "John H. Doe",
                "bio": "I am a senior software engineer specializing in backend development with Python and Node.js.",
                "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
            }
        }

class UserResponse(UserBase):
    id: str = Field(
        ...,
        description="The system-generated unique identifier for the user (e.g., UUID).",
        example="a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="A short biography or description of the user.",
        example="I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript."
    )
    last_login_at: Optional[datetime] = Field(
        None,
        description="The timestamp of the user's last successful login, timezone-aware.",
        example="2023-04-09T14:30:00+00:00"
    )
    created_at: datetime = Field(
        ...,
        description="The timestamp when the user account was created, timezone-aware.",
        example="2023-04-01T10:15:30+00:00"
    )
    updated_at: datetime = Field(
        ...,
        description="The timestamp when the user information was last updated, timezone-aware.",
        example="2023-04-05T16:45:00+00:00"
    )
    links: List[Link] = Field(
        [],
        description="Navigational links related to the user for HATEOAS compliance. Includes links for self-reference and updating the user.",
        example=[
            {"rel": "self", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"},
            {"rel": "update", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"}
        ]
    )
    # Custom validator to convert UUID to string
    @validator('id', pre=True, allow_reuse=True)
    def convert_uuid_to_string(cls, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    class Config:
        json_schema_extra = {
            "description": "Model for user response data.",
            "example": {
                "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                "username": "john_doe_123",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "bio": "I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript.",
                "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
                "last_login_at": "2023-04-09T14:30:00+00:00",
                "created_at": "2023-04-01T10:15:30+00:00",
                "updated_at": "2023-04-05T16:45:00+00:00",
                "links": [
                    {"rel": "self", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"},
                    {"rel": "update", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"}
                ]
            }
        }

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(
        ...,
        description="A list of user responses."
    )
    pagination: EnhancedPagination = Field(
        ...,
        description="Pagination details including the current page, total pages, total items, and navigational links."
    )

    class Config:
        json_schema_extra = {
            "description": "Model for a paginated list of user responses.",
            "example": {
                "items": [
                    {
                        "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                        "username": "john_doe_123",
                        "email": "john.doe@example.com",
                        "full_name": "John Doe",
                        "bio": "I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript.",
                        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
                        "last_login_at": "2023-04-09T14:30:00+00:00",
                        "created_at": "2023-04-01T10:15:30+00:00",
                        "updated_at": "2023-04-05T16:45:00+00:00",
                        "links": [
                            {"rel": "self", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"},
                            {"rel": "update", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"}
                        ]
                    },
                    {
                        "id": "b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7",
                        "username": "jane_smith_456",
                        "email": "jane.smith@example.com",
                        "full_name": "Jane Smith",
                        "bio": "I am a data scientist passionate about machine learning and big data analytics.",
                        "profile_picture_url": "https://example.com/profile_pictures/jane_smith.jpg",
                        "last_login_at": "2023-04-08T09:45:00+00:00",
                        "created_at": "2023-04-02T12:30:00+00:00",
                        "updated_at": "2023-04-06T18:15:00+00:00",
                        "links": [
                            {"rel": "self", "href": "https://api.example.com/users/b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7"},
                            {"rel": "update", "href": "https://api.example.com/users/b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7"}
                        ]
                    }
                ],
                "pagination": {
                    "currentPage": 1,
                    "totalPages": 5,
                    "totalItems": 100,
                    "links": [
                        {"rel": "first", "href": "https://api.example.com/users?page=1"},
                        {"rel": "prev", "href": None},
                        {"rel": "self", "href": "https://api.example.com/users?page=1"},
                        {"rel": "next", "href": "https://api.example.com/users?page=2"},
                        {"rel": "last", "href": "https://api.example.com/users?page=5"}
                    ]
                }
            }
        }

class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        description="Username of the user trying to login.",
        example="john_doe_123"
    )
    password: str = Field(
        ...,
        description="Password of the user trying to login.",
        example="StrongPassword123!"
    )

    class Config:
        json_schema_extra = {
            "description": "Model for user login request.",
            "example": {
                "username": "john_doe_123",
                "password": "StrongPassword123!"
            }
        }

class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="A brief description of the error that occurred.",
        example="Invalid username or password."
    )
    details: Optional[str] = Field(
        None,
        description="Additional details about the error, if available.",
        example="The provided username does not exist or the password is incorrect."
    )

    class Config:
        json_schema_extra = {
            "description": "Model for error responses.",
            "example": {
                "error": "Invalid username or password.",
                "details": "The provided username does not exist or the password is incorrect."
            }
        }