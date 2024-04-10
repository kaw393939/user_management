"""
This Python file is part of a FastAPI application, demonstrating user management functionalities including creating, reading,
updating, and deleting (CRUD) user information. It uses OAuth2 with Password Flow for security, ensuring that only authenticated
users can perform certain operations. Additionally, the file showcases the integration of FastAPI with SQLAlchemy for asynchronous
database operations, enhancing performance by non-blocking database calls.

The implementation emphasizes RESTful API principles, with endpoints for each CRUD operation and the use of HTTP status codes
and exceptions to communicate the outcome of operations. It introduces the concept of HATEOAS (Hypermedia as the Engine of
Application State) by including navigational links in API responses, allowing clients to discover other related operations dynamically.

OAuth2PasswordBearer is employed to extract the token from the Authorization header and verify the user's identity, providing a layer
of security to the operations that manipulate user data.

Key Highlights:
- Use of FastAPI's Dependency Injection system to manage database sessions and user authentication.
- Demonstrates how to perform CRUD operations in an asynchronous manner using SQLAlchemy with FastAPI.
- Implements HATEOAS by generating dynamic links for user-related actions, enhancing API discoverability.
- Utilizes OAuth2PasswordBearer for securing API endpoints, requiring valid access tokens for operations.
"""

from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_async_db
from app.schemas.pagination_schema import EnhancedPagination
from app.schemas.user_schemas import LoginRequest, UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.utils.common import create_access_token
from app.utils.link_generation import create_user_links, generate_pagination_links
from app.dependencies import get_settings
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()
@router.get("/users/{user_id}", response_model=UserResponse, name="get_user", tags=["User Management"])
async def get_user(user_id: UUID, request: Request, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    """
    Endpoint to fetch a user by their unique identifier (UUID).

    Utilizes the UserService to query the database asynchronously for the user and constructs a response
    model that includes the user's details along with HATEOAS links for possible next actions.

    Args:
        user_id: UUID of the user to fetch.
        request: The request object, used to generate full URLs in the response.
        db: Dependency that provides an AsyncSession for database access.
        token: The OAuth2 access token obtained through OAuth2PasswordBearer dependency.
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
        links=create_user_links(user.id, request)  
    )

# Additional endpoints for update, delete, create, and list users follow a similar pattern, using
# asynchronous database operations, handling security with OAuth2PasswordBearer, and enhancing response
# models with dynamic HATEOAS links.

# This approach not only ensures that the API is secure and efficient but also promotes a better client
# experience by adhering to REST principles and providing self-discoverable operations.

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
        bio=updated_user.bio,
        full_name=updated_user.full_name,
        profile_picture_url=updated_user.profile_picture_url,
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
    
    
    return UserResponse.model_construct(
        id=created_user.id,
        bio=created_user.bio,
        full_name=created_user.full_name,
        profile_picture_url=created_user.profile_picture_url,
        username=created_user.username,
        email=created_user.email,
        last_login_at=created_user.last_login_at,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at,
        links=create_user_links(created_user.id, request)
    )


@router.get("/users/", response_model=UserListResponse, name="list_users", tags=["User Management"])
async def list_users(request: Request, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    total_users = await UserService.count(db)
    users = await UserService.list_users(db, skip=skip, limit=limit)

    user_responses = [UserResponse.model_construct(
        id=user.id,
        bio=user.bio,
        full_name=user.full_name,
        profile_picture_url=user.profile_picture_url,
        username=user.username,
        email=user.email,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
        links=create_user_links(user.id, request)
    ) for user in users]

    pagination_links = generate_pagination_links(request, skip, limit, total_users)
    pagination = EnhancedPagination(
        page=skip // limit + 1,
        per_page=limit,
        total_items=total_users,
        total_pages=(total_users + limit - 1) // limit,
        links=pagination_links
    )

    return UserListResponse(items=user_responses, pagination=pagination)


@router.post("/register/", response_model=UserResponse)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_async_db)):
    user = await UserService.register_user(session, user_data.dict())
    if user:
        return user
    raise HTTPException(status_code=400, detail="Username already exists")

@router.post("/login/")
async def login(login_request: LoginRequest, session: AsyncSession = Depends(get_async_db)):
    if await UserService.is_account_locked(session, login_request.username):
        raise HTTPException(status_code=400, detail="Account locked due to too many failed login attempts.")

    user = await UserService.login_user(session, login_request.username, login_request.password)
    if user:
        # Generate a token for the user. You need to implement create_access_token.
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    
        # Generate an access token
        access_token = create_access_token(
        data={"sub": user.username},  # 'sub' (subject) field to identify the user
        expires_delta=access_token_expires
    )

        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password.")