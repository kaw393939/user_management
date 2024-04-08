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
