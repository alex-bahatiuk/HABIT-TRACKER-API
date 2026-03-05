from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date
from fastapi import Query
from app.api.deps import db_session
from app.schemas.habit import HabitCreate, HabitOut
from app.schemas.check import CheckCreate, CheckOut
from app.services import habits_service

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
def create(payload: HabitCreate, db: Session = Depends(db_session)):
    return habits_service.create_habit(db, payload.name)

@router.get("", response_model=list[HabitOut])
def list_all(db: Session = Depends(db_session)):
    return habits_service.list_habits(db)

@router.get("/{habit_id}", response_model=HabitOut)
def get_one(habit_id: int, db: Session = Depends(db_session)):
    return habits_service.get_habit(db, habit_id)

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