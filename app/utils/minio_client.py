from minio import Minio
import os

# Initialize the Minio client using credentials from the .env file
client = Minio(
    endpoint=os.getenv('MINIO_ENDPOINT'),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)

def upload_profile_picture(file_name, file_content):
    bucket_name = "profile-pictures"
    # Ensure the bucket exists before uploading
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Upload the profile picture to the Minio bucket
    client.put_object(
        bucket_name, file_name, file_content, length=-1, part_size=10 * 1024 * 1024
    )
    # Generate and return the URL for accessing the uploaded file
    return client.get_presigned_url("GET", bucket_name, file_name)
