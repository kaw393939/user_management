from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from app.main import app  # Adjust this import path as necessary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import Base  # Adjust this import to match where your Base metadata is defined
from sqlalchemy.orm import scoped_session
from unittest.mock import patch
 
# Update these variables to match your test database configuration
TEST_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Optional: If you're using Alembic, you can use it here to upgrade and downgrade your test database schema

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db_session():
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    Base.metadata.create_all(bind=engine)  # Create the tables.
    db_session = scoped_session(TestingSessionLocal)
    try:
        yield db_session
    finally:
        db_session.rollback()
        db_session.close()
        Base.metadata.drop_all(bind=engine)  # Optional: Drop tables after each test

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