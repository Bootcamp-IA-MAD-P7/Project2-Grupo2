from pydantic import BaseModel
from typing import Optional

# Lo que EXIGIMOS cuando alguien quiere CREAR un plan nuevo desde la web
class PlanCreate(BaseModel):
    nombre: str
    precio: float = 0.0
    descripcion: Optional[str] = None

# Lo que DEVOLVEMOS cuando el sistema lee un plan (incluye el ID de la base de datos)
class PlanRead(BaseModel):
    id: int
    nombre: str
    precio: float
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True