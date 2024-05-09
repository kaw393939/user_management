from builtins import Exception, str, super


class UserNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class EmailAlreadyExistsException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class AccountLockedException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidVerificationTokenException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)