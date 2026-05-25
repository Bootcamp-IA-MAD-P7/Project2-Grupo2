from datetime import datetime, time
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .reserva import Reserva


class TurnoDisponible(SQLModel, table=True):
    __tablename__ = "turnos_disponibles"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    segundo_apellido: str = Field(max_length=100)
    hora_inicio: time
    hora_fin: time
    aforo_maximo: int = Field(gt=0)
    slot_activo: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    reservas: List["Reserva"] = Relationship(back_populates="turno")