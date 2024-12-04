# Импортируем необходимые модули и функции
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, Table, MetaData

# Определение таблицы users
metadata = MetaData()
users_table = Table(
    "users",
    metadata,
    autoload_with="postgresql+asyncpg://luch1x:Fq12Ww@localhost:5432/KODE-practice",  # Используем существующую базу данных
)

# Определение модели данных для пользователя
class UserModel(BaseModel):
    user_id: int
    created_at: datetime
    approved_at: Optional[datetime] = None

# Репозиторий для работы с пользователями
class UsersRepo:
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db  # Сохраняем сессию базы данных

    # Метод для создания нового пользователя
    async def create_user(
        self,
        user: UserModel,
    ) -> None:
        # Создаем запрос на вставку данных в таблицу users
        query = insert(users_table).values(
            user_id=user.user_id,
            created_at=user.created_at,
            approved_at=user.approved_at,
        )
        # Выполняем запрос
        await self._db.execute(query)
        # Фиксируем транзакцию
        await self._db.commit()

    # Метод для получения деталей пользователя по его ID
    async def get_user_details(
        self,
        user_id: str,
    ) -> Optional[UserModel]:
        # Создаем запрос на выборку данных из таблицы users
        query = select(users_table).where(users_table.c.user_id == user_id)
        # Выполняем запрос
        result = await self._db.execute(query)
        # Получаем первую строку результата
        user = result.fetchone()
        if user:
            # Если пользователь найден, возвращаем его данные в виде модели UserModel
            return UserModel(
                user_id=user.user_id,
                created_at=user.created_at,
                approved_at=user.approved_at,
            )
        # Если пользователь не найден, возвращаем None
        return None