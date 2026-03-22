from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta

from app.models.check import HabitCheck
from app.services.habits_service import get_habit
from app.models.habit import Habit

def get_stats(db: Session, habit_id: int, days: int = 30) -> dict:
    habit = get_habit(db, habit_id)

    today = date.today()
    start = today - timedelta(days=days - 1 )

    checks = list(
        db.scalars(
            select(HabitCheck)
            .where(HabitCheck.habit_id == habit_id, HabitCheck.day >= start, HabitCheck.day <= today)
            .order_by(HabitCheck.day.asc())
        )
    )
    checked_days = {c.day for c in checks}
    if habit.target_per_week is not None:
        streak = calculate_weekly_streak(checks, habit.target_per_week)
    else:
        streak = calculate_daily_streak(checks)
   
    return {
        "habit_id": habit_id,
        "streak": streak,
        "days-window": days,
        "checked_last_days": len(checked_days),
        "range_start": start.isoformat(),
        "range_end": today.isoformat(),
    }

def calculate_daily_streak(checks):
    checked_days = {c.day for c in checks}
    today = date.today()

    if today in checked_days:
         cur = today 
    else:
            cur = today - timedelta(days=1)

    streak = 0

    while cur in checked_days:
        streak += 1
        cur -= timedelta(days=1)

    return streak

def calculate_weekly_streak(checks, target_per_week):

    weeks = { }
    for check in checks:
        week_start = check.day - timedelta(days=check.day.weekday())  # начало недели (понедельник)
        weeks[week_start] = weeks.get(week_start, 0) + 1
        
        today = date.today()
        current_week_start = today - timedelta(days=today.weekday())
        current_count = weeks.get(current_week_start, 0)
        checked_days = {c.day for c in checks}
        prev_day = today - timedelta(days=1)

        streak = current_count

    while prev_day in checked_days:
            streak += 1
            prev_day = prev_day - timedelta(days=1)

    return streak
    
    

    