from fastapi import HTTPException
from typing import List
from random_coffee_be_versia10.repositories.club_repository import ClubRepository
from random_coffee_be_versia10.services.club_groups import club_groups
from random_coffee_be_versia10.models.club import Club
from datetime import datetime

class ClubService:
    def __init__(self, club_repository: ClubRepository):
        self.club_repository = club_repository
        self.clubs = club_groups

    async def get_clubs(self) -> List[str]:
        return list(self.clubs.keys())

    async def join_club(self, user_id: int, club: str) -> dict:
        if club not in self.clubs:
            raise HTTPException(status_code=404, detail="Club not found")

        user = await self.club_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if club in user.clubs:
            raise HTTPException(status_code=400, detail="User already in club")

        user.clubs.append(club)
        await self.club_repository.update_user_clubs(user_id, user.clubs)
        return {"detail": f"User joined {club}"}

    async def leave_club(self, user_id: int, club: str) -> dict:
        user = await self.club_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if club not in user.clubs:
            raise HTTPException(status_code=400, detail="User not in club")

        user.clubs.remove(club)
        await self.club_repository.update_user_clubs(user_id, user.clubs)
        return {"detail": f"User left {club}"}

    async def create_club(self, name: str, description: str, is_active: bool = True) -> Club:
        db_club = Club(
            name=name,
            description=description,
            is_active=is_active,
            created_at=datetime.utcnow()
        )
        created_club = await self.club_repository.create_club(db_club)
        return created_club