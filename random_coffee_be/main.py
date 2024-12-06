from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from random_coffee_be_versia10.transports.views.common.views import common_router
from random_coffee_be_versia10.transports.views.users.users_views import users_router
from random_coffee_be_versia10.transports.views.clubs.clubs_views import clubs_router
from random_coffee_be_versia10.transports.views.common.user_club_views import user_club_router

from random_coffee_be_versia10.models.user_manager import UserManager
from random_coffee_be_versia10.config import TOKEN, MODER, MODER_1

if __name__ == "__main__":
    user_manager = UserManager()
    print("Loaded users: ", user_manager.users)

DATABASE_URL = "postgresql+asyncpg://luch1x:Fq12Ww@localhost:5432/KODE-practice"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

@asynccontextmanager
async def _lifespan(
    app: FastAPI,
) -> AsyncGenerator[dict[str, Any], None]:
    print(f"OUR FRIENDLY {app} STARTUP")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield {
        "db_engine": engine,
    }
    print(f"OUR FRIENDLY {app} SHUTDOWN")
    await engine.dispose()

def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
    )
    app.include_router(common_router)
    app.include_router(users_router)
    app.include_router(clubs_router)
    app.include_router(user_club_router)
    return app

app = make_app()