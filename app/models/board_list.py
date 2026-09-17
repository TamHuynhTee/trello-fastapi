from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils import enum_values

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.card import Card
    from app.models.user import User


class BoardListStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class ListWorkflowStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


class BoardList(Base):
    __tablename__ = "board_lists"

    __table_args__ = (UniqueConstraint("board_id", "order", name="uq_board_board_list_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    color: Mapped[str | None] = mapped_column(String(10), nullable=True, default="#000000")

    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete="RESTRICT"), nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    status: Mapped[BoardListStatus] = mapped_column(
        SQLEnum(
            BoardListStatus,
            name="boardliststatus",
            values_callable=enum_values,
        ),
        nullable=False,
        default=BoardListStatus.ACTIVE,
        server_default=BoardListStatus.ACTIVE.value,
    )

    workflow_status: Mapped[ListWorkflowStatus] = mapped_column(
        SQLEnum(
            ListWorkflowStatus,
            name="listworkflowstatus",
            values_callable=enum_values,
        ),
        nullable=False,
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

    board: Mapped[Board] = relationship(back_populates="board_lists", foreign_keys=[board_id])

    cards: Mapped[list[Card]] = relationship(
        back_populates="board_list", cascade="all, delete-orphan"
    )

    author: Mapped[User] = relationship(back_populates="board_lists", foreign_keys=[author_id])
