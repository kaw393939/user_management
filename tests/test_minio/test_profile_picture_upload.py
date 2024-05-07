import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from app.routers.user_routes import router as user_router
from app.utils.minio_utils import get_minio_client

@pytest.fixture
def app():
    _app = FastAPI()
    _app.include_router(user_router)
    return _app

@pytest.fixture
def mock_minio_client():
    with patch('app.utils.minio_utils.get_minio_client') as mock:
        client = MagicMock()
        client.put_object = MagicMock()
        mock.return_value = client
        yield client

@pytest.mark.asyncio
async def test_upload_profile_picture_invalid_file_type(app, mock_minio_client):
    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        response = await test_client.post(
            "/upload-profile-picture/1",  # Ensure the route expects and correctly handles user_id
            files={"file": ("wrongtype.txt", b"Not an image!", "text/plain")}
        )
        assert response.status_code == 400, "Expected failure on invalid file type"
