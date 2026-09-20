from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import jwt
import pytest
from fastapi.testclient import TestClient
from httpx2 import Response
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User

type AuthClient = tuple[TestClient, Engine]


@pytest.fixture
def auth_client() -> Generator[AuthClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Auth only needs users. Never connect to the application's database.
    Base.metadata.create_all(engine, tables=[Base.metadata.tables[User.__tablename__]])

    def override_db() -> Generator[Session, None, None]:
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(app) as client:
            yield client, engine
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def register(client: TestClient, **overrides: str | None) -> Response:
    payload = {"username": "alice", "password": "password-for-test", "email": "alice@example.com"}
    return client.post("/api/v1/auth/register", json=payload | overrides)


def test_register_login_and_me(auth_client: AuthClient) -> None:
    client, engine = auth_client
    response = register(client)
    assert response.status_code == 201
    user_id = response.json()["id"]
    assert "password" not in response.json()
    assert "password_hash" not in response.json()
    with Session(engine) as db:
        user = db.scalar(select(User))
        assert user is not None
        assert user.password_hash != "password-for-test"
        assert verify_password("password-for-test", user.password_hash)

    response = client.post(
        "/api/v1/auth/login", data={"username": "alice", "password": "password-for-test"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {response.json()['access_token']}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert "password_hash" not in response.json()


@pytest.mark.parametrize("overrides", [{"email": "other@example.com"}, {"username": "bob"}])
def test_duplicate_identity(auth_client: AuthClient, overrides: dict[str, str | None]) -> None:
    client, _ = auth_client
    assert register(client).status_code == 201
    assert register(client, **overrides).status_code == 409


def test_unique_constraint_race_rolls_back(auth_client: AuthClient) -> None:
    client, _ = auth_client
    assert register(client).status_code == 201
    # Simulate the pre-check missing a concurrent insert; DB unique is the final guard.
    with patch(
        "app.repositories.user_repository.UserRepository.identity_exists",
        side_effect=[False, True],
    ):
        assert register(client).status_code == 409
    assert register(client, username="bob", email="bob@example.com").status_code == 201


@pytest.mark.parametrize(
    "username,password", [("alice", "wrong-password"), ("missing", "wrong-password")]
)
def test_invalid_login(auth_client: AuthClient, username: str, password: str) -> None:
    client, _ = auth_client
    register(client)
    response = client.post("/api/v1/auth/login", data={"username": username, "password": password})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.parametrize(
    "overrides", [{"password": "short"}, {"username": "   "}, {"email": "bad"}]
)
def test_registration_validation(auth_client: AuthClient, overrides: dict[str, str | None]) -> None:
    client, _ = auth_client
    assert register(client, **overrides).status_code == 422


def test_required_email(auth_client: AuthClient) -> None:
    client, _ = auth_client
    assert register(client, email=None).status_code == 422
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "alice", "password": "password-for-test"},
    )
    assert response.status_code == 422


def test_missing_invalid_and_deleted_user_tokens(auth_client: AuthClient) -> None:
    client, _ = auth_client
    assert client.get("/api/v1/users/me").status_code == 401
    for token in ("invalid", create_access_token(999)):
        assert (
            client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}).status_code
            == 401
        )


@pytest.mark.parametrize(
    "case", ["expired", "wrong_signature", "missing_exp", "bad_sub", "wrong_type"]
)
def test_reject_invalid_claims(auth_client: AuthClient, case: str) -> None:
    client, _ = auth_client
    user_id = register(client).json()["id"]
    now = datetime.now(UTC)
    payload: dict[str, str | datetime] = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=5),
        "type": "access",
    }
    secret = settings.jwt_secret_key
    if case == "expired":
        payload["exp"] = now - timedelta(seconds=1)
    elif case == "wrong_signature":
        secret = "a-different-signing-key-for-testing-only"
    elif case == "missing_exp":
        del payload["exp"]
    elif case == "bad_sub":
        payload["sub"] = "not-an-id"
    else:
        payload["type"] = "refresh"
    # PyJWT's optional crypto key types are unknown without cryptography installed.
    token = jwt.encode(  # pyright: ignore[reportUnknownMemberType]
        payload, secret, algorithm=settings.jwt_algorithm
    )
    assert (
        client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}).status_code
        == 401
    )
