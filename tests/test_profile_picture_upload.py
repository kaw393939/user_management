# test_profile_picture.py
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.user_routes import router as user_router
from app.utils.minio_utils import get_minio_client
from app.dependencies import override_get_minio_client

@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(user_router)
    return app

@pytest.mark.asyncio
async def test_upload_profile_picture_success(test_app):
    file_data = b"fake_image_data"
    filename = "test_pic.jpg"
    content_type = "image/jpeg"
    with patch('app.utils.minio_utils.get_minio_client') as mock_minio_client:
        mock_minio_client.return_value.put_object = MagicMock(return_value=None)  # Simulate successful upload
        async with AsyncClient(app=test_app, base_url="http://testserver") as ac:
            response = await ac.post(
                "/upload-profile-picture",
                files={"file": (filename, file_data, content_type)}
            )
            assert response.status_code == 200
            assert "url" in response.json()

@pytest.mark.asyncio
async def test_upload_profile_picture_invalid_file_type():
    app = FastAPI()
    app.dependency_overrides[get_minio_client] = override_get_minio_client
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(
            "/upload-profile-picture",
            files={"file": ("test_pic.png", open("test_pic.png", "rb"), "image/png")}
        )
    assert response.status_code == 400
    assert "error" in response.json()

@pytest.mark.asyncio
async def test_retrieve_user_profile_picture(test_app, async_session: AsyncSession):
    user_id = 1  # Assuming this user is in your test database
    async with AsyncClient(app=test_app, base_url="http://testserver") as ac:
        response = await ac.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert 'profile_picture_url' in response.json()
        assert response.json()['profile_picture_url'].startswith("https://")


@pytest.mark.asyncio
async def test_profile_picture_upload_error_handling(test_app):
    with patch('app.utils.minio_utils.get_minio_client') as mock_minio_client:
        mock_minio_client.side_effect = Exception("Minio is down")
        async with AsyncClient(app=test_app, base_url="http://testserver") as ac:
            response = await ac.post(
                "/upload-profile-picture",
                files={"file": ("fake_pic.jpg", b"fake_data", "image/jpeg")}
            )
            assert response.status_code == 500
            assert "error" in response.json()
            assert response.json()['detail'] == "Failed to upload to Minio"
