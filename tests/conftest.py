# Imports related to testing and utilities
from datetime import datetime
from uuid import uuid4
from httpx import AsyncClient

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# SQLAlchemy and database related imports
from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

# Application-specific imports
from app.main import app
from app.database import Base, get_async_db, initialize_async_db
from app.models.user_model import User
from app.dependencies import get_db, get_settings

# Database Configuration
settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

@pytest.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(app=app, base_url="http://test") as client:
        app.dependency_overrides[get_async_db] = lambda: db_session
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def token():
    form_data = {
        "username": "admin",  # Use valid credentials
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)
        return response.json()["access_token"]

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    settings = get_settings()
    initialize_async_db(settings.database_url)
    
# Database Fixtures
@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture(scope="function")
async def user(db_session):
    unique_email = f"test_user_{str(uuid4())}@example.com"
    user_data = {
        "username": "test_user_" + str(uuid4()),
        "email": unique_email,
        "hashed_password": "fake_hashed_password",
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    users = []
    for _ in range(50):  # Create 50 users
        unique_email = f"user_{str(uuid4())}@example.com"
        user_data = {
            "username": "user_" + str(uuid4()),
            "email": unique_email,
            "hashed_password": "fake_hashed_password",
        }
        user = User(**user_data)
        db_session.add(user)
        users.append(user)

    await db_session.commit()  # Commit once after adding all users
    return users


# Client Fixture
@pytest.fixture(scope="function")
def client():
    client = TestClient(app)
    return client

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