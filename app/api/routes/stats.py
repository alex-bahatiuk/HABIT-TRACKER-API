from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.models.user import User
from app.services.dependencies import get_current_user
from app.schemas.check import StatsResponse
from app.services.stats_service import get_stats
from app.services.habits_service import get_habit

router = APIRouter(prefix="/habits", tags=["stats"])

@router.get("/{habit_id}/stats", response_model=StatsResponse)
def stats(
    habit_id: int,
    days: int = Query(30, ge=1),
    db: Session = Depends(db_session),
    current_user: User = Depends(get_current_user),
):
    get_habit(db, habit_id, owner_id=current_user.id)  # чтобы 404 если привычки нет
    return get_stats(db, habit_id, days=days, owner_id=current_user.id)

