from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

async_engine = None
AsyncSessionLocal = None

Base = declarative_base()

async def initialize_async_db(database_url: str):
    global async_engine, AsyncSessionLocal
    async_engine = create_async_engine(database_url, echo=True)
    AsyncSessionLocal = AsyncSession

async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal(async_engine) as session:
        try:
            yield session
        finally:
            await session.close()