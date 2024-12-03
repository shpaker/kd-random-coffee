from typing import Annotated, Any

from fastapi import Request
from fastapi.params import Depends

from random_coffee_be.integrations.participation_repo import ParticipationRepo
from random_coffee_be.integrations.users_repo import UsersRepo


def get_db_depends(
    request: Request,
):
    return request.state.db_engine


def get_users_repo(
    db_engine: Annotated[Any, Depends(get_db_depends)],
) -> UsersRepo:
    return UsersRepo(db_engine)


def get_participation_repo(
    db_engine: Annotated[Any, Depends(get_db_depends)],
) -> ParticipationRepo:
    return ParticipationRepo(db_engine)
