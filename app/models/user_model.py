from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    func,
    Enum as SQLAlchemyEnum
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
    Represents a user entity within the application, mapping to the 'users' table in the database.
    Enhanced to include role management, account lock functionality, and email verification status
    for improved security and administrative control.

    Attributes:
        id (UUID): Auto-generated unique identifier.
        username (str): User's unique username.
        email (str): User's unique email address.
        email_verified (bool): Indicates if the user's email address has been verified.
        hashed_password (str): Hashed password for secure storage.
        full_name (str, optional): Full name of the user.
        bio (str, optional): A short biography or personal description.
        profile_picture_url (str, optional): URL to the user's profile picture.
        role (UserRole): The role assigned to the user within the application.
        last_login_at (DateTime, optional): Timestamp of the last successful login attempt.
        failed_login_attempts (int): Count of consecutive failed login attempts.
        is_locked (bool): Indicates if the user account is locked.
        created_at (DateTime): Timestamp when the user account was created.
        updated_at (DateTime): Timestamp when the user account was last updated.
    """
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = Column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    email_verified: Mapped[bool] = Column(Boolean, default=False, nullable=False, doc="Indicates if the user's email address has been verified.")
    hashed_password: Mapped[str] = Column(String(255), nullable=False)
    full_name: Mapped[str] = Column(String(100), nullable=True)
    bio: Mapped[str] = Column(String(500), nullable=True)
    profile_picture_url: Mapped[str] = Column(String(255), nullable=True)
    role: Mapped[UserRole] = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
    last_login_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts: Mapped[int] = Column(Integer, default=0)
    is_locked: Mapped[bool] = Column(Boolean, default=False, doc="Indicates if the user account is locked due to security reasons.")
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<User {self.username}, Role: {self.role.name}>"

    def lock_account(self):
        """Locks the user account, preventing login."""
        self.is_locked = True

    def unlock_account(self):
        """Unlocks the user account, allowing login."""
        self.is_locked = False

    def has_role(self, role_name: UserRole) -> bool:
        """Checks if the user has a specific role."""
        return self.role == role_name

    def verify_email(self):
        """Marks the user's email address as verified."""
        self.email_verified = True