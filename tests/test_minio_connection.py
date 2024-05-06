# test_minio_connection.py
import pytest
from minio import Minio
from app.utils.minio_utils import get_minio_client

def test_minio_client_connection():
    minio_client = get_minio_client()
    assert isinstance(minio_client, Minio), "Minio client should be an instance of Minio"
    assert minio_client._endpoint == "localhost:9000", "Check the endpoint is correctly set"
