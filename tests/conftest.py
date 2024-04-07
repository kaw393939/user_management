# Imports related to testing and utilities
from datetime import datetime
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# SQLAlchemy and database related imports
from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

# Application-specific imports
from app.main import app
from app.database import Base, initialize_async_db
from app.models.models import Event, EventSection, EventApproval, EventReview, EventRegistration, Notification
from app.models.user_model import User
from app.models.user_role_model import UserRole 
from app.dependencies import get_db, get_settings

# Database Configuration
settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

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

# Model Fixtures
@pytest.fixture(scope="function")
async def user_role(db_session):
    role_data = {
        "name": "test_role"
    }
    role = UserRole(**role_data)
    db_session.add(role)
    await db_session.commit()
    return role

@pytest.fixture(scope="function")
async def user(db_session, user_role):
    unique_email = f"test_user_{str(uuid4())}@example.com"
    user_data = {
        "username": "test_user_" + str(uuid4()),
        "email": unique_email,
        "hashed_password": "fake_hashed_password",
        "role_id": user_role.id  # Ensure the user has a valid role_id
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

class EventStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
@pytest.fixture(scope="function")
async def event(db_session, user):
    event_data = {
        "creator_id": user.id,
        "title": "Sample Event",
        "description": "A sample event for testing.",
        "location": "Sample Location",
        "status": EventStatus.PENDING,
        "is_public": True,
        "qr_code_path": None
    }
    event = Event(**event_data)
    db_session.add(event)
    await db_session.commit()
    return event

@pytest.fixture(scope="function")
async def event_section(db_session, event):
    section_data = {
        "event_id": event.id,
        "title": "Sample Section",
        "start_date": datetime.strptime("2023-06-01T10:00:00", "%Y-%m-%dT%H:%M:%S"),
        "end_date": datetime.strptime("2023-06-01T12:00:00", "%Y-%m-%dT%H:%M:%S"),
        "location": "Sample Section Location",
        "capacity": 100,
        "registration_deadline": datetime.strptime("2023-06-01T10:00:00", "%Y-%m-%dT%H:%M:%S"),
        "additional_info": "Sample additional info",
        "qr_code_path": None
    }
    section = EventSection(**section_data)
    db_session.add(section)
    await db_session.commit()
    return section

@pytest.fixture(scope="function")
async def event_approval(db_session, event, user):
    approval_data = {
        "event_id": event.id,
        "approved": True,
        "approval_reason": "Sample approval reason",
        "reviewed_by_id": user.id,
        "reviewed_at": datetime.strptime("2023-06-01T10:00:00", "%Y-%m-%dT%H:%M:%S"),
    }
    approval = EventApproval(**approval_data)
    db_session.add(approval)
    await db_session.commit()
    return approval

@pytest.fixture(scope="function")
async def event_review(db_session, event, event_section, user):
    review_data = {
        "event_id": event.id,
        "event_section_id": event_section.id,
        "reviewer_id": user.id,
        "rating": 4,
        "comment": "Sample review comment"
    }
    review = EventReview(**review_data)
    db_session.add(review)
    await db_session.commit()
    return review

@pytest.fixture(scope="function")
async def event_registration(db_session, user, event_section):
    registration_data = {
        "user_id": user.id,
        "event_section_id": event_section.id,
        "attended": True,
        "attended_time": datetime.strptime("2023-06-01T10:00:00", "%Y-%m-%dT%H:%M:%S"),
    }
    registration = EventRegistration(**registration_data)
    db_session.add(registration)
    await db_session.commit()
    return registration

@pytest.fixture(scope="function")
async def notification(db_session, user, event):
    notification_data = {
        "user_id": user.id,
        "event_id": event.id,
        "message": "Sample notification message"
    }
    notification = Notification(**notification_data)
    db_session.add(notification)
    await db_session.commit()
    return notification

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