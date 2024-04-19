from builtins import Exception
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Database
from settings.config import Settings

def get_settings() -> Settings:
    """Return application settings."""
    return Settings()

async def get_db() -> AsyncSession:
    """Dependency that provides a database session for each request."""
    async_session_factory = Database.get_session_factory()
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
