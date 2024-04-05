from unittest.mock import patch
import pytest
from httpx import AsyncClient
from app.main import app  # Make sure this imports your FastAPI instance correctly

# Assuming mock_authenticate_user_success, mock_create_access_token,
# mock_authenticate_user_fail, mock_verify_refresh_token_success,
# and mock_verify_refresh_token_fail are asynchronous context managers or
# asynchronous functions that you've adapted from your mock patch utilities

@pytest.mark.asyncio
async def test_login_for_access_token_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_for_access_token_fail():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data={"username": "admin", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}