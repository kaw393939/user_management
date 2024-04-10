# app/security.py
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password.startswith('$2b$'):
        raise ValueError(f"Hashed password format is incorrect: {hashed_password}")
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
