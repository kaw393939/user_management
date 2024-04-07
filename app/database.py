from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Initialize these in your application startup routine
async_engine = None
AsyncSessionLocal = None

def initialize_async_db(database_url: str):
    global async_engine, AsyncSessionLocal
    async_engine = create_async_engine(database_url, echo=True, future=True)
    AsyncSessionLocal = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False, future=True
    )

async def get_async_db():
    # Use async with statement to ensure the session is properly closed
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()