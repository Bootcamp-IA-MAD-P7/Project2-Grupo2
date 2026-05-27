class ShiftBase(SQLModel):
    name: str = Field(max_length=100)
    instructor: str = Field(max_length=150)
    start_time: time
    end_time: time
    max_capacity: int = Field(gt=0)
    active_slot: bool = Field(default=True)