from datetime import date
from pydantic import BaseModel

class CheckCreate(BaseModel):
    day: date  # клиент передаёт конкретный день

class CheckOut(BaseModel):
    id: int
    habit_id: int
    day: date

    class Config:
        from_attributes = True