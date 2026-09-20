from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username))

    def identity_exists(self, username: str, email: str | None) -> bool:
        condition = User.username == username
        if email is not None:
            condition = or_(condition, User.email == email)
        return self.db.scalar(select(User.id).where(condition).limit(1)) is not None

    def add(self, user: User) -> None:
        self.db.add(user)
