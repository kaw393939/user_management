# app/services/user_service.py
from sqlalchemy.orm import Session
from app.models.models import User
from app.utils.security import hash_password
from uuid import UUID

def create_user(db: Session, username: str, email: str, password: str) -> User:
    """
    Create a new user with hashed password and return the user object.
    """
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: UUID) -> User:
    """
    Retrieve a user by their ID.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """
    Retrieve a list of users, with pagination.
    """
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: UUID, username: str = None, email: str = None, password: str = None) -> User:
    """
    Update user details.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.hashed_password = hash_password(password)
        db.commit()
        return user
    return None

def delete_user(db: Session, user_id: UUID) -> bool:
    """
    Delete a user by their ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
