import pytest
from datetime import datetime, timedelta
from app.models.models import Event, EventSection, EventApproval, EventReview, EventRegistration, Notification
from app.services.services import EventService, EventSectionService, EventApprovalService, EventReviewService, EventRegistrationService, NotificationService
from app.models.user_model import User
pytestmark = pytest.mark.asyncio


async def test_event_section_service(db_session, event, event_section):
    # Test get_by_id
    retrieved_section = await EventSectionService.get_by_id(db_session, event_section.id)
    assert retrieved_section == event_section

    # Test get_by_event_id
    event_sections = await EventSectionService.get_by_event_id(db_session, event.id)
    assert event_section in event_sections

    # Test create
    new_section_data = {
        "event_id": event.id,
        "title": "New Section",
        "start_date": event_section.start_date + timedelta(days=1),
        "end_date": event_section.end_date + timedelta(days=1),
        "capacity": 50
    }
    new_section = await EventSectionService.create(db_session, new_section_data)
    assert new_section.title == "New Section"
    assert new_section.capacity == 50

    # Test update
    update_data = {"title": "Updated Section Title"}
    updated_section = await EventSectionService.update(db_session, new_section, update_data)
    assert updated_section.title == "Updated Section Title"

    # Test delete
    await EventSectionService.delete(db_session, new_section)
    deleted_section = await EventSectionService.get_by_id(db_session, new_section.id)
    assert deleted_section is None

async def test_event_approval_service(db_session, event, event_approval):
    # Test get_by_event_id
    retrieved_approval = await EventApprovalService.get_by_event_id(db_session, event.id)
    assert retrieved_approval == event_approval

    # Test create
    new_approval_data = {
        "event_id": event.id,
        "approved": False,
        "rejection_reason": "Test rejection reason"
    }
    new_approval = await EventApprovalService.create(db_session, new_approval_data)
    assert new_approval.approved is False
    assert new_approval.rejection_reason == "Test rejection reason"

    # Test update
    update_data = {"approved": True}
    updated_approval = await EventApprovalService.update(db_session, new_approval, update_data)
    assert updated_approval.approved is True

    # Test delete
    await EventApprovalService.delete(db_session, new_approval)
    deleted_approval = await EventApprovalService.get_by_event_id(db_session, event.id)
    assert deleted_approval == event_approval

    # Clean up the event_approval fixture
    await EventApprovalService.delete(db_session, event_approval)
    fixture_approval = await EventApprovalService.get_by_event_id(db_session, event.id)
    assert fixture_approval is None

async def test_event_review_service(db_session, event, event_section, event_review):
    # Test get_by_event_id
    event_reviews = await EventReviewService.get_by_event_id(db_session, event.id)
    assert event_review in event_reviews

    # Test get_by_section_id
    section_reviews = await EventReviewService.get_by_section_id(db_session, event_section.id)
    assert event_review in section_reviews

    # Test create
    new_review_data = {
        "event_id": event.id,
        "event_section_id": event_section.id,
        "reviewer_id": event_review.reviewer_id,
        "rating": 3,
        "comment": "Test review comment"
    }
    new_review = await EventReviewService.create(db_session, new_review_data)
    assert new_review.rating == 3
    assert new_review.comment == "Test review comment"

    # Test update
    update_data = {"rating": 4}
    updated_review = await EventReviewService.update(db_session, new_review, update_data)
    assert updated_review.rating == 4

    # Test delete
    await EventReviewService.delete(db_session, new_review)
    deleted_review = await EventReviewService.get_by_event_id(db_session, event.id)
    assert new_review not in deleted_review

async def test_event_registration_service(db_session, user, event_section, event_registration):
    # Test get_by_user_id
    user_registrations = await EventRegistrationService.get_by_user_id(db_session, user.id)
    assert event_registration in user_registrations

    # Test get_by_section_id
    section_registrations = await EventRegistrationService.get_by_section_id(db_session, event_section.id)
    assert event_registration in section_registrations

    # Test create
    new_registration_data = {
        "user_id": user.id,
        "event_section_id": event_section.id
    }
    new_registration = await EventRegistrationService.create(db_session, new_registration_data)
    assert new_registration.user_id == user.id
    assert new_registration.event_section_id == event_section.id

    # Test update
    update_data = {"attended": True}
    updated_registration = await EventRegistrationService.update(db_session, new_registration, update_data)
    assert updated_registration.attended is True

    # Test delete
    await EventRegistrationService.delete(db_session, new_registration)
    deleted_registration = await EventRegistrationService.get_by_user_id(db_session, user.id)
    assert new_registration not in deleted_registration

async def test_notification_service(db_session, user, event, notification):
    # Test get_by_user_id
    user_notifications = await NotificationService.get_by_user_id(db_session, user.id)
    assert notification in user_notifications

    # Test create
    new_notification_data = {
        "user_id": user.id,
        "event_id": event.id,
        "message": "Test notification message"
    }
    new_notification = await NotificationService.create(db_session, new_notification_data)
    assert new_notification.user_id == user.id
    assert new_notification.event_id == event.id
    assert new_notification.message == "Test notification message"

    # Test delete
    await NotificationService.delete(db_session, new_notification)
    deleted_notification = await NotificationService.get_by_user_id(db_session, user.id)
    assert new_notification not in deleted_notification