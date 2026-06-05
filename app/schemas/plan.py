from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class PlanBase(SQLModel):
    name: str = Field(max_length=100)
    price: float = Field(default=0.0, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)
    duration_days: int = Field(default=30, gt=0)
    active: bool = Field(default=True)


class PlanCreate(PlanBase):
    pass


class PlanUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    price: Optional[float] = Field(default=None, ge=0)
    description: Optional[str] = None
    duration_days: Optional[int] = Field(default=None, gt=0)
    active: Optional[bool] = None


class PlanResponse(PlanBase):
    id: int
    created_at: datetime
    updated_at: datetime