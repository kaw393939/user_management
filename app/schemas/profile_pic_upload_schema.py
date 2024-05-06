from fastapi import FastAPI, File, UploadFile
from minio import Minio
from minio.error import S3Error
from pydantic import BaseModel



# Define the schema for profile picture upload
class ProfilePicture(BaseModel):
    file: bytes  # Assuming the file will be uploaded as bytes
    file_name: str  # Name of the file

# Initialize MinIO client
minio_client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="Shashwat123!",
    secure=False  # Change to True if using HTTPS
)

app = FastAPI()

# Route for uploading profile picture
@app.post("/upload-profile-picture/")
async def upload_profile_picture(file: UploadFile = File(...)):
    # Create an instance of the ProfilePicture schema
    profile_picture = ProfilePicture(file=file.file.read(), file_name=file.filename)
    
    # Save the profile picture to MinIO
    try:
        minio_client.put_object(
            "profile-pictures",  # Bucket name
            file.filename,  # Object name (use file name)
            file.file,  # File-like object
            length=-1,  # Use length=-1 to read until EOF
        )
    except S3Error as err:
        return {"error": f"Failed to upload profile picture: {err}"}
    
    # Return success message or relevant data
    return {"message": "Profile picture uploaded successfully"}
