from datetime import datetime
import re
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr, Field, HttpUrl, validator
from app.schemas.link_schema import Link

def validate_username(username: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
    return username

def validate_password(password: str) -> str:
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
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user.")
    email: EmailStr = Field(..., description="The email address of the user.")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="The full name of the user.")
    bio: Optional[str] = Field(None, max_length=500, description="The bio of the user.")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="The URL of the user's profile picture.")

    _normalize_username = validator("username", allow_reuse=True)(validate_username)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="The password of the user.")

    _validate_password = validator("password", allow_reuse=True)(validate_password)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="The updated email address of the user.")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="The updated full name of the user.")
    bio: Optional[str] = Field(None, max_length=500, description="The updated bio of the user.")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="The updated URL of the user's profile picture.")

class UserResponse(UserBase):
    id: UUID4 = Field(..., description="The unique identifier of the user.")
    last_login_at: Optional[datetime] = Field(None, description="The timestamp of the user's last login.")
    created_at: datetime = Field(..., description="The timestamp when the user was created.")
    updated_at: datetime = Field(..., description="The timestamp when the user was last updated.")
    links: List[Link] = Field([], description="The HATEOAS links related to the user.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., description="The list of users.")
    links: List[Link] = Field([], description="The HATEOAS links related to the user list.")
