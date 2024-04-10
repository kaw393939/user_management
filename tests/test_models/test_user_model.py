from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User, UserRole
from uuid import UUID

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    """
    Fixture to create an admin user instance for testing.
    """
    user = User(
        username="admin_user",
        email="admin@example.com",
        hashed_password="securepassword",  # Assume a hashed value
        role=UserRole.ADMIN,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def pro_user(db_session: AsyncSession):
    """
    Fixture to create a pro user instance for testing.
    """
    user = User(
        username="pro_user",
        email="pro@example.com",
        hashed_password="securepassword",  # Assume a hashed value
        role=UserRole.PRO,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.mark.asyncio
async def test_user_role(db_session: AsyncSession, user: User, admin_user: User, pro_user: User):
    """
    Tests that the default role is assigned correctly and can be updated.
    """
    assert user.role == UserRole.USER, "Default role should be USER"
    assert admin_user.role == UserRole.ADMIN, "Admin role should be correctly assigned"
    assert pro_user.role == UserRole.PRO, "Pro role should be correctly assigned"

@pytest.mark.asyncio
async def test_has_role(user: User, admin_user: User, pro_user: User):
    """
    Tests the has_role method to ensure it accurately checks the user's role.
    """
    assert user.has_role(UserRole.USER), "User should have USER role"
    assert not user.has_role(UserRole.ADMIN), "User should not have ADMIN role"
    assert admin_user.has_role(UserRole.ADMIN), "Admin user should have ADMIN role"
    assert pro_user.has_role(UserRole.PRO), "Pro user should have PRO role"

@pytest.mark.asyncio
async def test_user_repr(user: User):
    """
    Tests the __repr__ method for accurate representation of the User object.
    """
    assert repr(user) == f"<User {user.username}, Role: {user.role.name}>", "__repr__ should include username and role"

@pytest.mark.asyncio
async def test_failed_login_attempts_increment(db_session: AsyncSession, user: User):
    """
    Tests that failed login attempts can be incremented and persisted correctly.
    """
    initial_attempts = user.failed_login_attempts
    user.failed_login_attempts += 1
    await db_session.commit()
    await db_session.refresh(user)
    assert user.failed_login_attempts == initial_attempts + 1, "Failed login attempts should increment"

@pytest.mark.asyncio
async def test_last_login_update(db_session: AsyncSession, user: User):
    """
    Tests updating the last login timestamp.
    """
    new_last_login = datetime.now(timezone.utc)
    user.last_login_at = new_last_login
    await db_session.commit()
    await db_session.refresh(user)
    assert user.last_login_at == new_last_login, "Last login timestamp should update correctly"

# More tests can be added to cover additional functionalities and edge cases.
