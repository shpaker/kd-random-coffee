from fastapi import APIRouter, Depends
from typing import List
from random_coffee_be_versia10.services.clubs_service import ClubService
from random_coffee_be_versia10.repositories.club_repository import ClubRepository
from random_coffee_be_versia10.depends import get_db

clubs_router = APIRouter()

@clubs_router.get("/clubs", response_model=List[str])
async def get_clubs(db=Depends(get_db)):
    club_repository = ClubRepository(db)
    club_service = ClubService(club_repository)
    return await club_service.get_clubs()

@clubs_router.post("/clubs/join", response_model=dict)
async def join_club(user_id: int, club: str, db=Depends(get_db)):
    club_repository = ClubRepository(db)
    club_service = ClubService(club_repository)
    return await club_service.join_club(user_id, club)

@clubs_router.post("/clubs/leave", response_model=dict)
async def leave_club(user_id: int, club: str, db=Depends(get_db)):
    club_repository = ClubRepository(db)
    club_service = ClubService(club_repository)
    return await club_service.leave_club(user_id, club)