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

from builtins import dict, int, len, str
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_email_service, require_role
from app.schemas.user_schemas import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.utils.link_generation import create_user_links, generate_pagination_links
from app.dependencies import get_settings
from app.services.email_service import EmailService
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
settings = get_settings()
@router.get("/users/{user_id}", response_model=UserResponse, name="get_user", tags=["User Management Requires (Admin or Manager Roles)"])
async def get_user(user_id: UUID, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
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
        nickname=user.nickname,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        profile_picture_url=user.profile_picture_url,
        github_profile_url=user.github_profile_url,
        linkedin_profile_url=user.linkedin_profile_url,
        role=user.role,
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

@router.put("/users/{user_id}", response_model=UserResponse, name="update_user", tags=["User Management Requires (Admin or Manager Roles)"])
async def update_user(user_id: UUID, user_update: UserUpdate, request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
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
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        nickname=updated_user.nickname,
        email=updated_user.email,
        role=updated_user.role,
        last_login_at=updated_user.last_login_at,
        profile_picture_url=updated_user.profile_picture_url,
        github_profile_url=updated_user.github_profile_url,
        linkedin_profile_url=updated_user.linkedin_profile_url,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        links=create_user_links(updated_user.id, request)
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, name="delete_user", tags=["User Management Requires (Admin or Manager Roles)"])
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    """
    Delete a user by their ID.

    - **user_id**: UUID of the user to delete.
    """
    success = await UserService.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management Requires (Admin or Manager Roles)"], name="create_user")
async def create_user(user: UserCreate, request: Request, db: AsyncSession = Depends(get_db), email_service: EmailService = Depends(get_email_service), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    """
    Create a new user.

    This endpoint creates a new user with the provided information. If the email
    already exists, it returns a 400 error. On successful creation, it returns the
    newly created user's information along with links to related actions.

    Parameters:
    - user (UserCreate): The user information to create.
    - request (Request): The request object.
    - db (AsyncSession): The database session.

    Returns:
    - UserResponse: The newly created user's information along with navigation links.
    """
    existing_user = await UserService.get_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    created_user = await UserService.create(db, user.model_dump(), email_service)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    
    
    return UserResponse.model_construct(
        id=created_user.id,
        bio=created_user.bio,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        profile_picture_url=created_user.profile_picture_url,
        nickname=created_user.nickname,
        email=created_user.email,
        role=created_user.role,
        last_login_at=created_user.last_login_at,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at,
        links=create_user_links(created_user.id, request)
    )


@router.get("/users/", response_model=UserListResponse, tags=["User Management Requires (Admin or Manager Roles)"])
async def list_users(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))
):
    total_users = await UserService.count(db)
    users = await UserService.list_users(db, skip, limit)

    user_responses = [
        UserResponse.model_validate(user) for user in users
    ]
    
    pagination_links = generate_pagination_links(request, skip, limit, total_users)
    
    # Construct the final response with pagination details
    return UserListResponse(
        items=user_responses,
        total=total_users,
        page=skip // limit + 1,
        size=len(user_responses),
        links=pagination_links  # Ensure you have appropriate logic to create these links
    )