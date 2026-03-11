from pydantic import BaseModel, Field, ConfigDict

class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    target_per_week: int | None = Field(default=None, ge=1, le=7)

class HabitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    target_per_week: int | None = None

    