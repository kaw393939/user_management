from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Initialize these in your application startup routine
async_engine = None
AsyncSessionLocal = None

def initialize_async_db(database_url: str):
    global async_engine, AsyncSessionLocal
    async_engine = create_async_engine(database_url, echo=True)
    AsyncSessionLocal = sessionmaker(
        bind=async_engine, 
        class_=AsyncSession,
        expire_on_commit=False
    )

async def get_async_db():
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()
