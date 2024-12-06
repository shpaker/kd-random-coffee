from sqlalchemy.orm import Session
from random_coffee_be_versia10.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user