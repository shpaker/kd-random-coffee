from datetime import datetime
from typing import Annotated

from fastapi.params import Depends

from random_coffee_be.depends import get_users_repo
from random_coffee_be.integrations.users_repo import UsersRepo


class UserService:
    def __init__(
        self,
        users_repo: Annotated[UsersRepo, Depends(get_users_repo)],
    ):
        self._users_repo = users_repo

    async def is_user_approved(
        self,
        user_id: str,
    ) -> datetime | None:
        details = await self._users_repo.get_user_details(user_id)
        return details.approved_at
