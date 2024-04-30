# Standard library imports
from builtins import Exception, range, str
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import uuid4

# Third-party imports
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from faker import Faker

# Application-specific imports
from app.main import app
from app.database import Base, Database
from app.models.user_model import Event, EventType, User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import create_access_token

fake = Faker()

settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)


@pytest.fixture
def email_service():
    # Assuming the TemplateManager does not need any arguments for initialization
    template_manager = TemplateManager()
    email_service = EmailService(template_manager=template_manager)
    return email_service


# This fixture creates the http client for your API tests
@pytest.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: db_session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")

# This function sets up and tears down (drops tables) for each test function, ensuring a clean database for each test.
@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        # You can comment out this line during development if you are debugging a single test
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
async def locked_user(db_session):
    unique_email = fake.email()
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": unique_email,
        "hashed_password": hash_password("MySuperPassword$1234"),
        "role": UserRole.AUTHENTICATED,
        "email_verified": False,
        "is_locked": True,
        "failed_login_attempts": settings.max_login_attempts,
    }
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
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
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
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
async def unverified_user(db_session):
    user_data = {
        "nickname": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
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
async def users_with_same_role_50_users(db_session):
    users = []
    for _ in range(50):
        user_data = {
            "nickname": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
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

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    user = User(
        nickname="admin_user",
        email="admin@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password="securepassword",
        role=UserRole.ADMIN,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def manager_user(db_session: AsyncSession):
    user = User(
        nickname="manager_john",
        first_name="John",
        last_name="Doe",
        email="manager_user@example.com",
        hashed_password="securepassword",
        role=UserRole.MANAGER,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
def admin_token(admin_user):
    # Assuming admin_user has an 'id' and 'role' attribute
    token_data = {"sub": str(admin_user.id), "role": admin_user.role.name, "user_id": str(admin_user.id), "email": str(admin_user.email)}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))

@pytest.fixture(scope="function")
def manager_token(manager_user):
    token_data = {"sub": str(manager_user.id), "role": manager_user.role.name, "user_id": str(manager_user.id), "email": str(manager_user.email)}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))

@pytest.fixture(scope="function")
def user_token(user):
    token_data = {"sub": str(user.id), "role": user.role.name, "user_id": str(user.id), "email": str(user.email)}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))

@pytest.fixture
def email_service():
    if settings.send_real_mail == 'true':
        # Return the real email service when specifically testing email functionality
        return EmailService()
    else:
        # Otherwise, use a mock to prevent actual email sending
        mock_service = AsyncMock(spec=EmailService)
        mock_service.send_verification_email.return_value = None
        mock_service.send_user_email.return_value = None
        return mock_service

# Example event fixtures
@pytest.fixture(scope="function")
async def company_tour_event(db_session, verified_user):
    event_data = {
        "title": "Company Tour",
        "description": "A tour around our new facility.",
        "start_datetime": datetime.now(),
        "end_datetime": datetime.now() + timedelta(hours=2),
        "published": False,
        "event_type": EventType.COMPANY_TOUR,
        "creator_id": verified_user.id
    }
    event = Event(**event_data)
    db_session.add(event)
    await db_session.commit()
    return event

@pytest.fixture(scope="function")
async def mock_interview_event(db_session, verified_user):
    event_data = {
        "title": "Mock Interview Session",
        "description": "Prepare for your upcoming interviews with a practice session.",
        "start_datetime": datetime.now(),
        "end_datetime": datetime.now() + timedelta(hours=1),
        "published": True,
        "event_type": EventType.MOCK_INTERVIEW,
        "creator_id": verified_user.id
    }
    event = Event(**event_data)
    db_session.add(event)
    await db_session.commit()
    return event

@pytest.fixture(scope="function")
async def guest_lecture_event(db_session, manager_user):
    event_data = {
        "title": "Guest Lecture",
        "description": "An informative session with an industry expert.",
        "start_datetime": datetime.now(),
        "end_datetime": datetime.now() + timedelta(hours=3),
        "published": True,
        "event_type": EventType.GUEST_LECTURE,
        "creator_id": manager_user.id
    }
    event = Event(**event_data)
    db_session.add(event)
    await db_session.commit()
    return event


@pytest.fixture
async def user_with_events(db_session: AsyncSession, verified_user):
    user = User(
        nickname="testuser",
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="password",
        role=UserRole.AUTHENTICATED,
        is_locked=False,
    )
    event1 = Event(
        title="Event 1",
        description="Test event 1",
        start_datetime=datetime.now(),
        end_datetime=datetime.now() + timedelta(hours=1),
        published=True,
        event_type=EventType.COMPANY_TOUR,
        creator=user,
    )
    event2 = Event(
        title="Event 2",
        description="Test event 2",
        start_datetime=datetime.now() + timedelta(days=1),
        end_datetime=datetime.now() + timedelta(days=1, hours=1),
        published=False,
        event_type=EventType.MOCK_INTERVIEW,
        creator=user,
    )
    db_session.add_all([user, event1, event2])
    await db_session.commit()
    yield user