from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_async_db
from app.schemas.user_schemas import UserCreate, UserRole, UserResponse
from app.services.user_service import UserService
from app.schemas.link_schema import Link
from app.utils.link_generation import create_user_links

router = APIRouter()

# Assuming these routes are defined elsewhere in your application
@router.get("/users/{user_id}", response_model=UserResponse, name="get_user")
async def get_user(user_id: UUID):
    pass

@router.put("/users/{user_id}", response_model=UserResponse, name="update_user")
async def update_user(user_id: UUID):
    pass

@router.delete("/users/{user_id}", name="delete_user")
async def delete_user(user_id: UUID):
    pass



@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management"], name="create_user")
async def create_user(user: UserCreate, request: Request, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new user.

    This endpoint creates a new user with the provided information. If the username
    already exists, it returns a 400 error. On successful creation, it returns the
    newly created user's information along with links to related actions.

    Parameters:
    - user (UserCreate): The user information to create.
    - request (Request): The request object.
    - db (AsyncSession): The database session.

    Returns:
    - UserResponse: The newly created user's information along with navigation links.
    """
    existing_user = await UserService.get_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    created_user = await UserService.create(db, user.model_dump())
    if not created_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    
    links = create_user_links(created_user.id, request)
    
    return UserResponse.model_construct(
        id=created_user.id,
        username=created_user.username,
        email=created_user.email,
        role=UserRole(id=created_user.role.id, name=created_user.role.name),
        last_login_at=created_user.last_login_at,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at,
        links=links
    )