from pydantic import BaseModel
from typing import Optional

# ESTA ES LA PLANTILLA BASE CON LOS CAMPOS COMUNES DE UN PLAN
class PlanBase(BaseModel):
    name: str
    price: float = 0.0
    description: Optional[str] = None

# ESTE ES EL MOLDE QUE SE USA PARA CREAR UN PLAN NUEVO
class PlanCreate(PlanBase):
    pass

# ESTE ES EL MOLDE PARA MOSTRAR EL PLAN EN PANTALLA (INCLUYE EL ID)
class PlanResponse(PlanBase):
    id: int

    class Config:
        from_attributes = True