from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_engine
from settings.config import Settings

# Dependency to get settings
def get_settings():
    return Settings()

# Create an async session object
async_session = AsyncSession(async_engine, expire_on_commit=False)

# Define a function to get an async session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
