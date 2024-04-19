import pytest
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

@pytest.fixture
def email_service():
    template_manager = TemplateManager()  # Assuming you have template loading logic
    return EmailService(template_manager=template_manager)

@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')
    # Manual verification in Mailtrap
