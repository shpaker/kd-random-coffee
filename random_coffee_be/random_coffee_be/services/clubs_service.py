from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.club import Club
from club_groups import club_groups  # Импорт модуля с данными о группах

class ClubsService:
    def __init__(self, db: AsyncSession):
        self.db = db  # Сохраняем сессию базы данных
        self.club_groups = club_groups.club_groups  # Добавляем данные о группах к объекту сервиса

    # Метод для получения всех клубов
    async def get_all_clubs(self):
        # Создаем запрос на выборку всех клубов
        query = select(Club)
        # Выполняем запрос
        result = await self.db.execute(query)
        # Возвращаем все результаты в виде списка
        return result.scalars().all()

    # Пример метода, использующего данные о группах
    async def get_club_by_group_name(self, group_name):
        if group_name in self.club_groups:
            query = select(Club).where(Club.name == group_name)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        else:
            raise ValueError(f"Group {group_name} not found")