import pytest
from app.services.user_service import get_user, get_users, update_user, delete_user

@pytest.mark.asyncio
async def test_create_user(user):
    # The `user` fixture is an async fixture, so we need to await it
    user_obj = user
    assert user_obj.id is not None
    assert user_obj.username is not None
    assert user_obj.email is not None
    assert user_obj.hashed_password is not None

@pytest.mark.asyncio
async def test_get_user(db_session, user):
    # The `get_user()` function returns a coroutine, so we need to await it
    retrieved_user = await get_user(db=db_session, user_id=user.id)
    assert retrieved_user.id == user.id

@pytest.mark.asyncio
async def test_get_users(db_session, user):
    users = await get_users(db=db_session)
    assert len(users) >= 1
    assert any(u.id == user.id for u in users)

@pytest.mark.asyncio
async def test_update_user(db_session, user):
    updated_data = {"username": "updateduser", "email": "updatedemail@example.com"}
    updated_user = await update_user(db=db_session, user_id=user.id, **updated_data)
    assert updated_user.username == updated_data['username']
    assert updated_user.email == updated_data['email']

@pytest.mark.asyncio
async def test_delete_user(db_session, user):
    result = await delete_user(db=db_session, user_id=user.id)
    assert result is True
    deleted_user = await get_user(db=db_session, user_id=user.id)
    assert deleted_user is None
