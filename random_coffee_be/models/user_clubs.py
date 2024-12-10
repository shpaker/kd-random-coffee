from sqlalchemy import Column, Integer, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserClubs(Base): 
    __tablename__ = "user_clubs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)  # Дата присоединения в UTC

# Этот код создает модель уже существующей базы данных в Docker для выполнения эндпоинтов