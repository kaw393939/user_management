from typing import List, Tuple
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.models import Event  # Ensure correct import paths
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_event(db: Session, creator_id: uuid.UUID, title: str, description: str, qr_code_path: str = None) -> Event:
    """
    Create a new event without specifying start and end dates at this level.
    """
    db_event = Event(
        title=title,
        description=description,
        creator_id=creator_id,
        qr_code_path=qr_code_path
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 10) -> Tuple[List[Event], int]:
    """
    Retrieve a list of events with pagination.
    """
    items = db.query(Event).offset(skip).limit(limit).all()
    total = db.query(Event).count()
    return items, total

def get_event(db: Session, event_id: uuid.UUID) -> Event:
    """
    Retrieve an event by its ID.
    """
    return db.query(Event).filter(Event.id == event_id).first()

def update_event(db_session: Session, event_id: uuid.UUID, title: str = None, description: str = None, qr_code_path: str = None) -> Event:
    """
    Update an existing event with new details.
    """
    event = db_session.query(Event).filter(Event.id == event_id).first()
    if event:
        if title is not None:
            event.title = title
        if description is not None:
            event.description = description
        if qr_code_path is not None:
            event.qr_code_path = qr_code_path
        db_session.commit()
        return event
    else:
        return None

def delete_event(db: Session, event_id: uuid.UUID) -> bool:
    """
    Delete an event by its ID.
    """
    event_to_delete = db.query(Event).filter(Event.id == event_id).first()
    if event_to_delete:
        db.delete(event_to_delete)
        db.commit()
        return True
    return False
