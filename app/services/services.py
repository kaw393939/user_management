from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.models import Event, EventSection, EventApproval, EventReview, EventRegistration, Notification, Tag
from typing import List, Optional
from uuid import UUID
from app.models.user_model import User
from app.models.user_role_model import UserRole


class EventService:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        query = select(User).options(selectinload(User.role)).filter(User.id == user_id)
        result = await cls._execute_query(session, query)
        return result.scalars().first() if result else None

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[Event]:
        result = await session.execute(select(Event))
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, event_data: dict) -> Event:
        event = Event(**event_data)
        session.add(event)
        await session.commit()
        return event

    @classmethod
    async def update(cls, session: AsyncSession, event: Event, update_data: dict) -> Event:
        for field, value in update_data.items():
            setattr(event, field, value)
        await session.commit()
        return event

    @classmethod
    async def delete(cls, session: AsyncSession, event: Event) -> None:
        await session.delete(event)
        await session.commit()

class EventSectionService:
    @classmethod
    async def get_by_id(cls, session: AsyncSession, section_id: UUID) -> Optional[EventSection]:
        result = await session.execute(select(EventSection).where(EventSection.id == section_id))
        return result.scalars().first()

    @classmethod
    async def get_by_event_id(cls, session: AsyncSession, event_id: UUID) -> List[EventSection]:
        result = await session.execute(select(EventSection).where(EventSection.event_id == event_id))
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, section_data: dict) -> EventSection:
        section = EventSection(**section_data)
        session.add(section)
        await session.commit()
        return section

    @classmethod
    async def update(cls, session: AsyncSession, section: EventSection, update_data: dict) -> EventSection:
        for field, value in update_data.items():
            setattr(section, field, value)
        await session.commit()
        return section

    @classmethod
    async def delete(cls, session: AsyncSession, section: EventSection) -> None:
        await session.delete(section)
        await session.commit()

class EventApprovalService:
    @classmethod
    async def get_by_event_id(cls, session: AsyncSession, event_id: UUID) -> Optional[EventApproval]:
        result = await session.execute(select(EventApproval).where(EventApproval.event_id == event_id))
        return result.scalars().first()

    @classmethod
    async def create(cls, session: AsyncSession, approval_data: dict) -> EventApproval:
        approval = EventApproval(**approval_data)
        session.add(approval)
        await session.commit()
        return approval

    @classmethod
    async def update(cls, session: AsyncSession, approval: EventApproval, update_data: dict) -> EventApproval:
        for field, value in update_data.items():
            setattr(approval, field, value)
        await session.commit()
        return approval

    @classmethod
    async def delete(cls, session: AsyncSession, approval: EventApproval) -> None:
        await session.delete(approval)
        await session.commit()

class EventReviewService:
    @classmethod
    async def get_by_event_id(cls, session: AsyncSession, event_id: UUID) -> List[EventReview]:
        result = await session.execute(select(EventReview).where(EventReview.event_id == event_id))
        return result.scalars().all()

    @classmethod
    async def get_by_section_id(cls, session: AsyncSession, section_id: UUID) -> List[EventReview]:
        result = await session.execute(select(EventReview).where(EventReview.event_section_id == section_id))
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, review_data: dict) -> EventReview:
        review = EventReview(**review_data)
        session.add(review)
        await session.commit()
        return review

    @classmethod
    async def update(cls, session: AsyncSession, review: EventReview, update_data: dict) -> EventReview:
        for field, value in update_data.items():
            setattr(review, field, value)
        await session.commit()
        return review

    @classmethod
    async def delete(cls, session: AsyncSession, review: EventReview) -> None:
        await session.delete(review)
        await session.commit()

class EventRegistrationService:
    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: UUID) -> List[EventRegistration]:
        result = await session.execute(select(EventRegistration).where(EventRegistration.user_id == user_id))
        return result.scalars().all()

    @classmethod
    async def get_by_section_id(cls, session: AsyncSession, section_id: UUID) -> List[EventRegistration]:
        result = await session.execute(select(EventRegistration).where(EventRegistration.event_section_id == section_id))
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, registration_data: dict) -> EventRegistration:
        registration = EventRegistration(**registration_data)
        session.add(registration)
        await session.commit()
        return registration

    @classmethod
    async def update(cls, session: AsyncSession, registration: EventRegistration, update_data: dict) -> EventRegistration:
        for field, value in update_data.items():
            setattr(registration, field, value)
        await session.commit()
        return registration

    @classmethod
    async def delete(cls, session: AsyncSession, registration: EventRegistration) -> None:
        await session.delete(registration)
        await session.commit()

class NotificationService:
    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: UUID) -> List[Notification]:
        result = await session.execute(select(Notification).where(Notification.user_id == user_id))
        return result.scalars().all()

    @classmethod
    async def get_by_event_id(cls, session: AsyncSession, event_id: UUID) -> List[Notification]:
        result = await session.execute(select(Notification).where(Notification.event_id == event_id))
        return result.scalars().all()

    @classmethod
    async def create(cls, session: AsyncSession, notification_data: dict) -> Notification:
        notification = Notification(**notification_data)
        session.add(notification)
        await session.commit()
        return notification

    @classmethod
    async def update(cls, session: AsyncSession, notification: Notification, update_data: dict) -> Notification:
        for field, value in update_data.items():
            setattr(notification, field, value)
        await session.commit()
        return notification

    @classmethod
    async def delete(cls, session: AsyncSession, notification: Notification) -> None:
        await session.delete(notification)
        await session.commit()