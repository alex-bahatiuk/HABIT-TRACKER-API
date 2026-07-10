from pydantic import ConfigDict,BaseModel, Field
from app.models.check import HabitStatus
from app.models.user import User
from datetime import date

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
    
class HabitHistoryItem(BaseModel):
    day: date
    status: HabitStatus

    model_config = ConfigDict(from_attributes=True)