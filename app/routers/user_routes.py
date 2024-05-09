from builtins import Exception, dict, int, len, print, str
from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Security, status, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, get_db, get_email_service, require_role
from app.schemas.token_schema import TokenResponse
from app.schemas.user_schemas import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.services.jwt_service import create_access_token
from app.utils.link_generation import create_user_links, generate_pagination_links
from app.dependencies import get_settings
from app.services.email_service import EmailService
from app.exceptions.user_exceptions import UserNotFoundException, EmailAlreadyExistsException, InvalidCredentialsException, AccountLockedException, InvalidVerificationTokenException
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)

@router.get(
            "/users/{user_id}", 
            response_model=UserResponse, name="get_user", 
            tags=["User Management Requires (Admin or Manager Roles)"])
async def get_user(
    user_id: UUID, 
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme), 
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    try:
        user = await UserService.get_by_id(db, user_id)
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
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put(
        "/users/{user_id}", 
        response_model=UserResponse, 
        name="update_user", 
        tags=["User Management Requires (Admin or Manager Roles)"]
        )
async def update_user(
    user_id: UUID, 
    user_update: UserUpdate, 
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))
    ):
    try:
        user_data = user_update.model_dump(exclude_unset=True)
        updated_user = await UserService.update(db, user_id, user_data)
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
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

@router.delete(
        "/users/{user_id}", 
        status_code=status.HTTP_204_NO_CONTENT, 
        name="delete_user", 
        tags=["User Management Requires (Admin or Manager Roles)"]
        )
async def delete_user(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    try:
        await UserService.delete(db, user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post(
        "/users/", 
        response_model=UserResponse, 
        status_code=status.HTTP_201_CREATED, 
        tags=["User Management Requires (Admin or Manager Roles)"], 
        name="create_user")
async def create_user(
    user: UserCreate, 
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    email_service: EmailService = Depends(get_email_service), 
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))
    ):
    try:
        created_user = await UserService.create(db, user.model_dump(), email_service)
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
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user.")

@router.get(
        "/users/", 
        response_model=UserListResponse, 
        tags=["User Management Requires (Admin or Manager Roles)"])
async def list_users(
    request: Request,
    skip: int= 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))
):
    total_users = await UserService.count(db)
    users = await UserService.list_users(db, skip, limit)
    user_responses = [UserResponse.model_validate(user) for user in users]
    pagination_links = generate_pagination_links(request, skip, limit, total_users)
    return UserListResponse(
        items=user_responses,
        total=total_users,
        page=skip // limit + 1,
        size=len(user_responses),
        links=pagination_links
    )



@router.post(
        "/register/", 
        response_model=UserResponse, 
        tags=["Login and Registration"]
        )
async def register(
    user_data: UserCreate = Body(...), 
    session: AsyncSession = Depends(get_db), 
    email_service: EmailService = Depends(get_email_service)):
    try:
        user = await UserService.register_user(session, user_data.model_dump(), email_service)
        return UserResponse.model_construct(
            id=user.id,
            nickname=user.nickname,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.post("/login/",
             response_model=TokenResponse, 
             tags=["Login and Registration"]
             )
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
    ):
    try:
        user = await UserService.login_user(session, form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email, "role": str(user.role.name), "user_id": str(user.id)},
            expires_delta=access_token_expires
        )
        # Immediately decode to verify
        try:
            decoded = jwt.decode(access_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            logging.info(f"Immediate decode check: {decoded}")
        except jwt.PyJWTError as e:
            logging.error(f"Immediate decode failed: {e}")
        
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except AccountLockedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
@router.get(
        "/myaccount", 
        response_model=UserResponse, 
        tags=["My Account"]
        )
async def myaccount(
    request: Request,
    session: AsyncSession = Depends(get_db),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme), 
    current_user: dict = Depends(get_current_user)):
    
    print(f"What is my current user data: {current_user}")
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return UserResponse.model_construct(
        id=current_user["user_id"],
        role=current_user["role"],
        email=current_user["sub"],

    )

@router.put(
        "/myaccount/", 
        response_model=UserResponse, 
        name="update_myaccount", 
        tags=["My Account"]
        )
async def update_myaccount(
    user_update: UserUpdate, 
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(get_current_user)):
    
    try:
        user_data = user_update.model_dump(exclude_unset=True)
        user_id = current_user["user_id"]
        updated_user = await UserService.update(db, user_id, user_data)
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
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")



@router.post(
        "/login_with_form/", 
        include_in_schema=False, tags=["Login and Registration"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
    ):
    try:
        user = await UserService.login_user(session, form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email, "role": str(user.role.name), "user_id": str(user.id)},
            expires_delta=access_token_expires
        )
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except AccountLockedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.post("/logout", tags=["Login and Registration"])
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response

@router.get("/verify-email/{user_id}/{token}", status_code=status.HTTP_200_OK, name="verify_email", tags=["Login and Registration"])
async def verify_email(user_id: UUID, token: str, db: AsyncSession = Depends(get_db), email_service: EmailService = Depends(get_email_service)):
    try:
        await UserService.verify_email_with_token(db, user_id, token)
        return RedirectResponse(url=settings.account_verfiy_destination)
    except InvalidVerificationTokenException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

