from minio import Minio
from settings.config import settings
from io import BytesIO
from fastapi import HTTPException


minio_client = Minio(
    f"{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}",
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)

def upload_profile_picture(file_data, file_name):
    file_data.seek(0)
    minio_client.put_object(
        settings.MINIO_BUCKET_NAME,
        file_name,
        file_data,
        length=file_data.getbuffer().nbytes,
        content_type='image/jpeg'
    )
    return f"{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}/{settings.MINIO_BUCKET_NAME}/{file_name}"

def get_profile_picture_url(file_name):
    return minio_client.get_presigned_url('GET', settings.MINIO_BUCKET_NAME, file_name)

def get_profile_picture_stream(file_name):
    try:
        response = minio_client.get_object(settings.MINIO_BUCKET_NAME, file_name)
        return BytesIO(response.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve image: {str(e)}")
