import pytest
from httpx import AsyncClient
from app.main import app  # Adjust this import path as necessary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import Base  # Adjust this import to match where your Base metadata is defined
from sqlalchemy.orm import scoped_session

# Update these variables to match your test database configuration
TEST_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Optional: If you're using Alembic, you can use it here to upgrade and downgrade your test database schema

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

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
