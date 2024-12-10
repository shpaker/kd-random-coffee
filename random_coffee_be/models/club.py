from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)  # Исправлено на правильное название поля
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания в UTC
    is_active = Column(Boolean, default=True)

from pydantic import BaseModel

class ClubCreate(BaseModel):
    name: str
    description: str
    is_active: bool = True

class ClubResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    is_active: bool

class Config:
    orm_mode = True

# Этот код создает модель уже существующей базы данных в Docker для выполнения эндпоинтов