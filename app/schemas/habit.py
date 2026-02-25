from pydantic import BaseModel, Field

class HabitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class HabitOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True