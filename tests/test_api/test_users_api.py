from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403


# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]

@pytest.mark.asyncio
async def test_update_user_email_access_Not_allowed_test2(async_client, admin_user, verified_user, admin_token):
    # Prepare updated email data based on admin user's ID
    updated_email_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    await async_client.put(f"/users/{admin_user.id}", json=updated_email_data, headers=headers)
    second_response = await async_client.put(f"/users/{verified_user.id}", json=updated_email_data, headers=headers)
    assert "email already exist" in second_response.json().get("detail", ""), \
        "The API should prevent duplicate email addresses and return a corresponding error message."

@pytest.mark.asyncio
async def test_update_user_email_access_allowed_test3(async_client, admin_user, verified_user, admin_token):
    update_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}

    # First update to set the new email
    initial_response = await async_client.put(f"/users/{admin_user.id}", json=update_data, headers=headers)
    assert initial_response.status_code == 200, "The first update should be successful."

    # Second update with the same email to check idempotency
    repeat_response = await async_client.put(f"/users/{admin_user.id}", json=update_data, headers=headers)
    assert repeat_response.status_code == 200, "The repeated update with the same email should also be successful."

@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "AnotherPassword123!",
        "role": UserRole.ADMIN.name
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_with_linkedin_url_test4(async_client, verified_user):
    user_data = {
        "email": "john12_linkedin@example.com",  # Ensure unique email
        "password": "AnotherPassword123!",
        "role": UserRole.ADMIN.name,
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200, "Expected successful creation status code"

@pytest.mark.asyncio
async def test_create_user_with_github_url_test5(async_client, verified_user):
    user_data = {
        "email": "john12_github@example.com",  # Ensure unique email
        "password": "AnotherPassword123!",
        "role": UserRole.ADMIN.name,
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200, "Expected successful creation status code"

@pytest.mark.asyncio
async def test_clear_github_url_test6(async_client, admin_user, admin_token):
    # Prepare the data for updating the user, setting the GitHub URL to an empty string
    updated_data = {
        "email": f"updated_{admin_user.id}@example.com",
        "github_profile_url": ""
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Execute the PUT request to update the user
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)

    # Verify the response status code and that the GitHub URL was cleared (i.e., set to None)
    assert response.status_code == 200, "Expected HTTP 200 status code for successful update"
    assert response.json().get("github_profile_url") is None, "GitHub URL should be set to None after update"

@pytest.mark.asyncio
async def test_update_professional_status_as_admin_test7(async_client: AsyncClient, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.patch(f"/users/{admin_user.id}/upgrade", headers=headers)
    assert response.status_code == 200
    assert response.json().get("is_professional") == True, "Admin should be able to update professional status."

@pytest.mark.asyncio
async def test_update_professional_status_as_user_denied_test8(async_client: AsyncClient, admin_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.patch(f"/users/{admin_user.id}/upgrade", headers=headers)
    assert response.status_code == 403, "Regular users should not be allowed to update professional status."

@pytest.mark.asyncio
async def test_update_professional_status_as_manager_test9(async_client: AsyncClient, admin_user, manager_token):
    headers = {"Authorization": f"Bearer {manager_token}"}
    response = await async_client.patch(f"/users/{admin_user.id}/upgrade", headers=headers)
    assert response.status_code == 200
    assert response.json().get("is_professional") == True, "Managers should be able to update professional status."

@pytest.mark.asyncio
async def test_user_self_update_unauthorized_test10(async_client: AsyncClient, admin_user, admin_token):
    # Data to update, assuming the endpoint updates user's own profile based on their token
    updated_data = {"first_name": "Test", "last_name": "User"}
    # No authorization header is provided intentionally to simulate unauthorized access
    response = await async_client.put("/users/updateMyProfile", json=updated_data)
    assert response.status_code == 401, "Should require authorization to update profile."

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user
