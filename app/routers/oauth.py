"""
This Python file demonstrates the implementation of OAuth2 Password Flow in a FastAPI application. OAuth2 is a standard
protocol for authorization that enables applications to secure designated resources on behalf of a user. Specifically,
the Password Flow is suitable for trusted applications where the user provides their username and password directly to the
application, and in exchange, receives an access token to make authorized requests.

FastAPI simplifies the integration of OAuth2 by providing built-in tools and classes to manage authentication and token issuance.
This example will guide you through setting up an OAuth2PasswordBearer, which is a helper class provided by FastAPI to implement
the OAuth2 Password Flow, and creating endpoints for user authentication and token generation.

Understanding OAuth2PasswordBearer:
- OAuth2PasswordBearer is a class that FastAPI provides to handle OAuth2 Password Flow. It does not authenticate the user but
  specifies that the client (e.g., a frontend application) must send a token in the request's Authorization header using the Bearer scheme.
- The 'tokenUrl' parameter of OAuth2PasswordBearer indicates the URL where the client can send a username and password to obtain the token.

Workflow:
1. The client sends a username and password to the token endpoint.
2. The server authenticates the user with the provided credentials.
3. If authentication is successful, the server generates an access token and returns it to the client.
4. The client uses the access token for subsequent authorized requests to the server.
"""

# Import necessary modules and functions from FastAPI and the standard library
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.dependencies import get_settings  # Custom configuration settings loader
from app.schemas.token_schemas import Token  # Import the Token schema from our application schemas
from app.utils.common import authenticate_user, create_access_token

# Load application settings
settings = get_settings()

# Initialize OAuth2PasswordBearer with the token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create an API router object for registering endpoint(s)
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to authenticate a user and issue an access token.
    
    Uses OAuth2PasswordRequestForm dependency to parse and validate the request form data (username and password).
    
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        
    Returns:
        A JSON response containing the 'access_token' and 'token_type'.
    """
    
    # Authenticate the user with the provided credentials
    user = authenticate_user(form_data.username, form_data.password)
    
    # If authentication fails, return an HTTP 401 Unauthorized response
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Specify the duration the token will be valid
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    
    # Generate an access token
    access_token = create_access_token(
        data={"sub": user["username"]},  # 'sub' (subject) field to identify the user
        expires_delta=access_token_expires
    )
    
    # Return the access token and token type to the client
    return {"access_token": access_token, "token_type": "bearer"}
