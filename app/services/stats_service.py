from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta

from app.models.check import HabitCheck
from app.services.habits_service import get_habit

def get_stats(db: Session, habit_id: int, days: int = 30) -> dict:
    _ = get_habit(db, habit_id)

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

    # streak: считаем подряд от today назад
    streak = 0
    cur = today
    while cur in checked_days:
        streak += 1
        cur -= timedelta(days=1)

    return {
        "habit_id": habit_id,
        "streak": streak,
        "days-window": days,
        "checked_last_days": len(checked_days),
        "range_start": start.isoformat(),
        "range_end": today.isoformat(),
    }