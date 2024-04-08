import pytest
from app.models.user_model import User

pytestmark = pytest.mark.asyncio
# User Model Tests
@pytest.mark.asyncio
async def test_create_and_delete_user(db_session):
    user_data = {
        "username": "test_user_with_role",
        "email": "test_with_role@example.com",
        "hashed_password": "fake_hashed_password",
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()

    assert user.id is not None

    # Test deletion
    await db_session.delete(user)
    await db_session.commit()

    deleted_user = await db_session.get(User, user.id)
    assert deleted_user is None
