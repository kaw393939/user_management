from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import List, Optional
from app.schemas.link_schema import Link
from app.schemas.pagination_schema import EnhancedPagination
import re

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The unique username of the user. Must be 3-50 characters long. Only letters, numbers, underscores, and hyphens are allowed.")
    email: EmailStr = Field(..., description="The email address of the user.")
    full_name: Optional[str] = Field(None, max_length=100, description="The full name of the user, if available.")
    bio: Optional[str] = Field(None, max_length=500, description="A short biography or description of the user.")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="The URL to the user's profile picture.")

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="A strong password for the user's account. Must be at least 8 characters long and include uppercase and lowercase letters, a digit, and a special character.")

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

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="A new email address for the user.")
    full_name: Optional[str] = Field(None, max_length=100, description="An updated full name for the user.")
    bio: Optional[str] = Field(None, max_length=500, description="An updated biography or description of the user.")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="An updated URL to the user's profile picture.")

class UserResponse(UserBase):
    id: str = Field(..., description="The system-generated unique identifier for the user.")
    last_login_at: Optional[datetime] = Field(None, description="The timestamp of the user's last login, timezone-aware.")
    created_at: datetime = Field(..., description="The timestamp when the user account was created, timezone-aware.")
    updated_at: datetime = Field(..., description="The timestamp when the user information was last updated, timezone-aware.")
    links: List[Link] = Field([], description="Navigational links related to the user for HATEOAS compliance.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., description="A list of user responses.")
    pagination: EnhancedPagination = Field(..., description="Pagination details including navigational links.")

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username of the user trying to login.")
    password: str = Field(..., description="Password of the user trying to login.")
