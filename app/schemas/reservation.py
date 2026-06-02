from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field
from app.models.reservation import ReservationStatus


class ReservationBase(SQLModel):
    shift_id: int
    date: date
    status: ReservationStatus = Field(default=ReservationStatus.confirmed)


class ReservationCreate(SQLModel):
    shift_id: int
    date: date


class ReservationUpdate(SQLModel):
    status: Optional[ReservationStatus] = None
    queue_position: Optional[int] = None


class ReservationRead(ReservationBase):
    id: int
    member_id: int
    queue_position: Optional[int] = None
    created_at: datetime
    updated_at: datetime