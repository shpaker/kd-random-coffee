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

class UserModel(BaseModel):
    user_id: str
    created_at: datetime
    approved_at: Optional[datetime] = None

class UsersRepo:
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

    async def create_user(
        self,
        user: UserModel,
    ) -> None:
        query = insert(users_table).values(
            user_id=user.user_id,
            created_at=user.created_at,
            approved_at=user.approved_at,
        )
        await self._db.execute(query)
        await self._db.commit()

    async def get_user_details(
        self,
        user_id: str,
    ) -> Optional[UserModel]:
        query = select(users_table).where(users_table.c.user_id == user_id)
        result = await self._db.execute(query)
        user = result.fetchone()
        if user:
            return UserModel(
                user_id=user.user_id,
                created_at=user.created_at,
                approved_at=user.approved_at,
            )
        return None