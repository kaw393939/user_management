import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from app.utils.image_uploader import upload, allowed_file, resize_image
from minio.error import S3Error
from uuid import uuid4
from fastapi import UploadFile
from PIL import Image
from io import BytesIO
from unittest.mock import patch, mock_open, MagicMock

from app.dependencies import get_settings
settings = get_settings()

@pytest.fixture
def test_image():
    # Create a test image
    image = Image.new('RGB', (500, 300), color='red')
    image.save('/tmp/test_image.jpg')
    return '/tmp/test_image.jpg'

@pytest.fixture
def test_file():
     image = Image.new('RGB', (500, 300), color='red')
     image.save('/tmp/test_image.jpg')
     return UploadFile(filename="test_image.jpg", file=BytesIO(image.tobytes()))

@pytest.fixture
def test_user_id():
    return uuid4()

def test_allowed_file():
    file_data = b"image_data"
    assert allowed_file(UploadFile(filename="image.png", file=file_data))
    assert allowed_file(UploadFile(filename="image.jpg", file=file_data))
    assert allowed_file(UploadFile(filename="image.jpeg", file=file_data))
    # Test disallowed file extensions
    assert not allowed_file(UploadFile(filename="image.txt", file=file_data))
    assert not allowed_file(UploadFile(filename="image.gif", file=file_data))
