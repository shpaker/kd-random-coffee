from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import get_app_settings
from typing import AsyncGenerator

settings = get_app_settings()

engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор для получения сессии базы данных."""
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        # Обрабатываем возможные исключения
        raise e
