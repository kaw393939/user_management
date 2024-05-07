from fastapi import FastAPI, File, UploadFile
from app.utils.minio_utils import get_minio_client
from pydantic import BaseModel, Field
import logging


# Initialize logger
logger = logging.getLogger(__name__)

# Define the schema for profile picture upload
class ProfilePicture(BaseModel):
    file: bytes  # Assuming the file will be uploaded as bytes
    file_name: str  # Name of the file

    class Config:
        json_schema_extra = {
            "example": {
                "file": "base64-encoded-bytes-here",
                "file_name": "example.jpg"
            }
        }

