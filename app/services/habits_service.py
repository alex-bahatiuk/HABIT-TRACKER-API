from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.habit import Habit
from datetime import date, timedelta, datetime

from app.models.check import HabitCheck, HabitStatus
from app.models.habit import Habit

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
    # !zapret budushih dat
    if day > date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot check habit for future day")
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

def uncheck_habit(db: Session, habit_id: int, day: date) -> None:
    _ = get_habit(db, habit_id)

    existing = db.scalar(
        select(HabitCheck).where(
            HabitCheck.habit_id == habit_id,
            HabitCheck.day == day
        )
    )
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found for this day")

    db.delete(existing)
    db.commit()

def skip_habit(db: Session, habit_id: int, day: date) -> HabitCheck:
    habit = get_habit(db, habit_id)
    
    check = db.scalar(
        select(HabitCheck).where(
            HabitCheck.habit_id == habit_id,
            HabitCheck.day == day
        )
    )
    
    if check is None:
        check = HabitCheck(habit_id=habit_id, day=day, status=HabitStatus.SKIPPED)
        db.add(check)
    else:
        check.status = HabitStatus.SKIPPED

    db.commit()
    db.refresh(check)
    return check

def calculate_habit_strength(db: Session, habit_id: int) -> float:
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=30)
    habit=get_habit(db, habit_id) 

    stmt = select(HabitCheck).where(
        HabitCheck.habit_id == habit_id,
        HabitCheck.day >= start_date
    )

    result = db.execute(stmt)
    checks = result.scalars().all()
    unique_days = {check.day for check in checks}
    completed_days = len(unique_days)
    days_since_creation = (today - habit.created_at.date()).days + 1
    total_days = min(30, days_since_creation)

    if total_days == 0:
        return 0.0
    strength = (completed_days / total_days) * 100
    return min(round((strength), 2))

