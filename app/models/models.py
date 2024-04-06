from sqlalchemy import (
    Column, DateTime, String, Text, Boolean, ForeignKey, Integer,
    func, Table
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

# Association Table for many-to-many relationship between Event and Tag
event_tag_table = Table(
    'event_tags', Base.metadata,
    Column('event_id', UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    profile_picture_url = Column(String(255), nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    created_events = relationship("Event", back_populates="creator")
    reviews = relationship("EventReview", back_populates="reviewer")

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    role = Column(String(50), nullable=False)
    user = relationship("User", back_populates="roles")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    events = relationship("Event", secondary=event_tag_table, back_populates="tags")

class Event(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=True)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    qr_code_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    approval = relationship("EventApproval", back_populates="event", uselist=False)
    sections = relationship("EventSection", back_populates="event", cascade="all, delete-orphan")
    creator = relationship("User", back_populates="created_events")
    tags = relationship("Tag", secondary=event_tag_table, back_populates="events")

class EventSection(Base):
    __tablename__ = "event_sections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False)
    title = Column(String(255), nullable=False)  # Added title for each section
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)  # Maximum capacity
    registration_deadline = Column(DateTime, nullable=True)  # Deadline for registration
    additional_info = Column(Text, nullable=True)
    qr_code_path = Column(String(255), nullable=True)
    event = relationship("Event", back_populates="sections")

class EventApproval(Base):
    __tablename__ = "event_approvals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False)
    approved = Column(Boolean, default=False)
    approval_reason = Column(Text, nullable=True)  # Reason for approval
    rejection_reason = Column(Text, nullable=True)  # Reason for rejection
    reviewed_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    reviewed_at = Column(DateTime)
    event = relationship("Event", back_populates="approval")
    reviewed_by = relationship("User")

class EventReview(Base):
    __tablename__ = "event_reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # Rating given by the reviewer
    comment = Column(Text, nullable=True)  # Optional comment
    created_at = Column(DateTime, default=func.now(), nullable=False)
    event = relationship("Event")
    reviewer = relationship("User", back_populates="reviews")

class EventRegistration(Base):
    __tablename__ = "event_registrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    section_id = Column(UUID(as_uuid=True), ForeignKey('event_sections.id'), nullable=False)
    registered_at = Column(DateTime, default=func.now(), nullable=False)
    attended = Column(Boolean, default=False, nullable=False)  # Track attendance
    attended_time = Column(DateTime, nullable=True)  # Time of attendance
    user = relationship("User")
    section = relationship("EventSection")
