import pytest
from app.core.database import SessionLocal, Base, engine
from app.models.habit import Habit
from app.models.check import HabitCheck

@pytest.fixture(autouse=True)
def clean_database():
    """
    Czyści bazę przed każdym testem.
    """
    #Base.metadata.drop_all(bind=engine)  # Usuwamy wszystkie tabele
    #Base.metadata.create_all(bind=engine)  # Tworzymy je ponownie
    db = SessionLocal()

    try:
         #Usuwamy dane z tabel.
        db.query(HabitCheck).delete()
        db.query(Habit).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Błąd podczas czyszczenia bazy: {e}")
    finally:
       db.close()
    yield