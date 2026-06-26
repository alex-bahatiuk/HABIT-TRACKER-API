import pytest
from app.core.database import SessionLocal, Base, engine
from app.models.habit import Habit
from app.models.check import HabitCheck, HabitStatus
from app.main import app
from fastapi.testclient import TestClient

from app.models.user import User

client = TestClient(app)

def seed_skips(habit_id, dates):
    db = SessionLocal()
    try:
        for d in dates:
            # Tworzymy rekordy bezpośrednio w bazie, omijając walidację API
            check = HabitCheck(habit_id=habit_id, day=d, status=HabitStatus.SKIPPED)
            db.add(check)
        db.commit()
    except Exception as e:
        print(f"Błąd bazy: {e}")
        db.rollback()
    finally:
        db.close()

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
        db.query(User).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Błąd podczas czyszczenia bazy: {e}")
    finally:
       db.close()
    yield

def authenticate():
    email = "fixed@mail.com"
    password = "84@W84@w"
    client.post("/auth/register", json={"email": email, "password": password})

    res = client.post("/auth/login", data={"username": email, "password": password})

    token = res.json()["access_token"]

    return {"Authorization": f"Bearer {token}" }