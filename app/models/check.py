from sqlalchemy import Date, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class HabitCheck(Base):
    __tablename__ = "habit_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), index=True)
    day: Mapped[str] = mapped_column(Date, index=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    habit = relationship("Habit", back_populates="checks")

    __table_args__ = (
        UniqueConstraint("habit_id", "day", name="uq_habit_day"),
    )