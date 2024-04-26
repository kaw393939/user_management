from builtins import dict, int, len, str
from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, get_db, require_role
from app.schemas.pagination_schema import EnhancedPagination
from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse, EventListResponse
from app.services.event_service import EventService
from app.utils.link_generation import create_event_links, generate_pagination_links, create_event_links
from app.dependencies import get_settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
settings = get_settings()

@router.get("/events/{event_id}", response_model=EventResponse, name="get_event", tags=["Event Management Requires (Admin or Manager Roles)"])
async def get_event(event_id: UUID, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    event = await EventService.get_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return EventResponse.model_construct(
        id=event.id,
        title=event.title,
        description=event.description,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        published=event.published,
        event_type=event.event_type,
        creator_id=event.creator_id,
        created_at=event.created_at,
        updated_at=event.updated_at,
        links=create_event_links(event.id, request)
    )

@router.put("/events/{event_id}", response_model=EventResponse, name="update_event", tags=["Event Management Requires (Admin or Manager Roles)"])
async def update_event(event_id: UUID, event_update: EventUpdate, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    event_data = event_update.model_dump(exclude_unset=True)
    updated_event = await EventService.update(db, event_id, event_data)
    if not updated_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return EventResponse.model_construct(
        id=updated_event.id,
        title=updated_event.title,
        description=updated_event.description,
        start_datetime=updated_event.start_datetime,
        end_datetime=updated_event.end_datetime,
        published=updated_event.published,
        event_type=updated_event.event_type,
        creator_id=updated_event.creator_id,
        created_at=updated_event.created_at,
        updated_at=updated_event.updated_at,
        links=create_event_links(updated_event.id, request)
    )

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, name="delete_event", tags=["Event Management Requires (Admin or Manager Roles)"])
async def delete_event(event_id: UUID, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    success = await EventService.delete(db, event_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/events/", response_model=EventResponse, status_code=status.HTTP_201_CREATED, tags=["Event Management Requires (Admin or Manager Roles)"], name="create_event")
async def create_event(event: EventCreate, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    created_event = await EventService.create(db, event.model_dump())
    if not created_event:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create event")

    return EventResponse.model_construct(
        id=created_event.id,
        title=created_event.title,
        description=created_event.description,
        start_datetime=created_event.start_datetime,
        end_datetime=created_event.end_datetime,
        published=created_event.published,
        event_type=created_event.event_type,
        creator_id=created_event.creator_id,
        created_at=created_event.created_at,
        updated_at=created_event.updated_at,
        links=create_event_links(created_event.id, request)
    )

@router.get("/events/", response_model=EventListResponse, tags=["Event Management Requires (Admin or Manager Roles)"])
async def list_events(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))
):
    total_events = await EventService.count_events(db)
    events = await EventService.list_events(db, skip, limit)

    event_responses = [
        EventResponse.model_validate(event) for event in events
    ]

    pagination_links = generate_pagination_links(request, skip, limit, total_events)

    return EventListResponse(
        items=event_responses,
        total=total_events,
        page=skip // limit + 1,
        size=len(event_responses),
        links=pagination_links
    )

@router.put("/events/{event_id}/publish", response_model=EventResponse, name="publish_event", tags=["Event Management Requires (Admin or Manager Roles)"])
async def publish_event(event_id: UUID, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    published_event = await EventService.publish_event(db, event_id)
    if not published_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return EventResponse.model_construct(
        id=published_event.id,
        title=published_event.title,
        description=published_event.description,
        start_datetime=published_event.start_datetime,
        end_datetime=published_event.end_datetime,
        published=published_event.published,
        event_type=published_event.event_type,
        creator_id=published_event.creator_id,
        created_at=published_event.created_at,
        updated_at=published_event.updated_at,
        links=create_event_links(published_event.id, request)
    )

@router.put("/events/{event_id}/unpublish", response_model=EventResponse, name="unpublish_event", tags=["Event Management Requires (Admin or Manager Roles)"])
async def unpublish_event(event_id: UUID, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    unpublished_event = await EventService.unpublish_event(db, event_id)
    if not unpublished_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return EventResponse.model_construct(
        id=unpublished_event.id,
        title=unpublished_event.title,
        description=unpublished_event.description,
        start_datetime=unpublished_event.start_datetime,
        end_datetime=unpublished_event.end_datetime,
        published=unpublished_event.published,
        event_type=unpublished_event.event_type,
        creator_id=unpublished_event.creator_id,
        created_at=unpublished_event.created_at,
        updated_at=unpublished_event.updated_at,
        links=create_event_links(unpublished_event.id, request)
    )