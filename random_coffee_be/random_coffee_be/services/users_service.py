# Импортируем необходимые модули и функции
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from ..models.user import User

# Сервис для работы с пользователями
class UsersService:
    def __init__(self, db: AsyncSession):
        self.db = db  # Сохраняем сессию базы данных

    # Метод для получения пользователя по его Telegram ID
    async def get_user_by_tg_id(self, id: str):
        # Создаем запрос на выборку пользователя по Telegram ID
        query = select(User).where(User.id == id)
        # Выполняем запрос
        result = await self.db.execute(query)
        # Возвращаем первый результат или None, если пользователь не найден
        return result.scalars().first()

    # Метод для создания нового пользователя
    async def create_user(self, id: str):
        # Создаем запрос на вставку нового пользователя
        query = insert(User).values(id = id)
        # Выполняем запрос
        await self.db.execute(query)
        # Фиксируем транзакцию
        await self.db.commit()

# Создаем модель уже существующей таблицы в базе данных Docker
from sqlalchemy import Table, MetaData

# Определяем метаданные для таблицы
metadata = MetaData()

# Определяем таблицу users с автоматической загрузкой структуры из базы данных
users_table = Table(
    "users",
    metadata,
    autoload_with="postgresql+asyncpg://luch1x:Fq12Ww@localhost:5432/KODE-practice",  # Используем существующую базу данных
)