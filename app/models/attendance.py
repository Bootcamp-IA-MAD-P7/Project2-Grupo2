from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .member import Member
    from .reservation import Reservation


class Attendance(SQLModel, table=True):
    __tablename__ = "attendances"
    __table_args__ = (
        UniqueConstraint(
            "member_id",
            "reservation_id",
            name="uq_attendance_member_reservation",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    member_id: int = Field(foreign_key="members.id", index=True)
    reservation_id: int = Field(foreign_key="reservations.id", index=True)

    check_in: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    check_out: Optional[datetime] = Field(default=None)

    member: Optional["Member"] = Relationship(back_populates="attendances")
    reservation: Optional["Reservation"] = Relationship(back_populates="attendances")
