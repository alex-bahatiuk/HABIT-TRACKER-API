from datetime import datetime
from sqlalchemy import Column, ForeignKey, ForeignKey
from sqlalchemy import String, DateTime,Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    target_per_week = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    checks = relationship("HabitCheck", back_populates="habit", cascade="all, delete-orphan")

   