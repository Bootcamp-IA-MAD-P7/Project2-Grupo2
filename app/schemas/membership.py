from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field
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
    end_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime