from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Numeric
from enum import Enum

if TYPE_CHECKING:
    from .membership import Membership


class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    transfer = "transfer"
    bizum = "bizum"
    direct_debit = "direct_debit"
    other = "other"


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(SQLModel, table=True):
    """Financial transaction linked to a membership."""
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    membership_id: int = Field(foreign_key="memberships.id", index=True)
    amount: Decimal = Field(sa_column=Column(Numeric(8, 2)))
    payment_method: PaymentMethod
    status: PaymentStatus = Field(default=PaymentStatus.pending)
    reference: str = Field(default="", max_length=100)
    payment_date: datetime = Field(default_factory=datetime.utcnow)
    notes: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    membership: Optional["Membership"] = Relationship(back_populates="payments")
