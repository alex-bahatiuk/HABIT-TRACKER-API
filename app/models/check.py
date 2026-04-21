from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from enum import Enum
from sqlalchemy import Enum as SqlEnum
class HabitStatus(str, Enum):
    DONE = "done"
    SKIPPED = "skipped"

class HabitCheck(Base):
    __tablename__ = "habit_checks"

    id: Mapped[int] = mapped_column(primary_key=True)

    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    habit = relationship("Habit", back_populates="checks")

    __table_args__ = (
        UniqueConstraint("habit_id", "day", name="uq_habit_day"),
    )
    status:Mapped[HabitStatus] = mapped_column(SqlEnum(HabitStatus), nullable=False, default=HabitStatus.DONE)