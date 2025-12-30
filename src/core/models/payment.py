from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

import uuid


class Payment(Base):
    __table_args__ = (
        CheckConstraint("amount >= 50", name="ck_payment_amount_minimum"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="initiated")
    generated_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    