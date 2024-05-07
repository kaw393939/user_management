from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from unittest.mock import AsyncMock
from uuid import uuid4

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
async def test_register_user_with_invalid_data_1(db_session, email_service):
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



# Test updating a user's nickname
async def test_update_user_nickname(db_session, user):
    new_nickname = "new_nickname"
    updated_user = await UserService.update(db_session, user.id, {"nickname": new_nickname})
    assert updated_user is not None
    assert updated_user.nickname == new_nickname

# Test verifying a user's email with an expired token
async def test_verify_email_with_expired_token(db_session, user):
    expired_token = "expired_token_example"
    user.verification_token = expired_token
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, expired_token)
    assert result is True

# Test deleting a user account
async def test_delete_user_account(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is False

# Mock AsyncSession
class MockAsyncSession:
    async def execute(self, query):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass

# Mock EmailService
class MockEmailService:
    async def send_verification_email(self, user):
        pass

# Mock User model
class MockUser:
    def __init__(self, id, verification_token, role):
        self.id = id
        self.verification_token = verification_token
        self.role = role
        self.email_verified = False

# Test registering a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    invalid_user_data = {
        "email": "invalid_email_format",  # Invalid email format
        "password": "short",              # Invalid password
        # Missing 'nickname' and 'role'
    }
    user = await UserService.register_user(db_session, invalid_user_data, email_service)
    assert user is None

# Test verifying a user's email with an expired token
async def test_verify_email_with_expired_token(db_session, user):
    expired_token = "expired_token_example"
    user.verification_token = expired_token
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, expired_token)
    assert result is True

# Test deleting a user account
async def test_delete_user_account(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True


# Test sending a verification email after user creation
async def test_verification_email_sent_after_user_creation(db_session, email_service):
    # Define a mock async function to replace send_verification_email
    async def mock_send_verification_email(user):
        pass

    # Replace the send_verification_email method with the mock function
    email_service.send_verification_email = mock_send_verification_email

    # User data for registration
    user_data = {
        "nickname": generate_nickname(),
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
        "role": UserRole.ADMIN
    }

    # Call the register_user method
    user = await UserService.register_user(db_session, user_data, email_service)

    # Assert that the user is not None
    assert user is not None
    assert user.email == user_data["email"]

# Test verifying a user's email with an invalid token
async def test_verify_email_with_invalid_token(db_session):
    # Arrange
    user_id = "invalid_user_id"
    token = "invalid_token_example"
    
    # Mock UserService methods
    UserService.get_by_id = AsyncMock(return_value=None)
    
    # Act
    result = await UserService.verify_email_with_token(db_session, user_id, token)

    # Assert
    assert result is False

# Test registering a user with invalid data
async def test_register_user_with_invalid_data_safety(db_session, email_service):
    # Arrange
    invalid_user_data = {
        "email": "invalid_email_format",  # Invalid email format
        "password": "short",              # Invalid password
        # Missing 'nickname' and 'role'
    }
    
    # Act
    user = await UserService.register_user(db_session, invalid_user_data, email_service)
    
    # Assert
    assert user is None

# Test verifying a user's email with an expired token
async def test_verify_email_with_expired_token_safety(db_session, user):
    # Arrange
    expired_token = "expired_token_example"
    user.verification_token = expired_token
    await db_session.commit()
    
    # Act
    result = await UserService.verify_email_with_token(db_session, user.id, expired_token)
    
    # Assert
    assert result is False

# Test deleting a user account
async def test_delete_user_account_safety(db_session, user):
    # Act
    deletion_success = await UserService.delete(db_session, user.id)
    
    # Assert
    assert deletion_success is False
