from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta
from app.models.check import HabitCheck,HabitStatus
from app.services.habits_service import get_habit

def get_stats(db: Session, habit_id: int, days: int = 30, owner_id: int | None = None) -> dict:
    habit = get_habit(db, habit_id, owner_id)

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
    today = today or date.today()  
    current_week_start = today - timedelta(days=today.weekday())

    weeks = { }

    for check in checks:
            check_date = check.day #if hasattr(check, "date") else check
            week_start = check_date - timedelta(days=check_date.weekday())  
            weeks[week_start] = weeks.get(week_start, 0) + 1
        
    streak = 0

    # текущая неделя добавляется как есть
    current_count = weeks.get(current_week_start, 0)
    streak += current_count

    # дальше идём строго неделя за неделей назад
    week = current_week_start - timedelta(days=7)

    while True:
        count = weeks.get(week, 0)

        if count >= target_per_week:
            streak += count
            week -= timedelta(days=7)
        else:
            break

    return streak






        
    

    