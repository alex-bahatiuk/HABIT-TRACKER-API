from pydantic import ConfigDict,BaseModel, Field
from app.models.user import User

class HabitCreate(BaseModel):
   name: str = Field(min_length=1, max_length=120)
   target_per_week: int | None = Field(default=None, ge=1, le=7)

class HabitOut(BaseModel):
    id: int
    name: str
    target_per_week: int | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
class HabitStrengthOut(BaseModel):
    habit_id: int
    strength: float

    model_config = ConfigDict(from_attributes=True)
    