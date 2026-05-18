from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.habit import Habit 
from datetime import date, timedelta

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
    if existing is None:
            existing = HabitCheck(habit_id=habit_id, day=day, status=HabitStatus.DONE)
            db.add(existing)
    elif existing.status == HabitStatus.SKIPPED:
            existing.status = HabitStatus.DONE
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This day is already checked")
            
    db.commit()
    db.refresh(existing)
    return existing

def uncheck_habit(db: Session, habit_id: int, day: date) -> None:
    _ = get_habit(db, habit_id)
    
    today = date.today()
    existing = db.scalar(
        select(HabitCheck).where(
            HabitCheck.habit_id == habit_id,
            HabitCheck.day == day
        )
    )

    if day < today - timedelta(days=1):
        if existing and existing.status == HabitStatus.SKIPPED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot undo skip more than 1 day ago"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot uncheck habit more than 1 day ago"
        )

    if day > today:
        if existing and existing.status == HabitStatus.SKIPPED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot undo skip for future day"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot uncheck habit for future day"
        )

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check not found for this day"
        )

    if day > today:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot uncheck habit for future day")
    
    if day < today - timedelta(days=1):

        if existing.status == HabitStatus.SKIPPED:
            raise HTTPException(status_code=400,detail="Cannot undo skip more than 1 day ago")
        else:
            raise HTTPException(status_code=400,detail="Cannot uncheck habit more than 1 day ago")

    db.delete(existing)
    db.commit()

def skip_habit(db: Session, habit_id: int, day: date) -> HabitCheck:
    habit = get_habit(db, habit_id)
    today = date.today()

    if day > today:
       raise HTTPException(status_code=400,detail="Cannot skip habit for future day")
    if day < today - timedelta(days=1):
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot skip habit more than 1 day ago")
    
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
        if check.status == HabitStatus.SKIPPED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Habit already skipped for this day")  
        check.status = HabitStatus.SKIPPED

    db.commit()
    db.refresh(check)
    return check

def calculate_habit_strength(db: Session, habit_id: int) -> float:
    today = date.today()
    start_date = today - timedelta(days=30)
    habit=get_habit(db, habit_id) 

    stmt = select(HabitCheck).where(HabitCheck.habit_id == habit_id)

    result = db.execute(stmt)
    checks = result.scalars().all()
    unique_days = {check.day for check in checks}
    completed_days = len(unique_days)

    if completed_days == 0:
        return 0.0
    
    first_check_date = min(unique_days)
    days_range = (today - first_check_date).days + 1
    total_days = min( days_range, 30) #limit to 30 days for strength calculation
    start_date = today - timedelta(days=total_days - 1)

    checks_30 = [check.day for check in checks if check.day >= start_date] 
    completed_days_30 = len(set(checks_30))
    
    strength = (completed_days_30 / total_days) * 100
    print("DEBUG strength:", {
    "completed_days": completed_days,
    "first_check_date": first_check_date,
    "days_range": days_range,
    "total_days": total_days,
    "strength": strength,})
    return round(min(strength,100), 2)

def undo_skip_habit(db: Session, habit_id: int, day: date) -> None:
    get_habit(db, habit_id)
    today = date.today()

    if day < today - timedelta(days=1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot undo skip more than 1 day ago"
        )

    if day > today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot undo skip for future day"
        )

    existing = db.scalar(
        select(HabitCheck).where(
            HabitCheck.habit_id == habit_id,
            HabitCheck.day == day,
        )
    )

    if existing is None or existing.status != HabitStatus.SKIPPED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skip not found for this day"
        )

    db.delete(existing)
    db.commit()
    
    return round(0.0, 2)

