import pytest
from httpx import AsyncClient
from app.main import app  # Import your FastAPI app

@pytest.mark.asyncio
async def test_login_for_access_token():
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_success(client, mock_authenticate_user_success, mock_create_access_token):
    response = client.post("/token", data={"username": "user", "password": "password"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "test_access_token", "token_type": "bearer"}

def test_login_for_access_token_fail(client, mock_authenticate_user_fail):
    response = client.post("/token", data={"username": "user", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_refresh_access_token_success(client, mock_verify_refresh_token_success, mock_create_access_token):
    response = client.post("/token/refresh", json={"refresh_token": "valid_refresh_token"})
    assert response.status_code == 200
    assert response.json() == {"access_token": "test_access_token", "token_type": "bearer"}

def test_refresh_access_token_fail(client, mock_verify_refresh_token_fail):
    response = client.post("/token/refresh", json={"refresh_token": "invalid_refresh_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid refresh token"}
