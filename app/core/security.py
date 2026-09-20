from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()
# Verify a dummy hash too when the username does not exist.
DUMMY_PASSWORD_HASH = password_hasher.hash("dummy-password-for-timing")


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    now = datetime.now(UTC)
    # PyJWT's optional cryptography key types are unresolved; our key is str.
    return jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
            "type": "access",
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    # PyJWT's optional cryptography key types are unresolved; our key is str.
    payload = jwt.decode(  # pyright: ignore[reportUnknownMemberType]
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "iat", "exp", "type"]},
    )
    subject = payload["sub"]
    if payload["type"] != "access" or not isinstance(subject, str):
        raise jwt.InvalidTokenError("Invalid access token")
    if not subject.isascii() or not subject.isdecimal() or len(subject) > 10:
        raise jwt.InvalidTokenError("Invalid subject")
    user_id = int(subject)
    if not 0 < user_id <= 2_147_483_647:
        raise jwt.InvalidTokenError("Invalid subject")
    return user_id
