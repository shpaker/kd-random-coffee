from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from models.user import User
from depends import get_db

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    ready_status: bool = False
    clubs: List[str] = []

class UserResponse(BaseModel):
    id: int
    name: str
    ready_status: bool
    clubs: List[str]

class UserStates:
    INIT = "INIT"
    WAITING_NAME = "WAITING_NAME"
    EMAIL_SENT = "EMAIL_SENT"
    WAITING_MODERATION = "WAITING_MODERATION"
    ONBOARDING = "ONBOARDING"
    READY_STATUS = "READY_STATUS"
    CLUBS = "CLUBS"
    CREATE_MEETING = "CREATE_MEETING"

@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user", response_model=dict)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    return {"detail": "User created successfully"}