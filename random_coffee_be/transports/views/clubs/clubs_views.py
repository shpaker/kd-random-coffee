from fastapi import APIRouter, Depends
from typing import List
from random_coffee_be.services.clubs_service import ClubService
from random_coffee_be.repositories.club_repository import ClubRepository
from random_coffee_be.depends import get_db

clubs_router = APIRouter()

# Создаем экземпляры ClubRepository и ClubService один раз
def get_club_service(db=Depends(get_db)):
    club_repository = ClubRepository(db)
    return ClubService(club_repository)

@clubs_router.get("/clubs", response_model=List[str], summary="Get all clubs")
async def get_clubs(club_service: ClubService = Depends(get_club_service)):
    return await club_service.get_clubs()

@clubs_router.post("/clubs/join", response_model=dict, summary="Join a club")
async def join_club(user_id: int, club: str, club_service: ClubService = Depends(get_club_service)):
    return await club_service.join_club(user_id, club)

@clubs_router.post("/clubs/leave", response_model=dict, summary="Leave a club")
async def leave_club(user_id: int, club: str, club_service: ClubService = Depends(get_club_service)):
    return await club_service.leave_club(user_id, club)