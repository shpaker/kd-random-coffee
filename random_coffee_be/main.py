# Импортируем необходимые модули и функции
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
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Создание базовой модели для SQLAlchemy
Base = declarative_base()

# Асинхронный контекстный менеджер для управления жизненным циклом приложения
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

# Функция для создания FastAPI приложения
def make_app() -> FastAPI:
    # Создаем экземпляр FastAPI с настройками жизненного цикла
    app = FastAPI(
        lifespan=_lifespan,
    )
    # Добавляем маршруты из common_router
    app.include_router(common_router)
    # Добавляем маршруты из users_router
    app.include_router(users_router)
    return app

# Создание и запуск приложения
app = make_app()

#Импорт модулей и функций:
#asynccontextmanager: Для создания асинхронного контекстного менеджера.
#AsyncGenerator, Any: Для типизации.
#FastAPI: Основной класс для создания FastAPI приложения.
#create_async_engine, AsyncSession: Для создания асинхронного движка SQLAlchemy и сессии.
#sessionmaker: Для создания фабрики сессий.
#declarative_base: Для создания базовой модели SQLAlchemy.
#common_router, users_router: Маршруты для добавления в приложение.
#Настройки базы данных:
#DATABASE_URL: Строка подключения к базе данных.
#Создание асинхронного движка SQLAlchemy:
#engine: Создаем движок для работы с базой данных.
#Создание асинхронной сессии:
#async_session: Создаем фабрику сессий для работы с базой данных.
#Создание базовой модели для SQLAlchemy:
#Base: Создаем базовую модель для определения моделей данных.
#Асинхронный контекстный менеджер для управления жизненным циклом приложения:
#_lifespan: Функция, которая выполняется при запуске и завершении приложения.
#При запуске: Инициализирует базу данных.
#При завершении: Закрывает движок базы данных.
#Функция для создания FastAPI приложения:
#make_app: Создает экземпляр FastAPI с настройками жизненного цикла.
#Добавляет маршруты из common_router и users_router.
#Создание и запуск приложения:
#app: Создаем экземпляр приложения с помощью функции make_app.
#Заключение:
#Этот код настраивает FastAPI приложение, создает асинхронный движок SQLAlchemy, добавляет маршруты и управляет жизненным циклом приложения. 
#Каждый шаг объяснен с помощью комментариев, чтобы было понятно, что происходит в каждой строке кода.

