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
        print("Calculating weekly streak...")
        streak = calculate_weekly_streak(checks, habit.target_per_week)
    else:
        print("Calculating daily streak...")
        streak = calculate_daily_streak(checks)
    print("target per week=", habit.target_per_week)
    print("checks=", [c.day for c in checks])
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
    streak = 0

    sorted_weeks = sorted(weeks.keys(), reverse=True)
    print("Weeks:", sorted_weeks)
    for week in sorted_weeks:
        if week == current_week_start:
                streak += weeks[week]  # учитываем текущую неделю, даже если она не полная
                continue  # пропускаем текущую неделю, она уже учтена в current_count
        count = weeks[week]
        if count >= target_per_week:
                streak += count
        else:
                break
    return streak






        
    

    