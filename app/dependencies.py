# app/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from settings.config import Settings

def get_settings():
    return Settings()

async def get_db() -> AsyncSession:
    async for session in get_async_db():
        yield session
