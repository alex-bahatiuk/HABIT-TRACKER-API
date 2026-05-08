from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from tests.test_stats import seed_checkins
from app.models.check import HabitCheck, HabitStatus
from app.core.database import SessionLocal

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

def test_stats_not_increment_after_single_skip():
    habit_id = client.post("/habits", json={"name": "test"}).json()["id"]

    client.post(f"/habits/{habit_id}/skip", json={"day": date.today().isoformat()})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200

    stats_data = response.json()
    assert stats_data["checked_last_days"] == 0, f"expected no last days checked, got {stats_data["checked_last_days"]}"
    assert stats_data["streak"] == 0, f"expected 0 day streak, got {stats_data["streak"]}" 

def test_stats_30_days_skip_between_checks():

    habit_id = client.post("/habits", json={"name": "test"}).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(30)]
    past_days.pop(9)

    seed_checkins(habit_id, past_days)

    skip_day = date.today() - timedelta(days=9)
    seed_skips(habit_id, [skip_day])

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.json()["checked_last_days"] == 9
    assert response.json()["streak"] == 29