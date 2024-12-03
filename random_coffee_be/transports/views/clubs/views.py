from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from random_coffee_be.integrations._mocks import USERS, CLUBS
from random_coffee_be.services.clubs_service import (
    ClubJoinResponse,
    ParticipationService,
)

clubs_router = APIRouter(prefix="/clubs")


@clubs_router.get("/clubs")
async def get_club():
    return CLUBS


# "Clean Code" "Чистый код" Боб Мартин
@clubs_router.post(
    "/club/join",
    response_model=ClubJoinResponse,
)
async def join_club(
    tg_id: str,
    club: str,
    service: Annotated[ParticipationService, Depends(ParticipationService)],
) -> ClubJoinResponse:
    return await service.club_join(
        user_id=tg_id,
        club_id=club,
    )


@clubs_router.post("/club/leave")
async def leave_club(tg_id: int, club: str):
    if tg_id in USERS:
        if club in USERS[tg_id].clubs:
            USERS[tg_id].clubs.remove(club)
            return {"detail": f"The user removed in the {club}"}
        else:
            raise HTTPException(
                status_code=404, detail="Пользователь не находится в клубе"
            )
    raise HTTPException(status_code=404, detail="Гнида не найдена")
