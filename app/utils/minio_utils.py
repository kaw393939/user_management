# Adjust the import according to your project structure
from settings.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
from minio import Minio

def get_minio_client():
    client = Minio(
        endpoint="minio:9000",
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False  # Change to True if using HTTPS
    )
    
    # Check and create bucket if it doesn't exist
    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)
        
    return client

# Additional utility functions related to Minio can be added here as needed
