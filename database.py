from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import config
# Use the DATABASE_URL from config.py
# If you're using individual components (e.g., POSTGRES_USER), you could construct the URL in config.py and import it here directly.
SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

# The connect_args parameter is not used for PostgreSQL and can be omitted.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define sessionmaker, which is DB-agnostic and doesn't need changes.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
