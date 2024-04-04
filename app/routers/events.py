from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

# Renamed service function imports to avoid conflicts
from app.config import SERVER_BASE_URL
from app.services.event_service import (
    create_event as create_event_service,
    get_event as get_event_service,
    get_events as get_events_service,
    update_event as update_event_service,
    delete_event as delete_event_service,
)
from app.dependencies import get_db
from app.schemas.schemas import EventCreate, EventUpdate, Event as EventResponse, EventList, Link, Pagination
from app.utils.common import generate_event_links, generate_pagination_links

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()



@router.post("/events/", response_model=EventResponse, tags=["Event Manager"])
async def add_event(event: EventCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    new_event = create_event_service(db=db, **event.dict())
    new_event.links = generate_event_links(new_event.id)
    return new_event

@router.get("/events/", response_model=EventList, tags=["Event Manager"])
async def browse_events(db: Session = Depends(get_db), page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100)):
    events, total_count = get_events_service(db, page=page, per_page=per_page)
    total_pages = (total_count + per_page - 1) // per_page  # Calculate total pages

    items = []
    for event in events:
        event_model = EventResponse.model_validate(event)
        event_model.links = generate_event_links(event.id)  # Manually setting links
        items.append(event_model)

    _links = generate_pagination_links(page, per_page, total_pages)

    response = {
        "items": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total_count,
            "total_pages": total_pages,
        },
        "_links": _links,
    }
    return response


@router.get("/events/{event_id}", response_model=EventResponse, tags=["Event Manager"])
async def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = get_event_service(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_event.links = generate_event_links(db_event.id)
    return db_event

@router.put("/events/{event_id}", response_model=EventResponse, tags=["Event Manager"])
async def edit_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    updated_event = update_event_service(db, event_id=event_id, **event.dict(exclude_unset=True))
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    updated_event.links = generate_event_links(updated_event.id)
    return updated_event

@router.delete("/events/{event_id}", status_code=204, tags=["Event Manager"])
async def delete_event(event_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not delete_event_service(db, event_id=event_id):
        raise HTTPException(status_code=404, detail="Event not found")
    return {"ok": True}
