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

from builtins import Exception, bool, classmethod, str
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class for declarative model definition. All models will inherit from this class.
Base = declarative_base()

class Database:
    """Encapsulate database engine and sessionmaker to avoid global state."""
    engine = None
    session_factory = None

    @classmethod
    def initialize(cls, database_url: str, echo: bool = False):
        """
        Initializes the asynchronous database engine and sessionmaker.
        
        :param database_url: The database URL to connect to.
        :param echo: Enable SQL query logging.
        """
        cls.engine = create_async_engine(database_url, echo=echo, future=True)
        cls.session_factory = sessionmaker(
            bind=cls.engine, class_=AsyncSession, expire_on_commit=False, future=True
        )

async def get_async_db():
    """
    An asynchronous generator function to yield a database session and ensure it gets closed properly.
    
    This function should be used as a dependency in FastAPI route handlers to provide a session for each request.
    """
    async with Database.session_factory() as async_session:
        try:
            yield async_session
        except Exception as e:
            # Optionally add more specific database exception handling here
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await async_session.close()
