from builtins import bool, str
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> bool:
    """
    Validate the email address using the email-validator library.
    
    Args:
        email (str): Email address to validate.
    
    Returns:
        bool: True if the email is valid, otherwise False.
    """
    try:
        # Validate and get info
        validate_email(email)
        return True
    except EmailNotValidError as e:
        # Email not valid, return False
        print(f"Invalid email: {e}")
        return False