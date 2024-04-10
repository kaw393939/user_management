# Standard library imports
from unittest.mock import patch  # Used for mocking dependencies during testing
from uuid import uuid4  # Used for generating unique identifiers

# Third-party imports
import pytest  # Testing framework
from fastapi.testclient import TestClient  # Used for making HTTP requests to the FastAPI application during testing
from httpx import AsyncClient  # Used for making asynchronous HTTP requests
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Used for working with asynchronous SQLAlchemy sessions
from sqlalchemy.orm import sessionmaker, scoped_session  # Used for creating session factories and scoped sessions
from faker import Faker  # Used for generating fake data

# Application-specific imports
from app.main import app  # The FastAPI application
from app.database import Base, get_async_db, initialize_async_db  # Database-related imports
from app.models.user_model import User, UserRole  # User model
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password  # Dependency injection and settings

# Faker instance for generating fake data during testing
fake = Faker()

# Database Configuration
settings = get_settings()  # Retrieve database configuration settings
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")  # Modify the database URL for asynchronous communication
engine = create_async_engine(TEST_DATABASE_URL, echo=False)  # Create an asynchronous engine for the database
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # Create a session maker for asynchronous sessions
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)  # Create a scoped session for managing database sessions

@pytest.fixture(scope="function")
async def async_client(db_session):
    # This fixture creates an asynchronous test client for making HTTP requests to the FastAPI application
    async with AsyncClient(app=app, base_url="http://test") as client:
        app.dependency_overrides[get_async_db] = lambda: db_session  # Override the database dependency with the test database session
        yield client  # Yield the client for use in tests
        app.dependency_overrides.clear()  # Clear the dependency overrides after the test

@pytest.fixture(scope="function")
async def token():
    # This fixture generates an access token for authenticated requests during testing
    form_data = {
        "username": "admin",  # Use Faker or valid credentials securely
        "password": "secret",  # Consider using environment variables or secure storage
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)  # Make a POST request to the /token endpoint to obtain the access token
        return response.json()["access_token"]  # Return the access token

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    # This fixture initializes the database by calling the initialize_async_db function with the database URL
    initialize_async_db(settings.database_url)

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    # This fixture sets up the database before each test function and drops all tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create all the database tables
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop all the database tables
    await engine.dispose()  # Dispose of the database engine

@pytest.fixture(scope="function")
async def db_session(setup_database):
    # This fixture creates an asynchronous database session for use in tests
    async with AsyncSessionScoped() as session:
        try:
            yield session  # Yield the session for use in tests
        finally:
            await session.close()  # Close the session after the test

@pytest.fixture(scope="function")
async def locked_user(db_session):
    # This fixture creates a single User object with a locked account
    unique_email = fake.email()
    user_data = {
        "username": fake.user_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.USER,
        "email_verified": False,
        "is_locked": True,  # Set is_locked to True for a locked user
        "failed_login_attempts": get_settings().max_login_attempts,  # Set failed login attempts to the maximum allowed
    }
    user = User(**user_data)
    db_session.add(user)  # Add the user to the database session
    await db_session.commit()  # Commit the changes to the database
    return user  # Return the created user object

@pytest.fixture(scope="function")
async def user(db_session):
    # This fixture creates a single User object with fake data using the Faker instance
    unique_email = fake.email()
    user_data = {
        "username": fake.user_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.USER,
        "email_verified": False,  # Set email_verified to False by default
        "is_locked": False,  # Set is_locked to False by default
    }
    user = User(**user_data)
    db_session.add(user)  # Add the user to the database session
    await db_session.commit()  # Commit the changes to the database
    return user  # Return the created user object

@pytest.fixture(scope="function")
async def verified_user(db_session):
    # This fixture creates a single User object with a verified email
    unique_email = fake.email()
    user_data = {
        "username": fake.user_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.USER,
        "email_verified": True,  # Set email_verified to True for a verified user
        "is_locked": False,  # Set is_locked to False by default
    }
    user = User(**user_data)
    db_session.add(user)  # Add the user to the database session
    await db_session.commit()  # Commit the changes to the database
    return user  # Return the created user object

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    # This fixture creates 50 User objects with the same role and fake data
    users = []
    for _ in range(50):
        unique_email = fake.email()
        user_data = {
            "username": fake.user_name(),
            "email": unique_email,
            "hashed_password": fake.password(),
            "email_verified": False,  # Set email_verified to False by default
            "is_locked": False,  # Set is_locked to False by default
        }
        user = User(**user_data)
        db_session.add(user)  # Add each user to the database session
        users.append(user)  # Append the user to the list of users
    await db_session.commit()  # Commit the changes to the database
    return users  # Return the list of created users