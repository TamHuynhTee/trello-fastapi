from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils import enum_values

if TYPE_CHECKING:
    from app.models.board_list import BoardList
    from app.models.board_member import BoardMember
    from app.models.label import Label
    from app.models.user import User
    from app.models.workspace import Workspace


class BoardStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class BoardView(str, Enum):
    BOARD = "board"
    TABLE = "table"


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    status: Mapped[BoardStatus] = mapped_column(
        SQLEnum(
            BoardStatus,
            name="boardstatus",
            values_callable=enum_values,
        ),
        nullable=False,
        default=BoardStatus.ACTIVE,
        server_default=BoardStatus.ACTIVE.value,
    )

    view: Mapped[BoardView] = mapped_column(
        SQLEnum(
            BoardView,
            name="boardview",
            values_callable=enum_values,
        ),
        nullable=False,
        default=BoardView.BOARD,
        server_default=BoardView.BOARD.value,
    )

    workspace: Mapped[Workspace] = relationship(
        back_populates="boards", foreign_keys=[workspace_id]
    )

    board_members: Mapped[list[BoardMember]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )

    board_lists: Mapped[list[BoardList]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )

    labels: Mapped[list[Label]] = relationship(back_populates="board", cascade="all, delete-orphan")

    author: Mapped[User] = relationship(back_populates="boards", foreign_keys=[author_id])
