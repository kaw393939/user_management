from datetime import datetime
import re
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, Field, HttpUrl, validator

from app.schemas.link_schema import Link
from app.schemas.pagination_schema import EnhancedPagination

# Assuming the Link and EnhancedPagination imports remain unchanged
# from app.schemas.link_schema import Link
# from app.schemas.pagination_schema import EnhancedPagination

def validate_username(username: str) -> str:
    """
    Validates that the username contains only letters, numbers, underscores, and hyphens.
    """
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
    return username

def validate_password(password: str) -> str:
    """
    Validates that the password meets complexity requirements: at least 8 characters long,
    contains an uppercase letter, a lowercase letter, a digit, and a special character.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character.")
    return password

class UserBase(BaseModel):
    username: str = Field(..., example="john_doe", min_length=3, max_length=50, description="The unique username of the user. Only letters, numbers, underscores, and hyphens are allowed.")
    email: EmailStr = Field(..., example="john.doe@example.com", description="The email address of the user.")
    full_name: Optional[str] = Field(None, example="John Doe", min_length=1, max_length=100, description="The full name of the user, if available.")
    bio: Optional[str] = Field(None, example="A passionate software developer.", max_length=500, description="A short biography or description of the user.")
    profile_picture_url: Optional[HttpUrl] = Field(None, example="https://example.com/profiles/john_doe.jpg", description="The URL to the user's profile picture.")

    _normalize_username = validator("username", allow_reuse=True)(validate_username)

class UserCreate(UserBase):
    password: str = Field(..., example="SecretPassword123!", min_length=8, description="A password for the user's account, meeting complexity requirements. Must include an uppercase letter, a lowercase letter, a digit, and a special character.")

    _validate_password = validator("password", allow_reuse=True)(validate_password)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="new.email@example.com", description="A new email address for the user.")
    full_name: Optional[str] = Field(None, example="Jane Doe", min_length=1, max_length=100, description="An updated full name for the user.")
    bio: Optional[str] = Field(None, example="An enthusiastic open-source contributor.", max_length=500, description="An updated biography or description of the user.")
    profile_picture_url: Optional[HttpUrl] = Field(None, example="https://example.com/profiles/jane_doe.jpg", description="An updated URL to the user's profile picture.")

class UserResponse(UserBase):
    id: UUID4 = Field(..., example="3fa85f64-5717-4562-b3fc-2c963f66afa6", description="The system-generated unique identifier for the user.")
    last_login_at: Optional[datetime] = Field(None, example="2023-04-01T12:34:56.789Z", description="The timestamp of the user's last successful login.")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00Z", description="The timestamp when the user account was created.")
    updated_at: datetime = Field(..., example="2023-02-01T12:00:00Z", description="The timestamp when the user information was last updated.")
    links: List[Link] = Field([], example=[{"rel": "self", "href": "https://api.example.com/users/1"}], description="Navigational links related to the user for HATEOAS compliance.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., description="A list of user responses.")
    pagination: EnhancedPagination = Field(..., description="Pagination details including navigational links.")

class LoginRequest(BaseModel):
    username: str
    password: str