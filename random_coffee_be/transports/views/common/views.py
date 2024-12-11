from typing import Annotated, Any

from fastapi import APIRouter
from fastapi.params import Depends

from random_coffee_be.settings import EnvSettings, get_env_settings

common_router = APIRouter()


@common_router.get("/")
def _get_root(
    settings: Annotated[EnvSettings, Depends(get_env_settings)],
) -> dict[str, Any]:
    return {"version": settings.app_version}
