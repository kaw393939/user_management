from sqlalchemy.orm import Session
from app.database import SessionLocal
from settings.config import Settings  # Adjust the import path as necessary to find your SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to inject settings
def get_settings():
    return Settings()