from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from random_coffee_be_versia10.models.user import User
from random_coffee_be_versia10.models.club import Club

class ClubRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_club_by_name(self, club_name: str) -> Club:
        result = await self.db.execute(select(Club).where(Club.name == club_name))
        return result.scalars().first()

    async def update_user_clubs(self, user_id: int, clubs: list) -> User:
        await self.db.execute(update(User).where(User.id == user_id).values(clubs=clubs))
        await self.db.commit()
        return await self.get_user_by_id(user_id)

    async def create_club(self, club: Club) -> Club:
        self.db.add(club)
        await self.db.commit()
        await self.db.refresh(club)
        return club