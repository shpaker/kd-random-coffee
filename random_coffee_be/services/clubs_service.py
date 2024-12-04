# Импортируем необходимые модули и функции
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.club import Club

# Сервис для работы с клубами
class ClubsService:
    def __init__(self, db: AsyncSession):
        self.db = db  # Сохраняем сессию базы данных
    
    # Метод для получения всех клубов
    async def get_all_clubs(self):
        # Создаем запрос на выборку всех клубов
        query = select(Club)
        # Выполняем запрос
        result = await self.db.execute(query)
        # Возвращаем все результаты в виде списка
        return result.scalars().all()