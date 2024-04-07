import pytest
from starlette.testclient import TestClient

from app.models.user_role_model import UserRole
from app.main import app


import logging
import pytest

# Configure logging at the top of your test file
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_user_with_role(client, user_role):

    # Define user data for the test
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
        "role_id": str(user_role.id),
    }

    # Log the payload being sent to the API
 #   logger.debug("Sending payload to API: %s", user_data)

    # Send a POST request to create a user
    response = client.post("/users/", json=user_data)

    # Log the response from the API
    # logger.debug("Received response: %s", response.json())

    # Assert that the response status code and role_id are as expected
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}. Response: {response.json()}"
    assert response.json()["role"]["id"] == str(user_role.id), "Role ID does not match"
