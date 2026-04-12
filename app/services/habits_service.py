from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import date, timedelta

from app.models.habit import Habit
from app.models.check import HabitCheck, HabitStatus

def create_habit(db: Session, name: str, target_per_week: int | None = None) -> Habit:
    existing = db.scalar(select(Habit).where(Habit.name == name))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Habit with this name already exists"
        )

    habit = Habit(name=name, target_per_week=target_per_week)
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
    today = date.today()
    # !zapret budushih dat
    if day > today:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot check habit for future day")
    
    # !zapret otmechat proshluyu datu
    if day < today - timedelta(days=1):
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot check habit more than 1 day ago")
    
    existing = db.scalar(
        select(HabitCheck).where(HabitCheck.habit_id == habit_id, HabitCheck.day == day)
    )
    if existing: 
        if existing.status == HabitStatus.DONE:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This day is already checked")
        else:
            existing.status = HabitStatus.DONE
    else:
        existing = HabitCheck(habit_id=habit_id, day=day, status=HabitStatus.DONE)
        db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing

def uncheck_habit(db: Session, habit_id: int, day: date) -> None:
    _ = get_habit(db, habit_id)

    existing = db.scalar(select(HabitCheck).where(HabitCheck.habit_id == habit_id,HabitCheck.day == day))

    today = date.today()
    
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found for this day")

    if day > today:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot uncheck habit for future day")
    
    if day < today - timedelta(days=1):

        if existing.status == HabitStatus.SKIPPED:
            raise HTTPException(status_code=400,detail="Cannot undo skip more than 1 day ago")
        else:
            raise HTTPException(status_code=400,detail="Cannot uncheck habit more than 1 day ago")

    db.delete(existing)
    db.commit()

def skip_habit(db: Session, habit_id: int, day: date) -> HabitCheck :
    _ = get_habit(db, habit_id)

    today = date.today()
    
    if day > today:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot skip habit for future day")
    if day < today - timedelta(days=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot skip habit more than 1 day ago")
    
    check = db.scalar(select(HabitCheck).where(HabitCheck.habit_id == habit_id,HabitCheck.day == day))
    
    if check is None:
        check = HabitCheck(habit_id=habit_id, day=day, status=HabitStatus.SKIPPED)
        db.add(check)
    else:
        if check.status == HabitStatus.SKIPPED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Habit already skipped for this day")  
        check.status = HabitStatus.SKIPPED

    db.commit()
    db.refresh(check)
    return check