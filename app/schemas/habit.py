from pydantic import BaseModel, Field

class HabitCreate(BaseModel):
   name: str = Field(min_length=1, max_length=120)
   target_per_week: int | None = Field(default=None, ge=1, le=7)

class HabitOut(BaseModel):
    id: int
    name: str
    target_per_week: int | None = None

    class Config:
        from_attributes = True

class HabitStrengthOut(BaseModel):
    habit_id: int
    strength: float

    class Config:
        from_attributes = True