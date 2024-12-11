from pydantic import BaseModel, validator
from datetime import datetime
from typing import List
from fastapi import HTTPException
from random_coffee_be.repositories.user_repository import UserRepository
from random_coffee_be.models.user import User

class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    status: str
    availability_interval: str
    approved_at: datetime
    is_new: bool
    created_at: datetime

    @validator('approved_at')
    def convert_approved_at_to_naive(cls, v):
        if v.tzinfo:
            return v.replace(tzinfo=None)
        return v

    @validator('created_at')
    def convert_created_at_to_naive(cls, v):
        if v.tzinfo:
            return v.replace(tzinfo=None)
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    status: str
    availability_interval: str
    approved_at: datetime
    is_new: bool
    created_at: datetime

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user.__dict__)

    async def create_user(self, user: UserCreate) -> UserResponse:
        db_user = User(**user.dict())
        created_user = await self.user_repository.create_user(db_user)
        return UserResponse(**created_user.__dict__)