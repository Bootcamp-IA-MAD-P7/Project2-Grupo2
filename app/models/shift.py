from datetime import datetime, time
from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from .reservation import Reservation


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class AvailableShift(SQLModel, table=True):
    __tablename__ = "available_shifts"
    __table_args__ = (
        UniqueConstraint("day_of_week", "start_time", name="uq_shift_day_time"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    class_name: str = Field(max_length=100)
    instructor: str = Field(max_length=100)
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    max_capacity: int = Field(gt=0)
    active_slot: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    reservations: List["Reservation"] = Relationship(back_populates="shift")