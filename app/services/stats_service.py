from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date, timedelta

from app.models.check import HabitCheck

def get_stats(db: Session, habit_id: int) -> dict:
    # берём последние 30 дней отметок
    today = date.today()
    start = today - timedelta(days=29)

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
        "checked_last_30_days": len(checked_days),
        "range_start": start.isoformat(),
        "range_end": today.isoformat(),
    }