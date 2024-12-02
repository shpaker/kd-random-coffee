from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
from unittest.mock import Base

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from random_coffee_be.transports.views.common.views import common_router
from random_coffee_be.transports.views.users.views import users_router

# Настройки базы данных
DATABASE_URL = "postgresql+asyncpg://luch1x:Fq12Ww@localhost:5432/KODE-practice"

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронной сессии
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

@asynccontextmanager
async def _lifespan(
    app: FastAPI,
) -> AsyncGenerator[dict[str, Any], None]:
    print(f"OUR FRIENDLY {app} STARTUP")
    # Инициализация базы данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield {
        "db_engine": engine,
    }
    print(f"OUR FRIENDLY {app} SHUTDOWN")
    # Закрытие движка
    await engine.dispose()

def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
    )
    app.include_router(common_router)
    app.include_router(users_router)
    return app

# Создание и запуск приложения
app = make_app()