from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from minio import Minio
from minio.error import S3Error
import os
from builtins import str
from uuid import UUID
from settings.config import settings
from PIL import Image
from io import BytesIO

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024 

async def upload(file : UploadFile,user_id:UUID) -> str:
    try:
            # Save the uploaded file to a temporary directory
        # p = read_index()
        
        file_path = f"/tmp/{file.filename}"
        size = (200, 200)  # New size: width = 200, height = 200
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        resized_image_data = resize_image(file_path, size,user_id)
        print(resized_image_data)
        

        image_name = str(user_id)+"."+file.filename.split('.')[1]
        # Upload the file to Minio
        minio_client.fput_object(settings.MINIO_BUCKET_NAME, image_name, resized_image_data)

        # Remove the temporary file
        os.remove(file_path)
        os.remove(resized_image_data)

        # Return success response
        return "http://localhost:9000/"+settings.MINIO_BUCKET_NAME+"/"+image_name
    except S3Error as exc:
        print("error occurred.", exc)
        return None

def allowed_file(file:UploadFile):
    filename = file.filename
    """Check if the file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image, size,user_id):
    with Image.open(image) as img:
        resized_img = img.resize(size)
        # Convert image to bytes
        output_path = f"/tmp/{str(user_id)}.{image.split('.')[1]}"
        resized_img.save(output_path)
        return output_path