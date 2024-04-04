import pytest
from app.services.user_service import get_user, get_users, update_user, delete_user

def test_create_user(user):
    # The `user` fixture is used here implicitly to create a user
    assert user.id is not None
    assert user.username is not None
    assert user.email is not None
    assert user.hashed_password is not None

def test_get_user(db_session, user):
    retrieved_user = get_user(db=db_session, user_id=user.id)
    assert retrieved_user.id == user.id
    assert retrieved_user.username == user.username
    assert retrieved_user.email == user.email

def test_get_users(db_session, user):
    users = get_users(db=db_session)
    assert len(users) >= 1
    assert any(u.id == user.id for u in users)

def test_update_user(db_session, user):
    updated_data = {"username": "updateduser", "email": "updatedemail@example.com"}
    updated_user = update_user(db=db_session, user_id=user.id, **updated_data)
    assert updated_user.username == updated_data['username']
    assert updated_user.email == updated_data['email']

def test_delete_user(db_session, user):
    result = delete_user(db=db_session, user_id=user.id)
    assert result is True
    deleted_user = get_user(db=db_session, user_id=user.id)
    assert deleted_user is None
