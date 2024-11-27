from typing import Annotated, Any

from fastapi import APIRouter, Path
from fastapi.params import Depends

from random_coffee_be.services.users_service import UserService

users_router = APIRouter(prefix="/users")


@users_router.get("/{user_id}")
async def _get_root(
    user_id: Annotated[str, Path()],
    user_service: Annotated[UserService, Depends(UserService)],
) -> dict[str, Any]:
    # some logic
    return {
        "approved_at": await user_service.is_user_approved(user_id),
    }
