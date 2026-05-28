from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel
from pydantic import field_validator
from ..models.payment import PaymentMethod, PaymentStatus


class PaymentBase(SQLModel):
    membership_id: int
    amount: Decimal
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.pending
    reference: str = ""
    notes: str = ""

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("The amount must be greater than 0")
        return v


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(SQLModel):
    status: Optional[PaymentStatus] = None
    reference: Optional[str] = None
    notes: Optional[str] = None


class PaymentRead(PaymentBase):
    id: int
    payment_date: datetime
    created_at: datetime