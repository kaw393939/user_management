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


def test_resize_image(test_image, test_user_id):
    resized_image_path = resize_image(test_image, (200, 200), test_user_id)
    assert os.path.exists(resized_image_path)
    assert resized_image_path == f"/tmp/{str(test_user_id)}.jpg"

    os.remove(test_image)
    os.remove(resized_image_path)


@patch("PIL.Image.open")
@patch("app.utils.image_uploader.minio_client.fput_object")
async def test_upload_error(mock_fput_object, mock_image_open, test_file, test_user_id):
    mock_image = MagicMock(spec=Image.Image)
    mock_image.resize.return_value = mock_image
    mock_image_open.return_value = mock_image

    with patch("builtins.open", mock_open(read_data=b"test image data")), \
         patch("app.utils.image_uploader.resize_image", return_value="/tmp/resized_test.jpg"), \
         patch("app.utils.image_uploader.minio_client.fput_object", side_effect=S3Error(code=500, message="S3 error", resource="bucket/object", request_id="request_id", host_id="host_id",response="response")):
        url = await upload(test_file, test_user_id)
        assert url is None

@patch("PIL.Image.open")
@patch("app.utils.image_uploader.minio_client.fput_object")
async def test_upload(mock_fput_object, mock_image_open, test_file, test_user_id):
    mock_image = MagicMock(spec=Image.Image)
    mock_image.resize.return_value = mock_image
    mock_image_open.return_value = mock_image

    with patch("builtins.open", mock_open(read_data=b"test image data")), \
         patch("app.utils.image_uploader.resize_image", return_value="/tmp/resized_test.jpg"):
        url = await upload(test_file, test_user_id)
        assert url == f"http://localhost:9000/{settings.MINIO_BUCKET_NAME}/{str(test_user_id)}.jpg"
        mock_fput_object.assert_called_with(settings.MINIO_BUCKET_NAME, f"{str(test_user_id)}.jpg", "/tmp/resized_test.jpg")
