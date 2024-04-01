# conftest.py
import pytest
from httpx import AsyncClient
from app.main import app  # Adjust import path as necessary

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
async def get_access_token_for_test(client):
    form_data = {"username": "admin", "password": "secret"}
    response = await client.post("/token", data=form_data)
    return response.json()["access_token"]
