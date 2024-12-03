from fastapi import HTTPException

from fastapi import APIRouter

from random_coffee_be.integrations._mocks import USERS
from random_coffee_be.models import User

users_router = APIRouter(prefix="/users")


@users_router.post("/user")
async def create_user(user: User):
    USERS[user.tg_id] = user
    return {"detail": "User created successfully"}


@users_router.get("/user")
async def get_user(tg_id: int):
    if tg_id in USERS:
        return USERS[tg_id]
    raise HTTPException(status_code=404, detail="Гнида не найдена")
