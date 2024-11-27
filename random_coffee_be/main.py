from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI

from random_coffee_be.transports.views.common.views import common_router
from random_coffee_be.transports.views.users.views import users_router

app = FastAPI()


@asynccontextmanager
async def _lifespan(
    app: FastAPI,
) -> AsyncGenerator[dict[str, Any], None]:
    print(f"OUR FRIENDLY {app} STARTUP")
    # # тут должно быть что-то в духе get_db_engine()
    # db_engine = 'get_db_engine()'
    yield {
        "db_engine": "db_engine",  # тут, конечно же должен быть реальный объект
    }
    print(f"OUR FRIENDLY {app} SHUTDOWN")
    # # закрытие движка
    # await db_engine.dispose()


def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
    )
    app.include_router(common_router)
    app.include_router(users_router)
    return app
