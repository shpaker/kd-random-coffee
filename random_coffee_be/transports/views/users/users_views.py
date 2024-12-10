from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from random_coffee_be_versia10.services.users_service import UserService, UserCreate, UserResponse
from random_coffee_be_versia10.repositories.user_repository import UserRepository
from random_coffee_be_versia10.depends import get_db
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

users_router = APIRouter()

@users_router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db=Depends(get_db)):
    try:
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)
        return await user_service.get_user(user_id)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@users_router.post("/user", response_model=UserResponse)
async def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)
        return await user_service.create_user(user)
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")