
"""
File: user_schemas.py

Overview:
This file contains Pydantic models that define the structure, validation, serialization, and deserialization of data for user-related operations in a FastAPI application. These models ensure data integrity and security by enforcing constraints and patterns using Python type annotations and regular expressions. The models also contribute to automatic API documentation generation compatible with the OpenAPI specification.

Pydantic and Data Validation:
Pydantic is a Python library for data validation and settings management using Python type annotations. It ensures that the data received from HTTP requests conforms to the expected structure and types, which is crucial for the security and stability of the application. The models in this file use Pydantic's BaseModel as a base class and define fields with specific types and constraints.

Regular Expressions for Validation:
Regular expressions (regex) are used extensively in the models to define patterns for validating strings, such as usernames and passwords. They provide a powerful way to specify rules for string characters, lengths, and compositions, which are critical for maintaining security standards. For example, the validate_username function uses a regex to ensure that the username only contains letters, numbers, underscores, and hyphens, while the validate_password function checks for password complexity requirements.

Inheritance and Code Reusability:
The models in this file demonstrate the use of inheritance to promote code reusability and maintainability. The UserBase model serves as a base class that defines common fields and validations, which are then inherited by more specific models like UserCreate, UserUpdate, and UserResponse. This approach reduces code duplication and ensures consistency across different parts of the application.

Model-Specific Functionality:
Each model in this file serves a specific purpose within the application:

UserBase: Defines the base structure and validations for user data, including username, email, full name, bio, and profile picture URL.
UserCreate: Extends UserBase and adds a password field for creating new user accounts, with additional validation for password complexity.
UserUpdate: Defines the structure for updating user information, with all fields being optional.
UserResponse: Extends UserBase and includes additional fields that are populated during database queries, such as the user ID, last login timestamp, and creation/update timestamps. It also includes navigational links for HATEOAS compliance.
UserListResponse: Defines the structure for a paginated list of user responses, including the list of users and pagination details.
LoginRequest: Defines the structure for user login requests, including the username and password fields.
ErrorResponse: Defines the structure for error responses, including an error message and optional details.
HATEOAS and OpenAPI Integration:
The UserResponse model includes a links field that contains navigational links related to the user resource, following the HATEOAS (Hypermedia as the Engine of Application State) principle. These links allow clients to discover and navigate through the API dynamically. The models also contribute to the automatic generation of API documentation using FastAPI's integration with the OpenAPI specification, providing a clear and interactive documentation for developers and API consumers.

Security Best Practices:
The models in this file enforce several security best practices:

Input Validation: The models validate incoming data using Pydantic's type annotations and custom validators, ensuring that only properly formatted and constrained data is processed by the application. This helps prevent common security threats like SQL injection and cross-site scripting (XSS).
Password Security: The UserCreate model enforces strong password policies using regex-based validators, reducing the risk of weak passwords and potential brute-force attacks.
Data Serialization and Deserialization: Pydantic handles the secure conversion of data between JSON and Python objects, mitigating risks associated with manual serialization and deserialization.
Overall, the use of Pydantic models in this file contributes to building a secure, validated, and well-documented API for user-related operations in a FastAPI application. The combination of type annotations, regex-based validators, and inheritance promotes code reusability, maintainability, and adherence to security best practices.
"""
# Import required libraries and modules
from datetime import datetime, timezone  # Provides classes for manipulating dates and times in both simple and complex ways.
from urllib.parse import urlparse  # Functions for breaking down and reconstructing URLs.
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator  # Pydantic is used for data validation and settings management using Python type annotations.
from typing import List, Optional  # Standard library typing module, used for constructing complex type hints.
from app.schemas.link_schema import Link  # Custom module, likely provides a schema for links (part of HATEOAS).
from app.schemas.pagination_schema import EnhancedPagination  # Custom pagination schema supporting enriched functionality.
import re  # Provides regular expression matching operations.
import uuid  # Provides immutable UUID objects and functions for generating new UUIDs.

# Define a base user model with common attributes
class UserBase(BaseModel):
    username: str = Field(
        ...,  # Ellipsis is used to indicate that the field is required.
        min_length=3,
        max_length=50,
        description="The unique username of the user. Must be 3-50 characters long. Only letters, numbers, underscores, and hyphens are allowed.",
        example="john_doe_123"
    )
    email: EmailStr = Field(
        ...,
        description="The email address of the user.",
        example="john.doe@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="The full name of the user, if available. Should contain only letters, spaces, hyphens, or apostrophes.",
        example="John Doe"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="A short biography or description of the user.",
        example="I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript."
    )
    profile_picture_url: Optional[str] = Field(
        None,
        description="The URL to the user's profile picture. Must point to a valid image file (e.g., JPEG, PNG).",
        example="https://example.com/profile_pictures/john_doe.jpg"
    )

    # Validators are used to validate the data
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
        return v

    @validator('full_name')
    def validate_full_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("Full name can only contain letters, spaces, hyphens, or apostrophes.")
        return v

    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is None:
            return v  # If the URL is optional, allow None values
        parsed_url = urlparse(v)
        if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
            raise ValueError("Profile picture URL must point to a valid image file (JPEG, PNG).")
        return v

    class Config:
        json_schema_extra = {
            "description": "Base model for user information.",
            "example": {
                "username": "john_doe_123",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "bio": "I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript.",
                "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg"
            }
        }

# Define a model for creating new user accounts with additional attributes like password
class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="A strong password for the user's account. Must be at least 8 characters long and include uppercase and lowercase letters, a digit, and a special character.",
        example="SecurePassword123!"
    )

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        return v

    class Config:
        json_schema_extra = {
            "description": "Model for creating a new user account.",
            "example": {
                "username": "john_doe_123",
                "email": "john.doe@example.com",
                "password": "SecurePassword123!",
                "full_name": "John Doe",
                "bio": "I am a data scientist passionate about machine learning and big data analytics.",
                "profile_picture_url": "https://example.com/profile_pictures/jane_smith.jpg"
            }
        }

# Define a model for updating user information with optional fields
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(
        None,
        description="A new email address for the user.",
        example="john.doe.new@example.com"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="An updated full name for the user.",
        example="John H. Doe"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="An updated biography or description of the user.",
        example="I am a senior software engineer specializing in backend development with Python and Node.js."
    )
    profile_picture_url: Optional[HttpUrl] = Field(
        None,
        description="An updated URL to the user's profile picture.",
        example="https://example.com/profile_pictures/john_doe_updated.jpg"
    )

    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is not None:
            parsed_url = urlparse(str(v))  # Convert the URL object to a string before parsing
            if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
                raise ValueError("Profile picture URL must point to a valid image file (JPEG, PNG).")
        return v

    class Config:
        json_schema_extra = {
            "description": "Model for updating user information.",
            "example": {
                "email": "john.doe.new@example.com",
                "full_name": "John H. Doe",
                "bio": "I am a senior software engineer specializing in backend development with Python and Node.js.",
                "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
            }
        }

# Define a model for the user response, which includes fields populated during queries
class UserResponse(UserBase):
    id: str = Field(
        ...,
        description="The system-generated unique identifier for the user (e.g., UUID).",
        example="a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="A short biography or description of the user.",
        example="I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript."
    )
    last_login_at: Optional[datetime] = Field(
        None,
        description="The timestamp of the user's last successful login, timezone-aware.",
        example="2023-04-09T14:30:00+00:00"
    )
    created_at: datetime = Field(
        ...,
        description="The timestamp when the user account was created, timezone-aware.",
        example="2023-04-01T10:15:30+00:00"
    )
    updated_at: datetime = Field(
        ...,
        description="The timestamp when the user information was last updated, timezone-aware.",
        example="2023-04-05T16:45:00+00:00"
    )
    links: List[Link] = Field(
        [],
        description="Navigational links related to the user for HATEOAS compliance. Includes links for self-reference and updating the user.",
        example=[
            {"rel": "self", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"},
            {"rel": "update", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"}
        ]
    )
    # Custom validator to convert UUID to string
    @validator('id', pre=True, allow_reuse=True)
    def convert_uuid_to_string(cls, value):
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    class Config:
        json_schema_extra = {
            "description": "Model for user response data.",
            "example": {
                "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                "username": "john_doe_123",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "bio": "I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript.",
                "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
                "last_login_at": "2023-04-09T14:30:00+00:00",
                "created_at": "2023-04-01T10:15:30+00:00",
                "updated_at": "2023-04-05T16:45:00+00:00",
                "links": [
                    {"rel": "self", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"},
                    {"rel": "update", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"}
                ]
            }
        }

# Define a model for paginated list of user responses, including pagination details
class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(
        ...,
        description="A list of user responses."
    )
    pagination: EnhancedPagination = Field(
        ...,
        description="Pagination details including the current page, total pages, total items, and navigational links."
    )

    class Config:
        json_schema_extra = {
            "description": "Model for a paginated list of user responses.",
            "example": {
                "items": [
                    {
                        "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                        "username": "john_doe_123",
                        "email": "john.doe@example.com",
                        "full_name": "John Doe",
                        "bio": "I am a software engineer with over 5 years of experience in building scalable web applications using Python and JavaScript.",
                        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
                        "last_login_at": "2023-04-09T14:30:00+00:00",
                        "created_at": "2023-04-01T10:15:30+00:00",
                        "updated_at": "2023-04-05T16:45:00+00:00",
                        "links": [
                            {"rel": "self", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"},
                            {"rel": "update", "href": "https://api.example.com/users/a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"}
                        ]
                    },
                    {
                        "id": "b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7",
                        "username": "jane_smith_456",
                        "email": "jane.smith@example.com",
                        "full_name": "Jane Smith",
                        "bio": "I am a data scientist passionate about machine learning and big data analytics.",
                        "profile_picture_url": "https://example.com/profile_pictures/jane_smith.jpg",
                        "last_login_at": "2023-04-08T09:45:00+00:00",
                        "created_at": "2023-04-02T12:30:00+00:00",
                        "updated_at": "2023-04-06T18:15:00+00:00",
                        "links": [
                            {"rel": "self", "href": "https://api.example.com/users/b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7"},
                            {"rel": "update", "href": "https://api.example.com/users/b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7"}
                        ]
                    }
                ],
                "pagination": {
                    "currentPage": 1,
                    "totalPages": 5,
                    "totalItems": 100,
                    "links": [
                        {"rel": "first", "href": "https://api.example.com/users?page=1"},
                        {"rel": "prev", "href": None},
                        {"rel": "self", "href": "https://api.example.com/users?page=1"},
                        {"rel": "next", "href": "https://api.example.com/users?page=2"},
                        {"rel": "last", "href": "https://api.example.com/users?page=5"}
                    ]
                }
            }
        }

# Define a model for user login requests
class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        description="Username of the user trying to login.",
        example="john_doe_123"
    )
    password: str = Field(
        ...,
        description="Password of the user trying to login.",
        example="SecurePassword123!"
    )

    class Config:
        json_schema_extra = {
            "description": "Model for user login request.",
            "example": {
                "username": "john_doe_123",
                "password": "SecurePassword123!"
            }
        }

# Define a model for error responses in case of issues
class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="A brief description of the error that occurred.",
        example="Invalid username or password."
    )
    details: Optional[str] = Field(
        None,
        description="Additional details about the error, if available.",
        example="The provided username does not exist or the password is incorrect."
    )

    class Config:
        json_schema_extra = {
            "description": "Model for error responses.",
            "example": {
                "error": "Invalid username or password.",
                "details": "The provided username does not exist or the password is incorrect."
            }
        }
