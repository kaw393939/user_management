# Imports related to testing and utilities
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# SQLAlchemy and database related imports
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

# Application-specific imports
from app.main import app
from app.database import Base  # Adjust this import as necessary
from app.models.models import User
from app.dependencies import get_db, get_settings

# Database Configuration
settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

# Database Fixtures
@pytest.fixture(scope="function")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest.fixture(scope="function")
async def user(db_session):
    unique_email = f"test_user_{str(uuid4())}@example.com"
    user_data = {
        "username": "test_user_" + str(uuid4()),
        "email": unique_email,
        "hashed_password": "fake_hashed_password"
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

# Application Client Fixture
@pytest.fixture(scope="module")
async def client():
    async with TestClient(app) as c:
        yield c

# Mock Fixtures
@pytest.fixture
def mock_authenticate_user_success():
    with patch("app.routers.oauth.authenticate_user", return_value={"username": "test_user"}) as mock:
        yield mock

@pytest.fixture
def mock_authenticate_user_fail():
    with patch("app.routers.oauth.authenticate_user", return_value=None) as mock:
        yield mock

@pytest.fixture
def mock_create_access_token():
    with patch("app.routers.oauth.create_access_token", return_value="test_access_token") as mock:
        yield mock

@pytest.fixture
def mock_verify_refresh_token_success():
    with patch("app.routers.oauth.verify_refresh_token", return_value={"username": "test_user"}) as mock:
        yield mock

@pytest.fixture
def mock_verify_refresh_token_fail():
    with patch("app.routers.oauth.verify_refresh_token", return_value=None) as mock:
        yield mock

# Utility Fixture for Test Data
@pytest.fixture(scope="function")
def sample_event_data(user):
    return {
        "creator_id": user.id,
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "qr_code_path": None,
    }
