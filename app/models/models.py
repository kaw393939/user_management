from sqlalchemy import (
    Column, DateTime, String, Text, Boolean, ForeignKey, Integer,
    func, Table, Index, Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base
from app.models.user_model import User
from app.models.user_role_model import UserRole

# Association Table for many-to-many relationship between Event and Tag
event_tag_table = Table(
    'event_tags', Base.metadata,
    Column('event_id', UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    """Represents a tag for an event."""
    __tablename__ = "tags"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    events = relationship("Event", secondary=event_tag_table, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"


class Event(Base):
    """Represents an event."""
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(Enum("pending", "approved", "rejected", name="event_status_enum"), default="pending", nullable=False)
    is_public = Column(Boolean, default=True)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    qr_code_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    creator = relationship("User", back_populates="created_events")
    sections = relationship("EventSection", back_populates="event", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=event_tag_table, back_populates="events")
    approval = relationship("EventApproval", back_populates="event", uselist=False)
    reviews = relationship("EventReview", back_populates="event")
    notifications = relationship("Notification", back_populates="event")

    def __repr__(self):
        return f"<Event {self.title}>"

    def is_approved(self):
        """Checks if the event is approved."""
        return self.status == EventStatus.APPROVED

class EventSection(Base):
    """Represents a section of an event."""
    __tablename__ = "event_sections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=False)
    registration_deadline = Column(DateTime, nullable=True)
    additional_info = Column(Text, nullable=True)
    qr_code_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    event = relationship("Event", back_populates="sections")
    registrations = relationship("EventRegistration", back_populates="event_section", lazy='dynamic')
    reviews = relationship("EventReview", back_populates="event_section")

    def __repr__(self):
        return f"<EventSection {self.title}>"

    def is_capacity_reached(self):
        """Checks if the section has reached its capacity."""
        return self.registrations.count() >= self.capacity

class EventApproval(Base):
    """Represents the approval status of an event."""
    __tablename__ = "event_approvals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False, index=True)
    approved = Column(Boolean, default=False)
    approval_reason = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=func.now(), nullable=False)
    reviewed_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True, index=True)
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    event = relationship("Event", back_populates="approval")
    reviewed_by = relationship("User")

    def __repr__(self):
        return f"<EventApproval {self.event_id}>"

class EventReview(Base):
    """Represents a review of an event."""
    __tablename__ = "event_reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False, index=True)
    event_section_id = Column(UUID(as_uuid=True), ForeignKey('event_sections.id'), nullable=False, index=True)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    event = relationship("Event", back_populates="reviews")
    event_section = relationship("EventSection", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<EventReview {self.id}>"

class EventRegistration(Base):
    """Represents a registration for an event."""
    __tablename__ = "event_registrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    event_section_id = Column(UUID(as_uuid=True), ForeignKey('event_sections.id'), nullable=False, index=True)
    registered_at = Column(DateTime, default=func.now(), nullable=False)
    attended = Column(Boolean, default=False, nullable=False)
    attended_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    user = relationship("User")
    event_section = relationship("EventSection", back_populates="registrations")

    def __repr__(self):
        return f"<EventRegistration {self.id}>"

class Notification(Base):
    """Represents a notification for a user."""
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    user = relationship("User", back_populates="notifications")
    event = relationship("Event", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id}>"