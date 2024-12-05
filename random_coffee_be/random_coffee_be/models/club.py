from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key = True, index = True)
    name = Column (String(255), unique=True, nullable = False)
    decription = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

#Этот код создает модель уже существующей базы данных в Docker для выполнения эндпоинов 
