import faker
import pytest
from sqlalchemy.exc import IntegrityError
from app.services.user_service import create_user, get_user, get_users, update_user, delete_user
from app.models.models import User
from faker import Faker

faker = Faker()
@pytest.fixture(scope="function")
def sample_user_data():
    unique_suffix = faker.unique.first_name()
    return {
        "username": f"testuser_{unique_suffix}",
        "email": f"testuser_{unique_suffix}@example.com",
        "password": "SecurePassw0rd!",
    }

def test_create_user(db_session, sample_user_data):
    user = create_user(db=db_session, **sample_user_data)
    assert user.id is not None
    assert user.username == sample_user_data['username']
    assert user.email == sample_user_data['email']
    # Ensure the password is not stored in plain text
    assert user.hashed_password != sample_user_data['password']

def test_get_user(db_session, sample_user_data):
    created_user = create_user(db=db_session, **sample_user_data)
    retrieved_user = get_user(db=db_session, user_id=created_user.id)
    assert retrieved_user.id == created_user.id
    assert retrieved_user.username == created_user.username
    assert retrieved_user.email == created_user.email

def test_get_users(db_session, sample_user_data):
    create_user(db=db_session, **sample_user_data)
    users = get_users(db=db_session)
    assert len(users) >= 1
    # Verify the created user is in the retrieved list
    assert any(user.email == sample_user_data['email'] for user in users)

def test_update_user(db_session, sample_user_data):
    user = create_user(db=db_session, **sample_user_data)
    updated_data = {"username": "updateduser", "email": "updatedemail@example.com"}
    updated_user = update_user(db=db_session, user_id=user.id, **updated_data)
    assert updated_user.username == updated_data['username']
    assert updated_user.email == updated_data['email']

def test_delete_user(db_session, sample_user_data):
    # Create a user to delete
    user = create_user(db=db_session, **sample_user_data)

    # Delete the user
    result = delete_user(db=db_session, user_id=user.id)

    # Assert that the deletion was reported as successful
    assert result is True

    # Attempt to retrieve the deleted user
    deleted_user = get_user(db_session, user.id)

    # Assert that the user cannot be retrieved, indicating successful deletion
    assert deleted_user is None
