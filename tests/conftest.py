import pytest
from app.core.database import SessionLocal
from app.models.habit import Habit
from app.models.check import HabitCheck

@pytest.fixture(autouse=True)
def clean_database():
    """
    Czyści bazę przed każdym testem.
    """
    db = SessionLocal()
    try:
        # Usuwamy dane z tabel.
        db.query(HabitCheck).delete()
        db.query(Habit).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Błąd podczas czyszczenia bazy: {e}")
    finally:
        db.close()
    yield