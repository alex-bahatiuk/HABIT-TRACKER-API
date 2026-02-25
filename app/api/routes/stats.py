from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.services.stats_service import get_stats
from app.services.habits_service import get_habit

router = APIRouter(prefix="/habits", tags=["stats"])

@router.get("/{habit_id}/stats")
def stats(habit_id: int, db: Session = Depends(db_session)):
    # чтобы вернуть 404 если привычки нет
    get_habit(db, habit_id)
    return get_stats(db, habit_id)