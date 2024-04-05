# app/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from settings.config import Settings

def get_settings():
    return Settings()

async def get_db() -> AsyncSession:
    async with get_async_db() as session:
        yield session