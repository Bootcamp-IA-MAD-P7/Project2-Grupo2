from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel

# Esto evita que los archivos se bloqueen entre sí al importarse
if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.attendance import Attendance

class MemberStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class Member(SQLModel, table=True):
    __tablename__ = "members"  # <-- Mantenemos tus dos guiones bajos perfectos

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    phone: Optional[str] = None
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)

    # Las nuevas relaciones bidireccionales de tu modelo
    reservations: list["Reservation"] = Relationship(back_populates="member")
    attendances: list["Attendance"] = Relationship(back_populates="member")
