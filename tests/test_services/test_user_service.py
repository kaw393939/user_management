import pytest
from app.services.user_service import UserService
from app.models.user_model import User

pytestmark = pytest.mark.asyncio

# Test for creating a user with valid data
async def test_create_user_with_valid_data(db_session):
    user_data = {
        "username": "valid_user",
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
    }
    user = await UserService.create(db_session, user_data)
    assert user is not None
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]

# Test for creating a user with invalid data
async def test_create_user_with_invalid_data(db_session):
    user_data = {
        "username": "",  # Invalid username
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data)
    assert user is None

# Test for fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test for fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test for fetching a user by username when the user exists
async def test_get_by_username_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_username(db_session, user.username)
    assert retrieved_user.username == user.username

# Test for fetching a user by username when the user does not exist
async def test_get_by_username_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_username(db_session, "non_existent_username")
    assert retrieved_user is None

# Test for fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test for fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test for updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test for updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test for deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test for attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test for listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test for registering a user with valid data
async def test_register_user_with_valid_data(db_session):
    user_data = {
        "username": "register_valid_user",
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
    }
    user = await UserService.register_user(db_session, user_data)
    assert user is not None
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]

# Test for attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session):
    user_data = {
        "username": "",  # Invalid username
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data)
    assert user is None

# Test for successful user login
async def test_login_user_successful(db_session):
    user_data = {
        "username": "login_success_user",
        "email": "login_success_user@example.com",
        "password": "LoginSuccess123!",
    }
    plain_password = user_data["password"]
    await UserService.register_user(db_session, user_data)
    user = await UserService.login_user(db_session, user_data["username"], plain_password)
    assert user is not None

# Test for user login with incorrect username
async def test_login_user_incorrect_username(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser", "Password123!")
    assert user is None

# Test for user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.username, "IncorrectPassword!")
    assert user is None

# Test for account lock after failed login attempts
async def test_account_lock_after_failed_logins(db_session):
    username = "lock_test_user"
    password = "LockTestPass123!"
    user_data = {"username": username, "email": f"{username}@example.com", "password": password}
    await UserService.register_user(db_session, user_data)
    for _ in range(5):  # Assuming 5 attempts are enough to lock the account
        await UserService.login_user(db_session, username, "wrongpassword")
    is_locked = await UserService.is_account_locked(db_session, username)
    assert is_locked
