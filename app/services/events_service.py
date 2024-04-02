# event_service.py

from typing import List, Tuple
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models import Event
from datetime import datetime
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_event(db: Session, title: str, description: str, start_date: datetime, end_date: datetime):
    db_event = Event(title=title, description=description, start_date=start_date, end_date=end_date)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, page: int = 1, per_page: int = 10) -> Tuple[List[Event], int]:
    offset = (page - 1) * per_page
    items = db.query(Event).offset(offset).limit(per_page).all()
    total = db.query(Event).count()
    return items, total

def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def update_event(db_session, event_id, title=None, description=None, start_date=None, end_date=None):
    event = db_session.query(Event).filter(Event.id == event_id).first()
    if event:
        if title is not None:
            event.title = title
        if description is not None:
            event.description = description
        if start_date is not None:
            event.start_date = start_date
        if end_date is not None:
            event.end_date = end_date
        db_session.commit()
        return event
    else:
        # Handle the case where the event does not exist
        pass

def delete_event(db: Session, event_id: int):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event
