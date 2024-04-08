import re
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint

from app.schemas.link_schema import Link

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


