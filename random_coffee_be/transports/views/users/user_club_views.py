from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..depends import get_db
from ..services.user_club_service import UserClubService

router = APIRouter()

@router.post("/clubs/join")
async def join_club(user_id: int, club_id: int, db: AsyncSession = Depends(get_db)):
    user_club_service = UserClubService(db)
    await user_club_service.join_club(user_id, club_id)
    return {"message": f"User {user_id} joined club {club_id}"}

@router.post("/clubs/leave")
async def leave_club(user_id: int, club_id: int, db: AsyncSession = Depends(get_db)):
    user_club_service = UserClubService(db)
    await user_club_service.leave_club(user_id, club_id)
    return {"message": f"User {user_id} left club {club_id}"}