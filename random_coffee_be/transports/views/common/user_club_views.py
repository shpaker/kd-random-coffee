from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from random_coffee_be_versia10.depends import get_db
from random_coffee_be_versia10.services.user_club_service import UserClubService
from random_coffee_be_versia10.repositories.user_club_repository import UserClubRepository

user_club_router = APIRouter()

@user_club_router.post("/clubs/join")
async def join_club(user_id: int, club_id: int, db: AsyncSession = Depends(get_db)):
    user_club_repository = UserClubRepository(db)
    user_club_service = UserClubService(user_club_repository)
    await user_club_service.join_club(user_id, club_id)
    return {"message": f"User {user_id} joined club {club_id}"}

@user_club_router.post("/clubs/leave")
async def leave_club(user_id: int, club_id: int, db: AsyncSession = Depends(get_db)):
    user_club_repository = UserClubRepository(db)
    user_club_service = UserClubService(user_club_repository)
    await user_club_service.leave_club(user_id, club_id)
    return {"message": f"User {user_id} left club {club_id}"}