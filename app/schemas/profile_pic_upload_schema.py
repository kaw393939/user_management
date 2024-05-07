from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, HttpUrl
from app.utils.minio_utils import get_minio_client
import logging

# Initialize logger
logger = logging.getLogger(__name__)

app = FastAPI()

class ProfilePictureResponse(BaseModel):
    url: HttpUrl  # URL to the uploaded image
    detail: str = "Profile picture uploaded successfully."

@app.post("/upload-profile-picture/{user_id}", response_model=ProfilePictureResponse)
async def upload_profile_picture(user_id: int, file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    client = get_minio_client()
    file_path = f"profile-pictures/{user_id}/{file.filename}"
    
    try:
        # Read file content
        file_content = await file.read()
        # Upload to Minio
        client.put_object(bucket_name="profile-pictures", object_name=file_path, data=file_content, length=len(file_content))
        pic_url = construct_public_url("profile-pictures", file_path)  # Assumes you have a method to construct the URL
        
        return ProfilePictureResponse(url=pic_url)
    except Exception as e:
        logger.error(f"Failed to upload profile picture for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

def construct_public_url(bucket_name: str, object_name: str) -> str:
    # This function constructs a URL for accessing the stored file
    minio_host = "minio:9000"  # Adjust as necessary
    return f"http://{minio_host}/{bucket_name}/{object_name}"
