from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pytz import UTC

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(255), nullable=False)
    status = Column(String(20))
    availability_interval = Column(String(20))
    approved_at = Column(DateTime)  # Дата утверждения (если есть)
    is_new = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания в UTC

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.convert_approved_at_to_naive()
        self.convert_created_at_to_naive()

    def convert_approved_at_to_naive(self):
        if self.approved_at and self.approved_at.tzinfo:
            self.approved_at = self.approved_at.replace(tzinfo=None)

    def convert_created_at_to_naive(self):
        if self.created_at and self.created_at.tzinfo:
            self.created_at = self.created_at.replace(tzinfo=None)

# Этот код создает модель уже существующей базы данных в Docker для выполнения эндпоинтов