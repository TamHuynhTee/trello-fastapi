from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class WorkspaceMember(Base):
  __tablename__ = "workspace_members"

  __table_args__ = (
    UniqueConstraint(
      "workspace_id",
      "user_id",
      name="uq_workspace_members_workspace_user"
    ),
  )

  id: Mapped[int] = mapped_column(
    primary_key=True
  )

  workspace_id: Mapped[int] = mapped_column(
    ForeignKey(
      "workspaces.id",
      ondelete="CASCADE"
    ),
    nullable=False
  )

  user_id: Mapped[int] = mapped_column(
    ForeignKey(
      "users.id",
      ondelete="CASCADE"
    ),
    nullable=False
  )

  role: Mapped[str] = mapped_column(
    String(20),
    nullable=False,
    default="MEMBER"
  )

  joined_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
  )

  user: Mapped["User"] = relationship(
    back_populates="workspace_membership"
  )

  workspace: Mapped["Workspace"] = relationship(
    back_populates="members"
  )