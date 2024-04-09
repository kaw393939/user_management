import pytest
from sqlalchemy import select, text
from app.services.user_service import UserService
from app.models.user_model import User

pytestmark = pytest.mark.asyncio

async def test_user_service(db_session):
    # Ensure a role exists for the user
    #  = await ensure_role_exists(db_session, 'TestRole')
    
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "test_password",
    }
    user = await UserService.create(db_session, user_data)
    assert user is not None, "User creation failed"
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]

async def test_get_by_id(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

async def test_get_by_username(db_session, user):
    retrieved_user = await UserService.get_by_username(db_session, user.username)
    assert retrieved_user.username == user.username

async def test_get_by_email(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

async def test_update_user(db_session, user):
    new_username = "updated_" + user.username[:40]  # Ensure the new username is within the 50 characters limit
    updated_user = await UserService.update(db_session, user.id, {"username": new_username})
    assert updated_user is not None
    assert updated_user.username == new_username

@pytest.mark.asyncio
async def test_delete_user(db_session, user):
    # Verify the user exists in the database before deletion
    user_in_db_before_deletion = await db_session.execute(select(User).where(User.id == user.id))
    user_in_db_before_deletion = user_in_db_before_deletion.scalars().first()
    assert user_in_db_before_deletion is not None, "User should exist in the DB before deletion."

    # Attempt to delete the user
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True, "User deletion should succeed."

    # Verify the user no longer exists in the database after deletion
    user_in_db_after_deletion = await db_session.execute(select(User).where(User.id == user.id))
    user_in_db_after_deletion = user_in_db_after_deletion.scalars().first()
    assert user_in_db_after_deletion is None, "User should not exist in the DB after deletion."

@pytest.mark.asyncio
async def test_list_users(db_session, users_with_same_role_50_users):
    # Create multiple users to test pagination
    

    # List the first 10 users
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    assert len(users_page_1) == 10, "Should return 10 users"

    # List the next 1- users
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_2) == 10, "Should return the remaining 5 users"

    # Verify that pagination works correctly
    assert users_page_1[0].username != users_page_2[0].username, "Pagination should return different sets of users"

@pytest.mark.asyncio
async def test_register_user(db_session):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }
    # Create a copy of the user_data for password assertion
    original_password = user_data["password"]
    user = await UserService.register_user(db_session, user_data)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    # Ensure the password is hashed by comparing it to the original password
    assert user.hashed_password != original_password

@pytest.mark.asyncio
async def test_login_user(db_session):
    # Directly register the user here to ensure existence
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPassword123!"
    }
    registered_user = await UserService.register_user(db_session, user_data)
    assert registered_user is not None  # Ensure user is registered

    # Refresh the session if necessary
    await db_session.commit()

    # Test successful login
    user = await UserService.login_user(db_session, "testuser", "StrongPassword123!")
    assert user is not None

    # Reset for clean state if necessary
    await db_session.execute(
    text('UPDATE users SET failed_login_attempts = 0 WHERE username = :username'),
    {'username': "testuser"})
