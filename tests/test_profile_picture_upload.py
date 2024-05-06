# test_profile_picture_upload.py

import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.utils.minio_utils import get_minio_client

@pytest.mark.asyncio
async def test_upload_profile_picture_success():
    app = FastAPI()
    app.dependency_overrides[get_minio_client] = override_get_minio_client
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(
            "/upload-profile-picture",
            files={"file": ("test_pic.jpg", open("test_pic.jpg", "rb"), "image/jpeg")}
        )
    assert response.status_code == 200
    assert "url" in response.json()
    assert response.json()["url"].startswith("http://minio/")

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
