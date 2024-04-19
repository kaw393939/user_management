from builtins import ValueError, any, bool, int, str
from pydantic import BaseModel, EmailStr, Field, constr, root_validator, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'  # Regex for http and https URLs
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, pattern=r'^[\w-]+$')  # Corrected regex and constraint usage
    email: EmailStr
    email_verified: Optional[bool] = False
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    github_profile_url: Optional[str] = None
    role: UserRole = UserRole.ANONYMOUS
    is_professional: Optional[bool] = False
    last_login_at: Optional[datetime] = None
    failed_login_attempts: Optional[int] = 0
    is_locked: Optional[bool] = False

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None  # Make username optional
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # Optional password for password updates

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

class UserListResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    size: int
