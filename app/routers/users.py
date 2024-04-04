# routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models import models

from ..schemas import schemas
from .. import services
from ..dependencies import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management"])
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.create_user(db=db, user_create=user_create)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.get("/users/", response_model=List[schemas.UserResponse], tags=["User Management"])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["User Management"])
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["User Management"])
def update_user(user_id: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = services.update_user(db=db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User Management"])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    result = services.delete_user(db=db, user_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
