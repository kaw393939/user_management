"""
File: user_model.py

Overview:
This file defines the `User` data model using SQLAlchemy, a Python library that facilitates Object-Relational Mapping (ORM). ORM allows developers to work with databases using native Python objects instead of writing SQL queries directly. This abstraction enables developers to interact with the database in a more intuitive and object-oriented way.

Relational Database:
A relational database organizes data into one or more tables where data types may be related to each other; these relations help structure the data. SQL (Structured Query Language) is typically used to manage and query data in these databases.

SQLAlchemy:
SQLAlchemy is one of the most feature-rich ORM libraries available in Python. It offers a full suite of tools to handle database interactions, including a powerful ORM layer and a schema migration utility called Alembic. SQLAlchemy ORM allows developers to define Python classes as mappings to database tables, and instances of those classes as rows in those tables.

Alembic:
Alembic is a lightweight database migration tool for use with SQLAlchemy. It tracks database schema changes and applies them incrementally to the database. It is essential for evolving the database schema safely and efficiently without losing data.

Enums in Python:
An Enum (Enumerated type) is a symbolic name for a set of values. Enums help to code clarity by preventing the use of magic numbers and providing validation of acceptable values. Python’s `enum` module defines an enumeration type with iteration and comparison capabilities.

SQLAlchemy Enum:
SQLAlchemy supports Python's native enumeration types to be used in database columns. This feature allows enums to be stored in the database as string or integer values while being used in the code as enum instances, which adds a layer of validation and ease of use in the application code.

Mapped:
SQLAlchemy's `Mapped` type is a hint to type checkers that a class attribute is expected to be mapped to a database column. This helps with IDEs and tools to understand the types without the actual database interaction.

Attributes Explained:
Each attribute in the `User` class represents a column in the database with specific characteristics like data type, constraints, and defaults. Attributes such as `id`, `username`, `email`, etc., are defined with their respective SQL types and constraints such as uniqueness or indexability.
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, func, Enum as SQLAlchemyEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from app.database import Base

class UserRole(Enum):
    """Defines the roles available within the application, stored as ENUM type in the database."""
    ADMIN = "admin"
    USER = "user"
    PRO = "pro"

class User(Base):
    """
    Represents a user entity within the application, mapping to the 'users' table in the database.
    This class leverages SQLAlchemy ORM to map Python code to SQL tables transparently.
    
    The class includes methods to manipulate and query the user data, thus encapsulating the data handling in a high-level module.
    """
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}  # Ensure that SQLAlchemy loads column defaults from the database automatically upon insert.

    # UUID field automatically generated with uuid4, stored as UUID in the PostgreSQL database.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # User's unique username, constrained to be unique and indexed.
    username: Mapped[str] = Column(String(50), unique=True, nullable=False, index=True)
    # User's unique email address, also unique and indexed.
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    # Boolean flag to track email verification status, not nullable and defaults to False.
    email_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    # Storing the hashed password as a string.
    hashed_password: Mapped[str] = Column(String(255), nullable=False)
    # Optional full name of the user.
    full_name: Mapped[str] = Column(String(100), nullable=True)
    # Optional bio of the user, can store up to 500 characters.
    bio: Mapped[str] = Column(String(500), nullable=True)
    # Optional URL to the user's profile picture.
    profile_picture_url: Mapped[str] = Column(String(255), nullable=True)
    # User's role within the application, using SQLAlchemyEnum to map the UserRole enum.
    role: Mapped[UserRole] = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
    # Timestamp of the last successful login attempt.
    last_login_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    # Count of consecutive failed login attempts.
    failed_login_attempts: Mapped[int] = Column(Integer, default=0)
    # Boolean flag to indicate if the user account is locked.
    is_locked: Mapped[bool] = Column(Boolean, default=False)
    # Automatically set timestamp when the user account is created, using the server's current time.
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    # Automatically updated timestamp whenever the user data is updated.
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        """String representation of the User instance, helpful for debugging."""
        return f"<User {self.username}, Role: {self.role.name}>"

    def lock_account(self):
        """Locks the user account, preventing further login attempts in case of security concerns."""
        self.is_locked = True

    def unlock_account(self):
        """Unlocks the user account, allowing the user to attempt to login again."""
        self.is_locked = False

    def has_role(self, role_name: UserRole) -> bool:
        """Checks if the user has a specific role, facilitating role-based access control."""
        return self.role == role_name

    def verify_email(self):
        """Marks the user's email address as verified, updating the database record to reflect this."""
        self.email_verified = True
