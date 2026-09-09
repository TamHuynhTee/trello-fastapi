from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.board_member import BoardMember
    from app.models.workspace import Workspace
    from app.models.workspace_member import WorkspaceMember


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True, index=True)

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    owned_workspaces: Mapped[list[Workspace]] = relationship(
        back_populates="owner", foreign_keys="workspaces.owner_id"
    )

    workspace_members: Mapped[list[WorkspaceMember]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    board_members: Mapped[list[BoardMember]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
