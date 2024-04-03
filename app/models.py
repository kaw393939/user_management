# models.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

class Event(Base):
    __tablename__ = "events"
    # Use UUID as the primary key type for better scalability and uniqueness across distributed systems
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # Limit title length to 255 characters, which is a common practice for short text fields
    title = Column(String(255), nullable=False, index=True)
    # Use Text for potentially long descriptions, PostgreSQL has efficient handling for large text fields
    description = Column(Text, nullable=True)
    # Ensure start_date and end_date are not nullable to enforce data integrity
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
