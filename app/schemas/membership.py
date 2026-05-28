from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel
from pydantic import model_validator
from ..models.membership import MembershipStatus


class MembershipBase(SQLModel):
    member_id: int
    plan_id: int
    start_date: date
    status: MembershipStatus = MembershipStatus.pending


class MembershipCreate(MembershipBase):
    @model_validator(mode="after")
    def start_date_not_in_past(self):
        if self.start_date < date.today():
            raise ValueError("The start date cannot be in the past")
        return self


class MembershipUpdate(SQLModel):
    status: Optional[MembershipStatus] = None


class MembershipRead(MembershipBase):
    id: int
    end_date: Optional[date]
    is_active: bool = False
    days_remaining: int = 0
    created_at: datetime
    updated_at: datetime