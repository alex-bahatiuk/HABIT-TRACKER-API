from datetime import date
from pydantic import BaseModel, ConfigDict

class CheckCreate(BaseModel):
    day: date  # клиент передаёт конкретный день

class CheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    habit_id: int
    day: date

    