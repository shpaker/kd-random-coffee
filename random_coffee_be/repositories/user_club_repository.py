from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from random_coffee_be_versia10.models.user_clubs import UserClubs

class UserClubRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def join_club(self, user_id: int, club_id: int):
        query = insert(UserClubs).values(user_id=user_id, club_id=club_id)
        await self.db.execute(query)
        await self.db.commit()

    async def leave_club(self, user_id: int, club_id: int):
        query = delete(UserClubs).where(UserClubs.user_id == user_id, UserClubs.club_id == club_id)
        await self.db.execute(query)
        await self.db.commit()