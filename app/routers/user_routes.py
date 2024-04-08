from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_async_db
from app.schemas.user_schemas import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.schemas.link_schema import Link
from app.utils.link_generation import create_user_links

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Assuming these routes are defined elsewhere in your application
@router.get("/users/{user_id}", response_model=UserResponse, name="get_user", tags=["User Management"])
async def get_user(user_id: UUID, request: Request, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    """
    Fetch a user by their ID.

    - **user_id**: UUID of the user to fetch.
    """
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse.model_construct(
        id=user.id,
        username=user.username,
        email=user.email,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
        # Assuming a utility function `create_user_links` that generates HATEOAS links.
        links=create_user_links(user.id, request)  
    )


@router.put("/users/{user_id}", response_model=UserResponse, name="update_user", tags=["User Management"])
async def update_user(user_id: UUID, user_update: UserUpdate, request: Request, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    """
    Update user information.

    - **user_id**: UUID of the user to update.
    - **user_update**: UserUpdate model with updated user information.
    """
    user_data = user_update.model_dump(exclude_unset=True)
    updated_user = await UserService.update(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse.model_construct(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        last_login_at=updated_user.last_login_at,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        links=create_user_links(updated_user.id, request)
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, name="delete_user", tags=["User Management"])
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    """
    Delete a user by their ID.

    - **user_id**: UUID of the user to delete.
    """
    success = await UserService.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management"], name="create_user")
async def create_user(user: UserCreate, request: Request, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
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
        last_login_at=created_user.last_login_at,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at,
        links=links
    )

@router.get("/users/", response_model=UserListResponse, name="list_users", tags=["User Management"])
async def list_users(request: Request, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    """
    List users with optional pagination.

    - **skip**: Number of users to skip (for pagination).
    - **limit**: Max number of users to return.
    - **request**: The request object for generating full URLs in the response.
    - **db**: Database session dependency.
    """
    users = await UserService.list_users(db, skip=skip, limit=limit)
    user_responses = [
        UserResponse.model_construct(
            id=user.id,
            username=user.username,
            email=user.email,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at,
            # Generate user-specific links
            links=create_user_links(user.id, request)
        )
        for user in users
    ]
    
    # Generate links for the list itself (e.g., pagination links)
    list_links = [
        Link(rel="self", href=str(request.url), method="GET"),
        # Add more links as necessary (e.g., for pagination)
    ]
    
    return UserListResponse(items=user_responses, links=list_links)
