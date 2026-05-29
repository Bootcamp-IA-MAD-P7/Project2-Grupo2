from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AttendanceCreate(BaseModel):
    member_id: int
    reservation_id: int


class AttendanceResponse(BaseModel):
    id: int
    member_id: int
    reservation_id: int
    check_in: datetime
    check_out: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    