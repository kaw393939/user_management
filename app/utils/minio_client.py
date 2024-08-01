# app/utils/minio_client.py

from minio import Minio
from settings.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)

def upload_profile_picture(file_data, file_name):
    minio_client.put_object(
        settings.MINIO_BUCKET_NAME,
        file_name,
        file_data,
        length=-1,
        part_size=10*1024*1024
    )
    return f"{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{file_name}"

def get_profile_picture_url(file_name):
    return minio_client.get_presigned_url('GET', settings.MINIO_BUCKET_NAME, file_name)