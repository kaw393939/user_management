from sqlalchemy.orm import Session
from database import SessionLocal  # Adjust the import path as necessary to find your SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
