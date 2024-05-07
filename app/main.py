import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
from app.utils.minio_utils import get_minio_client
import uvicorn

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize MinIO client
minioClient = get_minio_client

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def connect_to_minio():
    try:
        # Attempt to connect to MinIO
        global minioClient
        minioClient = get_minio_client()
    except Exception as e:
        logging.error(f"Failed to connect to MinIO: {e}")
        raise  # Re-raise the exception to trigger retry

@app.on_event("startup")
async def startup_event():
    try:
        settings = get_settings()
        Database.initialize(settings.database_url, settings.debug)
        connect_to_minio()  # Initialize Minio client and ensure buckets are ready
    except Exception as e:
        logging.error(f"Startup failed: {e}")

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logging.error(f"An unexpected error occurred: {exc}")
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

'''# Route for uploading profile picture
@app.post("/upload-pp/")
async def upload_profile_picture(file: UploadFile = File(...)):
    try:
        # Create an instance of the ProfilePicture schema
        profile_picture = ProfilePicture(file=file.file.read(), file_name=file.filename)

        # Save the profile picture to MinIO
        minioClient.put_object(
            "profile-pictures",  # Bucket name
            file.filename,  # Object name (use file name)
            file.file,  # File-like object
            length=-1,  # Use length=-1 to read until EOF
        )

        # Return success message or relevant data
        return {"message": "Profile picture uploaded successfully"}
    except Exception as e:
        # Log the exception
        logging.error("An unexpected error occurred:", exc_info=True)
        # Return error response
        return {"error": "An unexpected error occurred. Please try again later."}
'''
app.include_router(user_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)  # Change the port number here
