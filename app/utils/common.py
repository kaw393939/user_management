import logging.config
import os
import base64
from typing import List
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.dependencies import get_settings
import validators  # Make sure to install this package
from urllib.parse import urlparse, urlunparse

from app.schemas.schemas import Link

settings = get_settings()
def setup_logging():
    """
    Sets up logging for the application using a configuration file.
    This ensures standardized logging across the entire application.
    """
    # Construct the path to 'logging.conf', assuming it's in the project's root.
    logging_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
    # Normalize the path to handle any '..' correctly.
    normalized_path = os.path.normpath(logging_config_path)
    # Apply the logging configuration.
    logging.config.fileConfig(normalized_path, disable_existing_loggers=False)

def authenticate_user(username: str, password: str):
    """
    Placeholder for user authentication logic.
    In a real application, replace this with actual authentication against a user database.
    """
    # Simple check against constants for demonstration.
    if username == settings.admin_user and password == settings.admin_password:
        return {"username": username}
    # Log a warning if authentication fails.
    logging.warning(f"Authentication failed for user: {username}")
    return None

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def validate_and_sanitize_url(url_str):
    """
    Validates a given URL string and returns a sanitized version if valid.
    Returns None if the URL is invalid, ensuring only safe URLs are processed.
    """
    if validators.url(url_str):
        parsed_url = urlparse(url_str)
        sanitized_url = urlunparse(parsed_url)
        return sanitized_url
    else:
        logging.error(f"Invalid URL provided: {url_str}")
        return None

# Assuming this function already exists and returns a user object if credentials are valid
def verify_refresh_token(refresh_token: str):
    # Placeholder for refresh token verification logic
    # You should validate the refresh token's signature and its expiration
    # Also check if the token has been revoked or is still valid
    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        # Implement additional checks here, such as token revocation or session validity
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
def encode_url_to_filename(url):
    """
    Encodes a URL into a base64 string safe for filenames, after validating and sanitizing.
    Removes padding to ensure filename compatibility.
    """
    sanitized_url = validate_and_sanitize_url(str(url))
    if sanitized_url is None:
        raise ValueError("Provided URL is invalid and cannot be encoded.")
    encoded_bytes = base64.urlsafe_b64encode(sanitized_url.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8').rstrip('=')
    return encoded_str

def decode_filename_to_url(encoded_str: str) -> str:
    """
    Decodes a base64 encoded string back into a URL, adding padding if necessary.
    This reverses the process done by `encode_url_to_filename`.
    """
    padding_needed = 4 - (len(encoded_str) % 4)
    if padding_needed:
        encoded_str += "=" * padding_needed
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')

def generate_links(action: str, qr_filename: str, base_api_url: str, download_url: str) -> List[Link]:
    links = []
    if action in ["list", "create"]:
        links.append(Link(rel="view", href=download_url, action="GET", type="image/png"))
    if action in ["list", "create", "delete"]:
        delete_url = f"{base_api_url}/qr-codes/{qr_filename}"
        links.append(Link(rel="delete", href=delete_url, action="DELETE", type="application/json"))
    return links

def generate_event_links(event_id: int) -> List[Link]:
    return [
        Link(rel="self", href=f"{settings.server_base_url}/events/{event_id}", action="GET", type="application/json"),
        Link(rel="edit", href=f"{settings.server_base_url}/events/{event_id}", action="PUT", type="application/json"),
        Link(rel="delete", href=f"{settings.server_base_url}/events/{event_id}", action="DELETE", type="application/json")
    ]

def generate_pagination_links(page: int, per_page: int, total_pages: int, base_url: str = "/events/") -> List[Link]:
    links = []
    links.append(Link(rel="first", href=f"{SERVER_BASE_URL}{base_url}?page=1&per_page={per_page}", action="GET", type="application/json"))
    links.append(Link(rel="last", href=f"{SERVER_BASE_URL}{base_url}?page={total_pages}&per_page={per_page}", action="GET", type="application/json"))
    
    if page > 1:
        links.append(Link(rel="prev", href=f"{SERVER_BASE_URL}{base_url}?page={page - 1}&per_page={per_page}", action="GET", type="application/json"))
    if page < total_pages:
        links.append(Link(rel="next", href=f"{SERVER_BASE_URL}{base_url}?page={page + 1}&per_page={per_page}", action="GET", type="application/json"))
    
    return links