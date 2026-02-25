from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import date

from app.models.habit import Habit
from app.models.check import HabitCheck

def create_habit(db: Session, name: str) -> Habit:
    existing = db.scalar(select(Habit).where(Habit.name == name))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Habit with this name already exists")

    habit = Habit(name=name)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def list_habits(db: Session) -> list[Habit]:
    return list(db.scalars(select(Habit).order_by(Habit.id)))

def get_habit(db: Session, habit_id: int) -> Habit:
    habit = db.get(Habit, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

def delete_habit(db: Session, habit_id: int) -> None:
    habit = get_habit(db, habit_id)
    db.delete(habit)
    db.commit()

def check_habit(db: Session, habit_id: int, day: date) -> HabitCheck:
    _ = get_habit(db, habit_id)

    # если уже отмечено — не ломаем статистику
    existing = db.scalar(
        select(HabitCheck).where(HabitCheck.habit_id == habit_id, HabitCheck.day == day)
    )
    if existing:
        raise HTTPException(status_code=409, detail="This day is already checked")

    check = HabitCheck(habit_id=habit_id, day=day)
    db.add(check)
    db.commit()
    db.refresh(check)
    return check