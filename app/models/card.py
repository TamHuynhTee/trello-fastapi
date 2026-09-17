from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils import enum_values

if TYPE_CHECKING:
    from app.models.board_list import BoardList
    from app.models.card_label import CardLabel
    from app.models.card_member import CardMember
    from app.models.comment import Comment
    from app.models.user import User


class CardStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class CardPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Card(Base):
    __tablename__ = "cards"

    __table_args__ = (UniqueConstraint("list_id", "order", name="uq_board_list_card_order"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    list_id: Mapped[int] = mapped_column(
        ForeignKey("board_lists.id", ondelete="RESTRICT"), nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    priority: Mapped[CardPriority | None] = mapped_column(
        SQLEnum(
            CardPriority,
            name="cardpriority",
            values_callable=enum_values,
        ),
        nullable=True,
    )

    status: Mapped[CardStatus | None] = mapped_column(
        SQLEnum(
            CardStatus,
            name="cardstatus",
            values_callable=enum_values,
        ),
        nullable=False,
        default=CardStatus.ACTIVE,
        server_default=CardStatus.ACTIVE.value,
    )

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(),
        nullable=True,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(),
        nullable=True,
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

    board_list: Mapped[BoardList] = relationship(back_populates="cards", foreign_keys=[list_id])

    comments: Mapped[list[Comment]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )

    labels: Mapped[list[CardLabel]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )

    assignments: Mapped[list[CardMember]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )

    author: Mapped[User] = relationship(back_populates="cards", foreign_keys=[author_id])
