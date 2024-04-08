"""
This Python file is designed to demonstrate how to set up and use an asynchronous database connection
with SQLAlchemy in a FastAPI application. The code introduces the concepts of creating an asynchronous
engine and session with SQLAlchemy, which are essential for performing database operations asynchronously.

Asynchronous database connections are crucial for non-blocking database operations, allowing FastAPI applications
to handle other requests while waiting for the database operations to complete. This is particularly beneficial
for applications with high concurrency requirements, improving overall performance and scalability.

The file consists of:
- Import statements for necessary SQLAlchemy async modules and functions.
- A base declarative class used to define database models.
- Initialization of global variables for the async engine and session.
- A function to initialize the async database engine and sessionmaker with a given database URL.
- An asynchronous generator function to manage database sessions, ensuring sessions are opened and closed correctly.

By the end of this file, students should understand how to set up an asynchronous database connection in FastAPI
and the importance of managing database sessions properly to avoid resource leaks and ensure the application's
efficiency and reliability.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class for declarative model definition. All models will inherit from this class.
Base = declarative_base()

# Initialize these variables in your application startup routine.
# `async_engine` will hold the connection pool to the database, and
# `AsyncSessionLocal` will be a factory for creating new sessions.
async_engine = None
AsyncSessionLocal = None

def initialize_async_db(database_url: str):
    """
    Initializes the asynchronous database engine and sessionmaker.

    :param database_url: The database URL to connect to, as a string.
    """
    global async_engine, AsyncSessionLocal
    # Create an async engine. This is the starting point for any SQLAlchemy application.
    # The `echo=True` flag is useful for debugging by showing the generated SQL queries.
    # The `future=True` flag is to enable future SQLAlchemy features.
    async_engine = create_async_engine(database_url, echo=True, future=True)
    
    # Create a sessionmaker, configured to use the async engine, for generating new database sessions.
    # The `class_=AsyncSession` parameter tells sessionmaker to use SQLAlchemy's async session class.
    # `expire_on_commit=False` prevents attributes from being expired after commit.
    AsyncSessionLocal = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False, future=True
    )

async def get_async_db():
    """
    An asynchronous generator function to yield a database session and ensure it gets closed properly.

    This function should be used as a dependency in FastAPI route handlers to provide a session for each request.
    """
    # Use async with statement to automatically manage session lifecycle.
    async with AsyncSessionLocal() as async_session:
        try:
            # Yield the session to the request handler.
            yield async_session
        finally:
            # Ensure the session is closed when the request handler is complete.
            await async_session.close()
