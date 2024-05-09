from builtins import ValueError, bool, classmethod, str
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from threading import Lock

Base = declarative_base()

class Database:
    """Handles database connections and sessions."""
    _engine = None
    _session_factory = None
    _lock = Lock()  # Mutex lock for thread safety

    @classmethod
    def initialize(cls, database_url: str, echo: bool = False):
        """Initialize the async engine and sessionmaker. Thread-safe initialization."""
        with cls._lock:  # Ensure that initialization is thread-safe
            if cls._engine is None:
                cls._engine = create_async_engine(
                    database_url, echo=echo, future=True
                )
                cls._session_factory = sessionmaker(
                    bind=cls._engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                    future=True
                )

    @classmethod
    def get_session_factory(cls):
        """Returns the session factory, ensuring it's initialized."""
        with cls._lock:  # Ensure thread-safe access
            if cls._session_factory is None:
                raise ValueError("Database not initialized. Call `initialize()` first.")
            return cls._session_factory

    @classmethod
    def dispose_engine(cls):
        """Dispose of the engine explicitly when done, for clean-up."""
        with cls._lock:
            if cls._engine is not None:
                cls._engine.sync_engine.dispose()
                cls._engine = None
                cls._session_factory = None
