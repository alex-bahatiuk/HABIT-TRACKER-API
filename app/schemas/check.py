from datetime import date
from pydantic import ConfigDict,BaseModel
from app.models.check import HabitStatus
class CheckCreate(BaseModel):
    day: date  # клиент передаёт конкретный день

class CheckOut(BaseModel):
    id: int
    habit_id: int
    day: date
    status: HabitStatus

    model_config = ConfigDict(from_attributes=True)

class StatsResponse(BaseModel):
    streak: int
    checked_last_days: int
   
