from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .miembro import Miembro
    from .reserva import Reserva


class Asistencia(SQLModel, table=True):
    __tablename__ = "asistencias"

    id: Optional[int] = Field(default=None, primary_key=True)

    miembro_id: int = Field(foreign_key="miembros.id")
    reserva_id: int = Field(foreign_key="reservas.id")

    entrada: datetime = Field(default_factory=datetime.utcnow)
    salida: Optional[datetime] = Field(default=None)

    miembro: Optional["Miembro"] = Relationship(back_populates="asistencias")
    reserva: Optional["Reserva"] = Relationship(back_populates="asistencias")