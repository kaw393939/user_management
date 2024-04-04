from uuid import UUID, uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app.database import Base  # Adjust this import to match where your Base metadata is defined
from app.dependencies import get_db
from unittest.mock import patch
from app.dependencies import get_settings
from app.models.models import User

settings = get_settings()
# Update this variable to match your test database configuration for PostgreSQL
TEST_DATABASE_URL = settings.database_url

# Note: Ensure that the PostgreSQL service is running and accessible at the above URL
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionScoped = scoped_session(TestingSessionLocal)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(setup_database):
    session = SessionScoped()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Dependency override for test database
@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_db] = lambda: SessionScoped()
    yield
    app.dependency_overrides.clear()

# Mock fixtures remain unchanged
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

@pytest.fixture(scope="function")
def user(db_session):
    # Mock user data according to the User model fields
    unique_email = f"test_user_{str(uuid4())}@example.com"  # Ensure unique email

    user_data = {
        "username": "test_user_" + str(uuid4()),  # Ensure unique username
        "email": unique_email,  # Ensure unique email
        "hashed_password": "fake_hashed_password"  # Assuming you have a mechanism to hash the password
    }
    # Directly instantiate and add the User model to the session to bypass any custom logic in create_user
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()  # Make sure to commit so the user is saved in the DB
    return user

@pytest.fixture(scope="function")
def sample_event_data(user):
    return {
        "creator_id": user.id,  # Use the created user's ID as the creator_id for the event
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "qr_code_path": None,  # Assuming no QR code for the basic test
    }

@pytest.fixture(scope="function")
def sample_event_data(user):
    # Directly use user.id for creator_id
    return {
        "creator_id": user.id,
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "qr_code_path": None,
    }
