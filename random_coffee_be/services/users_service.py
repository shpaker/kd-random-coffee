from pydantic import BaseModel
from datetime import datetime
from typing import List
from fastapi import HTTPException
from random_coffee_be_versia10.repositories.user_repository import UserRepository
from random_coffee_be_versia10.models.user import User

class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    status: str
    availability_interval: str
    approved_at: datetime
    is_new: bool

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    status: str
    availability_interval: str
    approved_at: datetime
    is_new: bool

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