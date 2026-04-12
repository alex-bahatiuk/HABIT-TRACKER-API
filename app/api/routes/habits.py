from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date
from fastapi import Query
from app.api.deps import db_session
from app.schemas.habit import HabitCreate, HabitOut, HabitStrengthOut
from app.schemas.check import CheckCreate, CheckOut
from app.services import habits_service

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
def create(payload: HabitCreate, db: Session = Depends(db_session)):
    return habits_service.create_habit(db, payload.name,payload.target_per_week)

@router.get("", response_model=list[HabitOut])
def list_all(db: Session = Depends(db_session)):
    return habits_service.list_habits(db)

@router.get("/{habit_id}", response_model=HabitOut)
def get_one(habit_id: int, db: Session = Depends(db_session)):
    return habits_service.get_habit(db, habit_id)

@router.get("/{habit_id}/strength", response_model=HabitStrengthOut)
def get_strength(habit_id: int, db: Session = Depends(db_session)):
    habit = habits_service.get_habit(db, habit_id)
    strength = habits_service.calculate_habit_strength(db, habit_id)
    return HabitStrengthOut(habit_id=habit_id, strength=strength)

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(habit_id: int, db: Session = Depends(db_session)):
    habits_service.delete_habit(db, habit_id)
    return None

@router.post("/{habit_id}/check", response_model=CheckOut, status_code=status.HTTP_201_CREATED)
def check(habit_id: int, payload: CheckCreate, db: Session = Depends(db_session)):
    return habits_service.check_habit(db, habit_id, payload.day)

@router.delete("/{habit_id}/check", status_code=status.HTTP_204_NO_CONTENT)
def uncheck(
    habit_id: int,
    day: date = Query(...),
    db: Session = Depends(db_session),
):
    habits_service.uncheck_habit(db, habit_id, day)
    return None

@router.post("/{habit_id}/skip",response_model=CheckOut, status_code=status.HTTP_201_CREATED)
def skip_habit_endpoint(habit_id: int, payload: CheckCreate, db: Session = Depends(db_session)):
    return habits_service.skip_habit(db, habit_id, payload.day)