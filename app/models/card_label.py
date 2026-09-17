from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.label import Label


class CardLabel(Base):
    __tablename__ = "card_labels"

    __table_args__ = (UniqueConstraint("card_id", "label_id", name="uq_cards_labels"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id", ondelete="RESTRICT"), nullable=False
    )

    label_id: Mapped[int] = mapped_column(
        ForeignKey("labels.id", ondelete="RESTRICT"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    card: Mapped[Card] = relationship(back_populates="labels")

    label: Mapped[Label] = relationship(back_populates="card_labels")
