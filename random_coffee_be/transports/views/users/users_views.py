from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from random_coffee_be_versia10.services.users_service import UserService, UserCreate, UserResponse
from random_coffee_be_versia10.repositories.user_repository import UserRepository
from random_coffee_be_versia10.depends import get_db

users_router = APIRouter()

@users_router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db=Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.get_user(user_id)

@users_router.post("/user", response_model=UserResponse)
async def create_user(user: UserCreate, db=Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.create_user(user)
