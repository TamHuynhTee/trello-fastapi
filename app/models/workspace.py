from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Workspace(Base):
  __tablename__ = "workspaces"

  id: Mapped[int] = mapped_column(
    primary_key=True
  )

  name: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
  )

  description: Mapped[str | None] = mapped_column(
    String(1000),
    nullable=True,
  )

  owner_id: Mapped[str] = mapped_column(
    ForeignKey(
      "users.id",
      ondelete="RESTRICT"
    ),
    nullable=False
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

  owner: Mapped["User"] = relationship(
    back_populates="owned_workspaces",
    foreign_keys=[owner_id]
  )

  members: Mapped[list["WorkspaceMember"]] = relationship(
    back_populates="workspace",
    cascade="all, delete-orphan"
  )