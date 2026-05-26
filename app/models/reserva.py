from datetime import datetime, date
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from .turno import TurnoDisponible
    from .miembro import Miembro


class EstadoReserva(str, Enum):
    confirmada = "confirmada"
    cancelada = "cancelada"
    no_asistio = "no_asistio"


class Reserva(SQLModel, table=True):
    __tablename__ = "reservas"
    __table_args__ = (
        UniqueConstraint("miembro_id", "turno_id", "fecha", name="uq_reserva_miembro_turno_fecha"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    miembro_id: Optional[int] = Field(default=None, foreign_key="miembros.id")
    turno_id: Optional[int] = Field(default=None, foreign_key="turnos_disponibles.id")
    fecha: date
    estado: EstadoReserva = Field(default=EstadoReserva.pendiente)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    miembro: Optional["Miembro"] = Relationship(back_populates="reservas")
    turno: Optional["TurnoDisponible"] = Relationship(back_populates="reservas")