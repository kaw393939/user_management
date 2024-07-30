# email_service.py
from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification",
            'professional_status_update': "Professional Notification Update"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User):
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        await self.send_user_email({
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }, 'email_verification')

    async def send_professional_status_update_email(self, user: User):
        """
        Sends an email to the user with an update on their professional status.

        Args:
            user (User): The user to send the email to.

        Returns:
            None
        """
        # Prepare email data
        # verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        await self.send_user_email({ # Send the email using the 'professional_status_update' template
            "name": user.first_name, # User's first name
            "email": user.email,  # User's email address
            "professional_status": user.professional_status, # User's updated professional status
        }, 'professional_status_update')