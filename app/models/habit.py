from datetime import datetime

from sqlalchemy import String, DateTime,Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    target_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    checks = relationship("HabitCheck", back_populates="habit", cascade="all, delete-orphan")

   