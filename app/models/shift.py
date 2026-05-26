from datetime import datetime, time
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .reservation import Reservation


class AvailableShift(SQLModel, table=True):
    __tablename__ = "available_shifts"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    start_time: time
    end_time: time
    max_capacity: int = Field(gt=0)
    active_slot: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    reservations: List["Reservation"] = Relationship(back_populates="shift")