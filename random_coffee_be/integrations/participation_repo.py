from sqlalchemy.ext.asyncio import AsyncSession


class ParticipationRepo:
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

    async def create(
        self,
        user_id: str,
        club_id: str,
    ) -> bool:
        # создать запись в таблице связи пользователя и клубов (один ко многим)
        return True
