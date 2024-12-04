from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .transports.common.views import common_router
from .views.users_views import users_router

# Настройки базы данных
DATABASE_URL = "postgresql+asyncpg://luch1x:Fq12Ww@localhost:5432/KODE-practice"

# Создание асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронной сессии
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Создание базовой модели для SQLAlchemy
Base = declarative_base()

# Асинхронный контекстный менеджер для управления жизненным циклом приложения
@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print(f"OUR FRIENDLY {app} STARTUP")
    
    # Инициализируем базу данных
    async with engine.begin() as transaction:
        await transaction.run_sync(Base.metadata.create_all)
        
    try:
        yield
    finally:
        print(f"OUR FRIENDLY {app} SHUTDOWN")
        await engine.dispose()

# Создание FastAPI приложения
app = FastAPI(lifespan=_lifespan)

# Добавляем маршруты из common_router
app.include_router(common_router)

# Добавляем маршруты из users_router
app.include_router(users_router)
