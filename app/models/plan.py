from sqlmodel import SQLModel, Field
from typing import Optional

class Plan(SQLModel, table=True):
    __tablename__ = "plans"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    price: float = Field(default=0.0)
    description: Optional[str] = None