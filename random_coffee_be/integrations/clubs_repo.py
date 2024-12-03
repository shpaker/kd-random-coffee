from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class ClubsRepo:
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

    async def create_user(
        self,
        club_id: UserModel,
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
