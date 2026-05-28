from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ESTA ES LA PLANTILLA BASE CON LOS CAMPOS COMUNES DE UN MIEMBRO
class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool = True

# ESTE ES EL MOLDE QUE SE USA PARA REGISTRAR A UN MIEMBRO NUEVO
class MemberCreate(MemberBase):
    pass

# ESTE ES EL MOLDE PARA MOSTRAR AL MIEMBRO EN PANTALLA (INCLUYE ID Y FECHA DE REGISTRO)
class MemberResponse(MemberBase):
    id: int
    registration_date: datetime

    class Config:
        from_attributes = True