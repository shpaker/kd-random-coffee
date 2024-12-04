from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from ..models.user_clubs import UserClub 

class UserClubService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def join_club(self, user_id: int, club_id: id):
        query = insert(UserClub).values(user_id = user_id, club_id = club_id)
        await self.db.execute(query)
        await self.db.commit()

    async def leave_club(self, user_id: int, club_id: int):
        query = delete(UserClub).where(UserClub.user_id == user_id, UserClub.club_id == club_id)
        await self.db.execute(query)
        await self.db.commit()
#Создаем модель уже существующей таблицы в базе данных Docker