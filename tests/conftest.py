"""
File: test_database_operations.py

Overview:
This Python test file uses pytest fixtures to manage the database states for testing various functionalities in a web application using FastAPI and SQLAlchemy.
The file sets up fixtures to mock a testing environment, manipulating database states and HTTP clients to perform isolated tests.
Fixtures are reusable components that set up and tear down necessary preconditions or clean up after the tests are run. They help in maintaining a consistent testing environment and ensure that tests run in isolation, which is crucial for accurate, predictable test outcomes.

Key Components:
- `async_client`: Sets up an asynchronous HTTP client for interacting with the FastAPI app.
- `db_session`: Manages database transactions for each test, ensuring each function starts with a clean database.
- `user`, `locked_user`, `verified_user`, `users_with_same_role_50_users`: Create various user states to test different application behaviors under diverse data conditions.
"""

# Standard library imports
from builtins import range
from unittest.mock import patch  # Used for mocking dependencies during testing
from uuid import uuid4  # Generates unique identifiers, useful in creating objects with a unique key

# Third-party imports
import pytest  # Provides utilities to write concise and maintainable tests
from fastapi.testclient import TestClient  # Facilitates making HTTP requests in tests
from httpx import AsyncClient  # Supports asynchronous HTTP requests
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Asyncio support for SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session  # Utilities to handle SQLAlchemy ORM sessions
from faker import Faker  # Utility for generating fake data

# Application-specific imports
from app.main import app  # The main FastAPI app
from app.database import Base, get_async_db, initialize_async_db  # Database setup and session management
from app.models.user_model import User, UserRole  # User model and roles
from app.dependencies import get_db, get_settings  # Utilities to manage dependencies
from app.utils.security import hash_password  # Helper for hashing passwords

# Faker instance for generating fake data during testing
fake = Faker()

# Database Configuration
settings = get_settings()  # Load configuration settings
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")  # Modify URL for async compatibility
engine = create_async_engine(TEST_DATABASE_URL, echo=False)  # Async engine for database connections
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # Session factory for async operations
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)  # Scoped session to manage sessions throughout the app lifecycle

@pytest.fixture(scope="function")
async def async_client(db_session):
    """Fixture to provide a test client that uses the application instance with overriden dependencies for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        app.dependency_overrides[get_async_db] = lambda: db_session  # Override dependency to use the session created by fixture
        yield client
        app.dependency_overrides.clear()  # Reset overrides after the test to avoid state leakage

@pytest.fixture(scope="function")
async def token():
    """Fixture to generate an access token by authenticating against the FastAPI app's /token endpoint."""
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)
        return response.json()["access_token"]  # Return the access token extracted from the response

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    """Session-wide fixture to initialize the database before any tests are run."""
    initialize_async_db(settings.database_url)

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Fixture to setup the database by creating all tables before each test and dropping them after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Setup schema
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Clean up schema
    await engine.dispose()  # Dispose the engine to free up connections

@pytest.fixture(scope="function")
async def db_session(setup_database):
    """Creates a scoped session for database operations during a test, ensuring transactional isolation."""
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()  # Always close session to prevent leaks

@pytest.fixture(scope="function")
async def locked_user(db_session):
    """Generates a user with a locked status to test application behavior with locked accounts."""
    unique_email = fake.email()
    user_data = {
        "username": fake.user_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": True,
        "failed_login_attempts": get_settings().max_login_attempts,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def user(db_session):
    """Generates a typical user object using fake data for testing normal user interactions."""
    unique_email = fake.email()
    user_data = {
        "username": fake.user_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def verified_user(db_session):
    """Generates a user with a verified email status to test specific application paths that require email verification."""
    unique_email = fake.email()
    user_data = {
        "username": fake.user_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": True,
        "is_locked": False,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    """Generates a bulk of 50 users to test performance and bulk operations within the application."""
    users = []
    for _ in range(50):
        unique_email = fake.email()
        user_data = {
            "username": fake.user_name(),
            "email": unique_email,
            "hashed_password": fake.password(),
            "role": UserRole.AUTHENTICATED,
            "email_verified": False,
            "is_locked": False,
        }
        user = User(**user_data)
        db_session.add(user)
        users.append(user)
    await db_session.commit()
    return users
