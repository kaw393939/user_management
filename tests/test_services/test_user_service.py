from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from pydantic import ValidationError
from app.schemas.user_schemas import UserCreate
from sqlalchemy.exc import IntegrityError


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

#Additional tests 
@pytest.mark.asyncio
async def test_create_admin_user(db_session, email_service):
    user_data = {
        "email": "admin@example.com",
        "password": "Secure*1234",
        "nickname": "admin",
        "role": UserRole.ADMIN.name  # Adding the role field
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.role == UserRole.ADMIN
    assert user.email_verified is True

@pytest.mark.asyncio
async def test_create_user_with_invalid_role(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "invalid_role_user@example.com",
        "password": "ValidPassword123!",
        "role": "INVALID_ROLE"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**user_data)
    assert exc_info.value.errors()[0]['loc'] == ('role',)
    assert exc_info.value.errors()[0]['msg'] == "Input should be 'ANONYMOUS', 'AUTHENTICATED', 'MANAGER' or 'ADMIN'"

@pytest.mark.asyncio
async def test_update_user_non_existent_id(db_session):
    non_existent_user_id = "non-existent-id"
    updated_user = await UserService.update(db_session, non_existent_user_id, {"email": "new_email@example.com"})
    assert updated_user is None

@pytest.mark.asyncio
async def test_register_user_with_short_nickname(db_session, email_service):
    user_data = {
        "nickname": "ab",
        "email": "short_nickname_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ANONYMOUS  # Adding the role field
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**user_data)
    assert exc_info.value.errors()[0]['loc'] == ('nickname',)
    assert exc_info.value.errors()[0]['msg'] == "String should have at least 3 characters"

@pytest.mark.asyncio
async def test_register_user_with_invalid_nickname(db_session, email_service):
    user_data = {
        "nickname": "invalid!nickname",
        "email": "invalid_nickname_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ANONYMOUS  # Adding the role field
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**user_data)
    assert exc_info.value.errors()[0]['loc'] == ('nickname',)
    assert exc_info.value.errors()[0]['msg'] == "String should match pattern '^[\\w-]+$'"

# Test registering a user with a too long email address
@pytest.mark.asyncio
async def test_register_user_with_long_email(db_session, email_service):
    long_email = "a" * 245 + "@example.com"  # Total length 256 characters
    user_data = {
        "nickname": generate_nickname(),
        "email": long_email,
        "password": "ValidPassword123!",
        "role": UserRole.ANONYMOUS  # Adding the role field
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

@pytest.mark.asyncio
async def test_update_user_with_invalid_role(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"role": "INVALID_ROLE"})
    assert updated_user is None

# Test login with an unverified account
@pytest.mark.asyncio
async def test_login_unverified_account(db_session, email_service):
    user_data = {
        "email": "unverified_login@example.com",
        "password": "Secure*1234",
        "nickname": "unverified_login",
        "role": UserRole.ANONYMOUS  # Ensuring the role is ANONYMOUS
    }
    user = await UserService.create(db_session, user_data, email_service)
    user.email_verified = False  # Explicitly setting email_verified to False
    await db_session.commit()  # Commit the changes to the database

    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is None

# Check if the email_verified flag is set to False when creating a regular user
@pytest.mark.asyncio
async def test_create_regular_user_email_verified_flag(db_session, email_service):
    # Ensure there is already an ADMIN user in the system
    admin_user_data = {
        "email": "admin_user@example.com",
        "password": "Secure*1234",
        "nickname": "admin_user",
        "role": UserRole.ADMIN.name
    }
    await UserService.create(db_session, admin_user_data, email_service)

    # Now create a regular user
    regular_user_data = {
        "email": "regular_user@example.com",
        "password": "Secure*1234",
        "nickname": "regular_user",
        "role": UserRole.ANONYMOUS.name  # Explicitly setting the role to ANONYMOUS
    }
    user = await UserService.create(db_session, regular_user_data, email_service)
    assert user is not None
    assert user.email_verified is False

# Test if the user can be fetched by role
@pytest.mark.asyncio
async def test_fetch_user_by_role(db_session, email_service):
    # Ensure there is already an ADMIN user in the system
    admin_user_data = {
        "email": "admin_user@example.com",
        "password": "Secure*1234",
        "nickname": "admin_user",
        "role": UserRole.ADMIN.name
    }
    await UserService.create(db_session, admin_user_data, email_service)

    # Now create a user with the ANONYMOUS role
    user_data = {
        "email": "role_user@example.com",
        "password": "Secure*1234",
        "nickname": "role_user",
        "role": UserRole.ANONYMOUS.name  # Explicitly setting the role to ANONYMOUS
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None, "User creation failed"
    assert user.role == UserRole.ANONYMOUS, f"Expected role to be ANONYMOUS but got {user.role}"

    query = select(User).filter(User.role == UserRole.ANONYMOUS)
    result = await db_session.execute(query)
    users = result.scalars().all()
    assert len(users) > 0, "No users found with role ANONYMOUS"

@pytest.mark.asyncio
async def test_login_locked_account(db_session, email_service):
    user_data = {
        "email": "locked_user@example.com",
        "password": "Secure*1234",
        "nickname": "locked_user",
        "role": UserRole.ANONYMOUS.name  # Adding the role field
    }
    user = await UserService.create(db_session, user_data, email_service)
    user.is_locked = True  # Lock the user's account
    await db_session.commit()  # Commit the changes to the database

    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is None, "Locked user should not be able to log in"

# If IntegrityError is still not caught, test if log message is correctly captured
@pytest.mark.asyncio
async def test_update_user_email_to_existing_email_with_logging(db_session, email_service, caplog):
    # Create the first user with a unique email
    first_user_data = {
        "email": "first_user@example.com",
        "password": "Secure*1234",
        "nickname": "first_user",
        "role": UserRole.ANONYMOUS.name
    }
    first_user = await UserService.create(db_session, first_user_data, email_service)
    assert first_user is not None, "First user creation failed"
    
    # Create a second user with a different email
    second_user_data = {
        "email": "second_user@example.com",
        "password": "Secure*1234",
        "nickname": "second_user",
        "role": UserRole.ANONYMOUS.name
    }
    second_user = await UserService.create(db_session, second_user_data, email_service)
    assert second_user is not None, "Second user creation failed"
    
    # Attempt to update the second user's email to the first user's email
    await UserService.update(db_session, second_user.id, {"email": first_user.email})
    
    # Verify the log contains the integrity error message
    assert any("Database error" in message for message in caplog.messages), "IntegrityError should be logged as a Database error"
    
    # Verify the second user's email has not been updated
    updated_second_user = await UserService.get_by_id(db_session, second_user.id)
    assert updated_second_user.email == "second_user@example.com", "The email should not have been updated due to uniqueness constraint"
