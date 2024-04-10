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
    """Defines the roles available within the application."""
    ADMIN = "admin"
    USER = "user"
    PRO = "pro"

class User(Base):
    """
    Represents a user entity, enhanced with an enum for role management to ensure consistency and
    ease of use across the application. The use of enums also facilitates generating comprehensive
    and accurate OpenAPI documentation.

    Attributes:
        id (UUID): Auto-generated unique identifier.
        username (str): Unique username, validated for uniqueness and format.
        email (str): Unique email address.
        hashed_password (str): Securely stored hashed password.
        full_name (str, optional): User's full name.
        bio (str, optional): Short biography or description.
        profile_picture_url (str, optional): URL to the profile picture.
        role (UserRole): Enum representing the user's role.
        last_login_at (DateTime, optional): Timestamp of the last login, timezone-aware.
        failed_login_attempts (int): Counter for failed login attempts.
        created_at (DateTime): Timestamp when the account was created, timezone-aware.
        updated_at (DateTime): Timestamp of the last update, timezone-aware.
    """
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, doc="Unique identifier for the user."
    )
    username: Mapped[str] = Column(String(50), unique=True, nullable=False, index=True, doc="User's username, must be unique.")
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True, doc="User's email address, must be unique.")
    hashed_password: Mapped[str] = Column(String(255), nullable=False, doc="User's hashed password for security.")
    full_name: Mapped[str] = Column(String(100), nullable=True, doc="User's full name.")
    bio: Mapped[str] = Column(String(500), nullable=True, doc="Short biography or description of the user.")
    profile_picture_url: Mapped[str] = Column(String(255), nullable=True, doc="URL to the user's profile picture.")
    role: Mapped[UserRole] = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False, doc="Role of the user in the application.")
    last_login_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True, doc="Timestamp of the user's last login, timezone-aware.")
    failed_login_attempts: Mapped[int] = Column(Integer, default=0, doc="Number of consecutive failed login attempts.")
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Timestamp when the user record was created, timezone-aware.")
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Timestamp when the user record was last updated, timezone-aware.")

    def __repr__(self) -> str:
        """
        Provides a string representation of the User object for debugging and logging,
        including the user's username and role.
        """
        return f"<User {self.username}, Role: {self.role.name}>"

    def has_role(self, role_name: UserRole) -> bool:
        """
        Checks if the user has a specific role by comparing the role enum.

        Parameters:
            role_name (UserRole): The role to check.

        Returns:
            bool: True if the user has the specified role, False otherwise.
        """
        return self.role == role_name
