import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint

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

