from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.board_member import BoardMember
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
        String(1000),
        nullable=True,
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="RESTRICT"), nullable=False
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
        SQLEnum(BoardStatus), default=BoardStatus.ACTIVE, nullable=False
    )

    view: Mapped[BoardView] = mapped_column(
        SQLEnum(BoardView), default=BoardView.BOARD, nullable=False
    )

    workspace: Mapped[Workspace] = relationship(
        back_populates="boards", foreign_keys=[workspace_id]
    )

    board_members: Mapped[list[BoardMember]] = relationship(
        back_populates="board", cascade="all, delete-orphan"
    )
