import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate
from app.models.user_model import UserRole

pytestmark = pytest.mark.asyncio

async def test_user_created_with_default_role(db_session: AsyncSession):
    user_data = {
        "email": "user@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "role": "ADMIN"
    }
    
    mock_email_service = AsyncMock()

    new_user = await UserService.create(db_session, user_data, mock_email_service)
    
    assert new_user is not None, "User should not be None"
    assert new_user.role == UserRole.ADMIN, f"Expected role to be {UserRole.ADMIN}, but got {new_user.role}"
    assert new_user.email == user_data["email"], f"Expected email to be {user_data['email']}, but got {new_user.email}"
    assert new_user.first_name == user_data["first_name"], f"Expected first name to be {user_data['first_name']}, but got {new_user.first_name}"
    assert new_user.last_name == user_data["last_name"], f"Expected last name to be {user_data['last_name']}, but got {new_user.last_name}"
    mock_email_service.send_verification_email.assert_called_once_with(new_user)
