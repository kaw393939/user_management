from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from unittest.mock import patch
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import hash_password
from unittest.mock import AsyncMock
from fastapi import HTTPException


pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ADMIN.name
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test registering a user with valid data
async def test_register_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
        "role": UserRole.ADMIN
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    user_data = {
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is None

# Test successful user login
async def test_login_user_successful(db_session, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "MySuperPassword$1234",
    }
    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is not None

# Test user login with incorrect email
async def test_login_user_incorrect_email(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser@noway.com", "Password123!")
    assert user is None

# Test user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.email, "IncorrectPassword!")
    assert user is None

# Test account lock after maximum failed login attempts
async def test_account_lock_after_failed_logins(db_session, verified_user):
    max_login_attempts = get_settings().max_login_attempts
    for _ in range(max_login_attempts):
        await UserService.login_user(db_session, verified_user.email, "wrongpassword")
    
    is_locked = await UserService.is_account_locked(db_session, verified_user.email)
    assert is_locked, "The account should be locked after the maximum number of failed login attempts."

# Test resetting a user's password
async def test_reset_password(db_session, user):
    new_password = "NewPassword123!"
    reset_success = await UserService.reset_password(db_session, user.id, new_password)
    assert reset_success is True

# Test verifying a user's email
async def test_verify_email_with_token(db_session, user):
    token = "valid_token_example"  # This should be set in your user setup if it depends on a real token
    user.verification_token = token  # Simulating setting the token in the database
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, token)
    assert result is True

# Test unlocking a user's account
async def test_unlock_user_account(db_session, locked_user):
    unlocked = await UserService.unlock_user_account(db_session, locked_user.id)
    assert unlocked, "The account should be unlocked"
    refreshed_user = await UserService.get_by_id(db_session, locked_user.id)
    assert not refreshed_user.is_locked, "The user should no longer be locked"

# NEW Test role assignment to the first user
async def test_first_user_role_assignment(db_session, email_service):
    user_data = {
        "nickname": "first_user",
        "email": "first_user@example.com",
        "password": "SecurePassword123!",
        "role": UserRole.ANONYMOUS.name  # Assuming default role to be ANONYMOUS for the sake of example
    }
    # Patching UserService.count to simulate no existing users in the database
    with patch('app.services.user_service.UserService.count', return_value=0):
        first_user = await UserService.create(db_session, user_data, email_service)
    assert first_user is not None, "User creation failed"
    assert first_user.role == UserRole.ADMIN, "First user should be assigned ADMIN role"

# NEW Test password is hashed
async def test_password_hashing_on_creation(db_session, email_service):
    user_data = {
        "nickname": "new_user",
        "email": "secure_user@example.com",
        "password": "SecurePassword123!",
        "role": UserRole.ANONYMOUS.name  # Assuming ANONYMOUS is a valid role enum
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None, "User should be created successfully"
    assert user.hashed_password != "SecurePassword123!", "Password should be hashed and not stored in plaintext"
    
# NEW Test listing users with extreme pagination
async def test_list_users_extreme_pagination(db_session):
    users = await UserService.list_users(db_session, skip=-1, limit=1000)
    assert len(users) >= 0, "Skip with negative should handle gracefully and limit should not overflow"

# NEW test where creation sends verification email with token 
async def test_user_creation_sends_verification_email_with_token(db_session: AsyncSession, mocker):
    # Mock dependencies
    email_service_mock = AsyncMock()
    mocker.patch('app.utils.nickname_gen.generate_nickname', return_value='unique_nickname')
    mocker.patch('app.utils.security.hash_password', return_value='hashed_password')
    mocker.patch('app.services.user_service.generate_verification_token', return_value='12345-token')
    mocker.patch('app.services.user_service.UserService.count', return_value=1)

    # User data for the test
    user_data = {
        "email": "new_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ANONYMOUS.name  # Ensure the user gets a verification token
    }

    # Call the method under test
    new_user = await UserService.create(db_session, user_data, email_service_mock)

    # Assertions to check token assignment and email sending
    assert new_user is not None, "User should be successfully created"
    assert new_user.verification_token == '12345-token', "Verification token should be assigned to the user"
    assert new_user.email == "new_user@example.com", "User email should be set correctly"
    email_service_mock.send_verification_email.assert_called_once_with(new_user)

# NEW NICKNAME TESTS
# Mock database access and nickname generation
async def fake_get_by_nickname(session, nickname):
    # Simulate database check for existing nicknames
    return None  # Simulate all nicknames as unique

@pytest.fixture
def setup_mocks(mocker):
    mocker.patch('app.services.user_service.generate_nickname', side_effect=lambda: "user123")
    mocker.patch('app.services.user_service.UserService.get_by_nickname', new=fake_get_by_nickname)

async def test_generate_unique_nickname_with_collision(db_session: AsyncSession, mocker):
    """Test that unique nickname generation handles collisions and retries."""
    # Setup mocker to simulate a nickname collision on the first call
    mocker.patch('app.services.user_service.UserService.get_by_nickname', side_effect=[True, None])
    mocker.patch('app.services.user_service.generate_nickname', side_effect=["user123", "user124"])

    unique_nickname = await UserService.generate_unique_nickname(db_session)
    assert unique_nickname == "user124", "Should return a new unique nickname after detecting a collision"
