import time
from datetime import date, timedelta
from app.core.database import SessionLocal

from fastapi.testclient import TestClient
from app.main import app
from app.models.check import HabitCheck, HabitStatus

client = TestClient(app)

def seed_checkins(habit_id, dates):
    db = SessionLocal()
    try:
        for d in dates:
            # Tworzymy rekordy bezpośrednio w bazie, omijając walidację API
            check = HabitCheck(habit_id=habit_id, day=d)
            db.add(check)
        db.commit()
    except Exception as e:
        print(f"Błąd bazy: {e}")
        db.rollback()
    finally:
        db.close()

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

def test_stats_increment_after_single_checkin():
    unique_name = f"StatTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    client.post(f"/habits/{habit_id}/check", json={"day": date.today().isoformat()})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200

    stats_data = response.json()
    assert stats_data["streak"] == 1
    assert stats_data["checked_last_days"] == 1

def test_stats_30_days():
    unique_name = f"30days_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(30)]
    seed_checkins(habit_id, past_days)

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    assert stats["checked_last_days"] == 30

def test_stats_total_count_limit_check():
    unique_name = f"LimitTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    days = 100
    past_days = [(date.today() - timedelta(days=i)) for i in range(days)]
    seed_checkins(habit_id, past_days)

    response = client.get(f"/habits/{habit_id}/stats", params={"days": days})
    stats = response.json()

    actual_checks = stats.get("checked_last_days", 0)
    assert actual_checks == days

#  Weryfikacja, czy przerwa w dniach poprawnie przerywa streak.
def test_stats_streak_calculation_with_gap():
    unique_name = f"GapTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(5)]
    past_days.pop(3)
    seed_checkins(habit_id, past_days)

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # Streak powinien liczyć ciąg wstecz od dzisiaj (3 dni), ignorując wpis sprzed przerwy
    assert stats["streak"] == 3


# TEST LIMITU 365 DNI
def test_stats_should_allow_more_than_365_days():
    unique_name = f"LongTerm_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    response = client.get(f"/habits/{habit_id}/stats", params={"days": 400})

    assert response.status_code == 200


""" SUGESTIA UX: Weryfikacja, czy streak jest utrzymywany, jeśli dzisiejszy dzień 
nie został jeszcze odhaczony (szansa dla użytkownika). """

def test_stats_streak_grace_period_ux():
    unique_name = f"UX_Test_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    # Odhaczamy tylko wczoraj
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    client.post(f"/habits/{habit_id}/check", json={"day": yesterday})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # Oczekiwanie: Streak wynosi 1 (utrzymanie passy z wczoraj do końca bieżącego dnia)
    assert stats["streak"] == 1, "System zbyt surowo zeruje streak przed końcem dnia"

""" SUGESTIA UX: Weryfikacja, czy streak jest utrzymywany przy targecie/tyd < 7. """

# Streak przy celu 3/tydzień (oczekujemy utrzymania streaka, dostaniemy 0)
def test_stats_streak_should_persist_with_target():
    name = "WeeklyGap"
    # Tworzymy nawyk z celem 3 dni w tygodniu przez API
    response = client.post("/habits", json={"name": name, "target_per_week": 3})

    assert response.status_code == 201, f"API nie utworzyło nawyku: {response.text}"

    habit_id = response.json()["id"]

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    tuesday = monday + timedelta(days=1)
    thursday = monday + timedelta(days=3)

    seed_checkins(habit_id, [monday, tuesday, thursday])

    stats = client.get(f"/habits/{habit_id}/stats").json()
    assert stats["streak"] >= 3

    # ???


# Streak z kilku tygodni przy celu 3/tydzień (oczekujemy utrzymania streaka)
def test_stats_streak_should_ignore_gaps_within_target_logic():
    name = "TargetLogic_Trap"
    # Tworzymy nawyk: cel 3 razy w tygodniu przez API
    habit_id = client.post("/habits", json={"name": name, "target_per_week": 3}).json()["id"]

    # 1. Daty z POPRZEDNIEGO tygodnia 
    
    today = date.today()
    #current_week = [today, today - timedelta(days=2)]

    current_week_start = today - timedelta(days=today.weekday())
    past_week_start = current_week_start - timedelta(days=7)

    past_week = [
    past_week_start,
    past_week_start + timedelta(days=1),
    past_week_start + timedelta(days=2),
]
    # 2. Daty z BIEŻĄCEGO tygodnia (dzisiaj i 2 dni temu)
    current_week = [date.today(), date.today() - timedelta(days=2)]

    # Wrzucamy wszystko naraz do bazy
    seed_checkins(habit_id, past_week + current_week)

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # My oczekujemy, że streak wynosi co najmniej 2 (bo wczoraj i przedwczoraj było OK).
    assert stats["streak"] >= 2


def test_stats_not_increment_after_single_skip():
    habit_id = client.post("/habits", json={"name": "test"}).json()["id"]

    client.post(f"/habits/{habit_id}/skip", json={"day": date.today().isoformat()})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200

    stats_data = response.json()

    result = stats_data["checked_last_days"] == 0 and stats_data["streak"] == 0

    assert result, f"expected no last days checked and 0 day streak, got {stats_data["checked_last_days"]} last days and {stats_data["streak"]} day streak"

def test_stats_30_days_skip_between_checks():

    habit_id = client.post("/habits", json={"name": "test"}).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(30)]
    past_days.pop(9)

    seed_checkins(habit_id, past_days)

    skip_day = date.today() - timedelta(days=9)
    seed_skips(habit_id, [skip_day])

    response = client.get(f"/habits/{habit_id}/stats")
    stats_data = response.json()

    result = stats_data["checked_last_days"] == 9 and stats_data["streak"] == 29

    assert result, f"expected 9 last days checked and 29 day streak, got {stats_data["checked_last_days"]} last days and {stats_data["streak"]} day streak"