from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Member(SQLModel, table=True):
    __tablename__ = "members"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    phone: Optional[str] = None
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)