from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from random_coffee_be_versia10.models.user import User
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User:
        try:
            query = select(User).filter(User.id == user_id)
            result = await self.db.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error getting user by id: {e}")
            raise

    async def create_user(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise