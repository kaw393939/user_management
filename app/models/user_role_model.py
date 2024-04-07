from sqlalchemy import (
    Column, String
    )
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class UserRole(Base):
    """Represents the role of a user."""
    __tablename__ = "user_roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<UserRole {self.name}>"