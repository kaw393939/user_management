from builtins import range
#import pytz
import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.dependencies import get_email_service, get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname
from app.schemas.user_schemas import UserCreate, UserSearchFilter, UserUpdate

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

    
# Additional Test Scenarios
# Test user creation with an existing email address
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_create_user_with_existing_email(email_service, db_session, existing_user):
    user_data = {
        "email": existing_user.email,  # Using the existing user's email
        "password": "AnotherStrongPassword123!",
        "full_name": "Another User",
        "role": UserRole.ANONYMOUS
    }
    
    new_user = await UserService.create(db_session, user_data, email_service)
    
    # User creation should fail as the email already exists
    assert new_user is None

# Helper function to mock query results
class MockResult:
    def __init__(self, users):
        self._users = users

    def scalars(self):
        return self

    def all(self):
        return self._users
       

# Helper function to mock query results
def mock_query_result(users):
    return MockResult(users)

# Test searching users by first name
async def test_search_by_first_name(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.first_name == "John"])

    db_session.execute = mock_execute

    search_filter = UserSearchFilter(username="John")
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if user.first_name == "John"])
    assert all(user.first_name == "John" for user in users)

# Test searching users by last name
async def test_search_by_last_name(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.last_name == "Doe"])

    db_session.execute = mock_execute

    search_filter = UserSearchFilter(username="Doe")
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if user.last_name == "Doe"])
    assert all(user.last_name == "Doe" for user in users)


# Test searching users by email
async def test_search_by_email(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users

    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.email == "john.doe12@example.com"])

   # db_session.execute = AsyncMock(side_effect=mock_execute)
    db_session.execute = mock_execute

    search_filter = UserSearchFilter(email="john.doe@example.com")
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if user.email == "john.doe12@example.com"])

# Test searching users by role
async def test_search_by_role(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.role == UserRole.AUTHENTICATED])

    db_session.execute = mock_execute

    search_filter = UserSearchFilter(role=UserRole.AUTHENTICATED)
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if user.role == UserRole.AUTHENTICATED])
    assert users[0].role == UserRole.AUTHENTICATED 

# Test searching users with no match
async def test_search_no_match(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    async def mock_execute(query):
        return mock_query_result([])

    db_session.execute = mock_execute

    search_filter = UserSearchFilter(username="NonExistentUser")
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == 0

# Test filtering users by account status
async def test_filter_by_account_status(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users

    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.is_locked == False])

    db_session.execute = AsyncMock(side_effect=mock_execute)

    search_filter = UserSearchFilter(account_status=False)
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if not user.is_locked])
    assert all(user.is_locked == False for user in users)

# Test filtering users by creation date range (created_from)
async def test_filter_by_created_from(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    created_from_date = datetime.now(timezone.utc) - timedelta(days=30)

    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.created_at >= created_from_date])

    db_session.execute = AsyncMock(side_effect=mock_execute)

    search_filter = UserSearchFilter(created_from=created_from_date)
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if user.created_at >= created_from_date])
    assert all(user.created_at >= created_from_date for user in users)

# Test filtering users by creation date range (created_to)
async def test_filter_by_created_to(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    created_to_date = datetime.now(timezone.utc) - timedelta(days=30)

    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if user.created_at <= created_to_date])

    db_session.execute = AsyncMock(side_effect=mock_execute)

    search_filter = UserSearchFilter(created_to=created_to_date)
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if user.created_at <= created_to_date])
    assert all(user.created_at <= created_to_date for user in users)

# Test filtering users by creation date range (created_from and created_to)
async def test_filter_by_created_date_range(db_session, users_with_same_role_50_users):
    sample_users = users_with_same_role_50_users
    created_from_date = datetime.now(timezone.utc) - timedelta(days=60)
    created_to_date = datetime.now(timezone.utc) - timedelta(days=30)

    async def mock_execute(query):
        return mock_query_result([user for user in sample_users if created_from_date <= user.created_at <= created_to_date])

    db_session.execute = AsyncMock(side_effect=mock_execute)

    search_filter = UserSearchFilter(created_from=created_from_date, created_to=created_to_date)
    users = await UserService.search_and_filter_users(db_session, search_filter)
    assert len(users) == len([user for user in sample_users if created_from_date <= user.created_at <= created_to_date])
    assert all(created_from_date <= user.created_at <= created_to_date for user in users)
