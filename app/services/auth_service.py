from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse


class IdentityAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register(self, data: RegisterRequest) -> User:
        if self.users.identity_exists(data.username, data.email):
            raise IdentityAlreadyExistsError
        user = User(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(data.password.get_secret_value()),
        )
        self.users.add(user)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            # The unique constraint also protects concurrent registrations.
            if self.users.identity_exists(data.username, data.email):
                raise IdentityAlreadyExistsError from exc
            raise
        self.db.refresh(user)
        return user

    def login(self, username: str, password: str) -> TokenResponse:
        user = self.users.get_by_username(username.strip())
        valid = verify_password(password, user.password_hash if user else DUMMY_PASSWORD_HASH)
        if user is None or not valid:
            raise InvalidCredentialsError
        return TokenResponse(access_token=create_access_token(user.id))
