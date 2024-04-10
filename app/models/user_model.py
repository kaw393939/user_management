"""
This Python file defines the User model using SQLAlchemy ORM (Object-Relational Mapping), 
a technique that connects the objects of an application to tables in a relational database. 
In this context, SQLAlchemy acts as the ORM and provides a systematic way to create, 
read, update, and delete database entries using high-level entities such as classes, 
instances, and attributes instead of direct SQL statements.

The User model represents the structure of the 'users' table in the database, including 
its columns and their attributes (like data types, constraints, etc.). This model is used 
throughout the application to interact with user-related data, ensuring that operations 
are performed in an object-oriented manner.

Key Components Explained:
- `__tablename__`: Specifies the name of the table in the database to which this model maps.
- `__mapper_args__`: Configuration options for the mapper. Here, `eager_defaults` is set to True
  to ensure that SQLAlchemy fetches defaults, such as the database-generated UUID, eagerly upon 
  inserting a new record.
- Columns: Define the fields in the database table, along with their data types and constraints. 
  For example, `username` is a string of up to 50 characters and must be unique across all records.
- `default=uuid.uuid4`: Automatically generates a new UUID for each record upon creation.
- `default=func.now()`: Uses the current timestamp from the database server as the default value 
  for the `created_at` and `updated_at` fields. `onupdate=func.now()` ensures `updated_at` 
  is automatically updated to the current timestamp every time a record is updated.
- `__repr__`: A special method used to represent a class's objects as a string, providing 
  a more readable representation of the user object, primarily useful for debugging.
  
By defining models like `User`, the application can leverage SQLAlchemy's ORM capabilities 
to abstract and simplify database operations, making code more maintainable and scalable.
"""

from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Integer,
    func
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
import uuid
from app.database import Base

class User(Base):
    """
    Represents a user entity within the application, mapping to the 'users' table in the database.
    Enhanced to ensure timezone awareness in datetime fields and to adhere to best practices in 
    ORM modeling with SQLAlchemy.
    """
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="Unique identifier for the user")
    username = Column(String(50), unique=True, nullable=False, index=True, comment="User's username, must be unique")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="User's email address, must be unique")
    hashed_password = Column(String(255), nullable=False, comment="User's hashed password for security")
    full_name = Column(String(100), nullable=True, comment="User's full name")
    bio = Column(String(500), nullable=True, comment="Short biography or description about the user")
    profile_picture_url = Column(String(255), nullable=True, comment="URL to the user's profile picture")
    last_login_at = Column(DateTime(timezone=True), nullable=True, comment="Timestamp of the user's last login, timezone-aware")
    failed_login_attempts = Column(Integer, default=0, comment="Number of consecutive failed login attempts")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="Timestamp when the user record was created, timezone-aware")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment="Timestamp when the user record was last updated, timezone-aware")
    
    def __repr__(self):
        """Provides a string representation of the User object."""
        return f"<User {self.username}>"
