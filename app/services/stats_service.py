from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta
from app.models.check import HabitCheck,HabitStatus
from app.services.habits_service import get_habit
#from app.models.habit import Habit

def get_stats(db: Session, habit_id: int, days: int = 30) -> dict:
    habit = get_habit(db, habit_id)

    today = date.today()
    start = today - timedelta(days=days-1)

    checks = list(
        db.scalars(
            select(HabitCheck)
            .where(HabitCheck.habit_id == habit_id, HabitCheck.day >= start, HabitCheck.day <= today)
            .order_by(HabitCheck.day.asc())
        )
    )
    skipped_days = {c.day for c in checks if c.status == HabitStatus.SKIPPED}
    checked_last_days = calculate_checked_last_days(checks)

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
        "checked_last_days": checked_last_days,
        "skipped_last_days": len(skipped_days),
        "range_start": start.isoformat(),
        "range_end": today.isoformat(),
    }

def calculate_daily_streak(checks):
    checked_days = {c.day: c.status for c in checks}
    skipped_checks = [c for c in checks if c.status == HabitStatus.SKIPPED]
    today = date.today()

    if today in checked_days:
         cur = today 
    else:
        cur = today - timedelta(days=1)

    streak = 0

    while cur in checked_days:
        status = checked_days[cur]

        if status == HabitStatus.DONE:
            streak += 1

        elif status == HabitStatus.SKIPPED:
            pass  
        else:
            break  
        cur -= timedelta(days=1)
    
    print("STREAK:", streak)
    print("SKIPPED CHECKS:", [(c.day, c.status) for c in skipped_checks if c.status == HabitStatus.SKIPPED])
    print("DONE CHECKS:", [(c.day, c.status) for c in checks if c.status == HabitStatus.DONE])
    return streak

def calculate_checked_last_days(checks):

    checked_days = { c.day: c.status for c in checks }
    today = date.today()
    cur = today
    count = 0

    while cur in checked_days:
        status = checked_days[cur]
        if status == HabitStatus.DONE:
            count += 1
        else:
            break
        cur -= timedelta(days=1)

    return count

def calculate_weekly_streak(checks, target_per_week, today=None):

    weeks = { }

    for check in checks:
            week_start = check.day - timedelta(days=check.day.weekday())  # начало недели (понедельник)
            weeks[week_start] = weeks.get(week_start, 0) + 1
        
    today = today or date.today()  # Позволяет передать конкретную дату для тестирования вместо
    current_week_start = today - timedelta(days=today.weekday())
    streak = 0

    sorted_weeks = sorted(weeks.keys(), reverse=True)
    print("Weeks:", sorted_weeks)
    for week in sorted_weeks:
        if week == current_week_start:
                streak += weeks[week]  
                continue  
        count = weeks[week]
        if count >= target_per_week:
                streak += count
        else:
                break

    return streak






        
    

    