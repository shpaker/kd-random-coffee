from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(255), nullable=False)
    status = Column(String(20))
    availability_interval = Column(String(20))
    approved_at = Column(DateTime)
    is_new = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

#Этот код создает модель уже существующей базы данных в Docker для выполнения эндпоинов 