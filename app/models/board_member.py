from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.user import User


class BoardRole(str, Enum):
    MEMBER = "member"
    ADMIN = "admin"
    VIEWER = "viewer"


class BoardMember(Base):
    __tablename__ = "board_members"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete="RESTRICT"), nullable=False
    )

    role: Mapped[BoardRole] = mapped_column(
        SQLEnum(BoardRole), default=BoardRole.MEMBER, nullable=False
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="board_members")

    board: Mapped[Board] = relationship(back_populates="board_members")
