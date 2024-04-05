from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import User
from app.utils.security import hash_password
from uuid import UUID

async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    """
    Asynchronously create a new user with hashed password and return the user object.
    """
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(db: AsyncSession, user_id: UUID) -> User:
    """
    Asynchronously retrieve a user by their ID.
    """
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    """
    Asynchronously retrieve a list of users, with pagination.
    """
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users

async def update_user(db: AsyncSession, user_id: UUID, username: str = None, email: str = None, password: str = None) -> User:
    """
    Asynchronously update user details.
    """
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.hashed_password = hash_password(password)
        await db.commit()
        return user
    return None

async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    """
    Asynchronously delete a user by their ID.
    """
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
