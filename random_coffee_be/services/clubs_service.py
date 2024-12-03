from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from random_coffee_be.depends import get_participation_repo
from random_coffee_be.integrations._mocks import USERS
from random_coffee_be.integrations.participation_repo import ParticipationRepo


class ClubJoinResponse(BaseModel):
    detail: str


class ParticipationService:
    def __init__(
        self,
        participation_repo: Annotated[
            ParticipationRepo,
            Depends(get_participation_repo),
        ],
    ) -> None:
        self._participation_repo = participation_repo

    async def club_join(
        self,
        user_id: str,
        club_id: str,
    ) -> ClubJoinResponse:
        if user_id not in USERS:
            raise HTTPException(
                status_code=404,
                detail="Гнида не найдена",
            )
        if await self._participation_repo.create(
            user_id=user_id,
            club_id=club_id,
        ):
            raise HTTPException(
                status_code=404,
                detail="Гнида не найдена",
            )
        return ClubJoinResponse(detail=f"The user appeared in the {club_id}")
