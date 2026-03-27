from datetime import date
from pydantic import BaseModel
from app.models.check import HabitStatus
class CheckCreate(BaseModel):
    day: date  # клиент передаёт конкретный день

class CheckOut(BaseModel):
    id: int
    habit_id: int
    day: date
    status: HabitStatus
    class Config:
        from_attributes = True