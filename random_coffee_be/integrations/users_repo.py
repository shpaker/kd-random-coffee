from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: str
    created_at: datetime
    approved_at: datetime | None = None


class UsersRepo:
    def __init__(
        self,
        db,
    ) -> None:
        self._db = db

    async def create_user(
        self,
        user: UserModel,
    ) -> None: ...

    async def get_user_details(
        self,
        user_id: str,
    ) -> UserModel:
        return UserModel(
            user_id="1",
            created_at=datetime.now(),
            approved_at=None,
        )
