from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field, SecretStr, StringConstraints

Username = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_.-]+$"
    ),
]


class RegisterRequest(BaseModel):
    username: Username
    password: SecretStr = Field(min_length=8, max_length=128)
    email: EmailStr = Field(max_length=255)
    full_name: str | None = Field(default=None, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
