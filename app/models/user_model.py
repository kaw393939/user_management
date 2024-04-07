from sqlalchemy import (
    Column, DateTime, String, ForeignKey, Integer,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class User(Base):
    """Represents a user."""
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    profile_picture_url = Column(String(255), nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    role_id = Column(UUID(as_uuid=True), ForeignKey('user_roles.id'), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    role = relationship("UserRole", back_populates="users", lazy='joined')
    created_events = relationship("Event", back_populates="creator")
    reviews = relationship("EventReview", back_populates="reviewer")
    notifications = relationship("Notification", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def has_role(self, role_name):
        """Checks if the user has a specific role."""
        return self.role.name == role_name
