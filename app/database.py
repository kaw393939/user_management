from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define sessionmaker, which is DB-agnostic and doesn't need changes.
SessionLocal = sessionmaker(autocommit=False, autoflush=False)

Base = declarative_base()

def get_engine():
    from app.dependencies import get_settings
    settings = get_settings()
    # Use the DATABASE_URL from config.py
    # If you're using individual components (e.g., POSTGRES_USER), you could construct the URL in config.py and import it here directly.
    SQLALCHEMY_DATABASE_URL = settings.database_url
    # The connect_args parameter is not used for PostgreSQL and can be omitted.
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return engine
