import uuid
from httpx import AsyncClient
from app.main import app  # Import your FastAPI app
import pytest


@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    # Attempt to create a QR code without authentication
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/qr-codes/", json=qr_request)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    unique_part = uuid.uuid4()  # Generate a unique identifier
    test_url = f"https://example.com/{unique_part}"
    form_data = {
        "username": "admin",
        "password": "secret",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login and get the access token
        token_response = await ac.post("/token", data=form_data)
        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create a QR code with a unique URL
        qr_request = {
            "url": test_url,
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        create_response = await ac.post("/qr-codes/", json=qr_request, headers=headers)
        assert create_response.status_code == 201, "QR Code should be created successfully or already exist."

        # Retrieve the filename from the creation response and delete the QR code
        qr_code_url = create_response.json()["qr_code_url"]
        qr_filename = qr_code_url.split('/')[-1]
        delete_response = await ac.delete(f"/qr-codes/{qr_filename}", headers=headers)
        assert delete_response.status_code == 204, "QR Code should be deleted successfully."