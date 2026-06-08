import time
from datetime import date, timedelta
from app.core.database import SessionLocal
from freezegun import freeze_time

from fastapi.testclient import TestClient
from app.main import app
from app.models.check import HabitCheck, HabitStatus
from tests.conftest import authenticate

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
    headers = authenticate()
    unique_name = f"StatTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]

    client.post(f"/habits/{habit_id}/check", json={"day": date.today().isoformat()}, headers=headers)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    assert response.status_code == 200

    stats_data = response.json()
    assert stats_data["streak"] == 1
    assert stats_data["checked_last_days"] == 1

def test_stats_30_days():
    headers = authenticate()
    unique_name = f"30days_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(30)]
    seed_checkins(habit_id, past_days)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    stats = response.json()

    assert stats["checked_last_days"] == 30

def test_stats_total_count_limit_check():
    headers = authenticate()
    unique_name = f"LimitTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]

    days = 100
    past_days = [(date.today() - timedelta(days=i)) for i in range(days)]
    seed_checkins(habit_id, past_days)

    response = client.get(f"/habits/{habit_id}/stats", params={"days": days}, headers=headers)
    stats = response.json()

    actual_checks = stats.get("checked_last_days", 0, headers=headers)
    assert actual_checks == days

#  Weryfikacja, czy przerwa w dniach poprawnie przerywa streak.
def test_stats_streak_calculation_with_gap():
    headers = authenticate()
    unique_name = f"GapTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(5)]
    past_days.pop(3)
    seed_checkins(habit_id, past_days)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    stats = response.json()

    # Streak powinien liczyć ciąg wstecz od dzisiaj (3 dni), ignorując wpis sprzed przerwy
    assert stats["streak"] == 3


# TEST LIMITU 365 DNI
def test_stats_should_allow_more_than_365_days():
    headers = authenticate()
    unique_name = f"LongTerm_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]
    #today= date.today()
    response = client.get(f"/habits/{habit_id}/stats", params={"days": 400}, headers=headers)

    assert response.status_code == 200


""" SUGESTIA UX: Weryfikacja, czy streak jest utrzymywany, jeśli dzisiejszy dzień 
nie został jeszcze odhaczony (szansa dla użytkownika). """

def test_stats_streak_grace_period_ux():
    headers = authenticate()
    unique_name = f"UX_Test_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]

    # Odhaczamy tylko wczoraj
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    client.post(f"/habits/{habit_id}/check", json={"day": yesterday}, headers=headers)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    stats = response.json()

    # Oczekiwanie: Streak wynosi 1 (utrzymanie passy z wczoraj do końca bieżącego dnia)
    assert stats["streak"] == 1, "System zbyt surowo zeruje streak przed końcem dnia"

""" SUGESTIA UX: Weryfikacja, czy streak jest utrzymywany przy targecie/tyd < 7. """

# Streak przy celu 3/tydzień (oczekujemy utrzymania streaka, dostaniemy 0)
@freeze_time("2026-05-03")
def test_stats_streak_should_persist_with_target():
    headers = authenticate()
    name = "WeeklyGap"
    # Tworzymy nawyk z celem 3 dni w tygodniu przez API
    response = client.post("/habits", json={"name": name, "target_per_week": 3}, headers=headers)

    assert response.status_code == 201, f"API nie utworzyło nawyku: {response.text}"

    habit_id = response.json()["id"]

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    tuesday = monday + timedelta(days=1)
    thursday = monday + timedelta(days=3)

    seed_checkins(habit_id, [monday, tuesday, thursday])

    stats = client.get(f"/habits/{habit_id}/stats", headers=headers).json()
    assert stats["streak"] >= 3

# Streak z kilku tygodni przy celu 3/tydzień (oczekujemy utrzymania streaka)
@freeze_time("2026-05-03") # niedziela
def test_stats_streak_should_ignore_gaps_within_target_logic():
    headers = authenticate()
    name = "TargetLogic_Trap"
    # Tworzymy nawyk: cel 3 razy w tygodniu przez API
    habit_id = client.post("/habits", json={"name": name, "target_per_week": 3}, headers=headers).json()["id"]

    # 1. Daty z POPRZEDNIEGO tygodnia 
    
    today = date.today()
    #current_week = [today, today - timedelta(days=2)]

    current_week_start = today - timedelta(days=today.weekday())
    past_week_start = current_week_start - timedelta(days=7)

    past_week_checks = [
        past_week_start,
        past_week_start + timedelta(days=2),
    ]
    past_week_skips = [
        past_week_start + timedelta(days=1),
    ]
    # 2. Daty z BIEŻĄCEGO tygodnia (dzisiaj i 2 dni temu)
    current_week = [date.today(), date.today() - timedelta(days=2)]

    # Wrzucamy wszystko naraz do bazy
    seed_checkins(habit_id, past_week_checks + current_week)
    seed_skips(habit_id, past_week_skips)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    stats = response.json()

    # My oczekujemy, że streak wynosi co najmniej 2 (bo wczoraj i przedwczoraj było OK).
    assert stats["streak"] == 5, f"expected 5 day streak, got {stats["streak"]}"

@freeze_time("2026-05-03") # niedziela
def test_stats_incomplete_week_between_complete_ones():
    headers = authenticate()
    name = "test habit"
    habit_id = client.post("/habits", json={"name": name, "target_per_week": 2}, headers=headers).json()["id"]

    today = date.today()
    current_week_start = today - timedelta(days=today.weekday())
    one_week_ago_start = current_week_start - timedelta(days=7)
    two_weeks_ago_start = one_week_ago_start - timedelta(days=7)

    current_week_checks = [
        current_week_start,
        current_week_start + timedelta(days=3),
    ]

    one_week_ago_checks = [
        one_week_ago_start + timedelta(days=5),
    ]

    two_weeks_ago_checks = [
        two_weeks_ago_start,
        two_weeks_ago_start + timedelta(days=1),
    ]

    seed_checkins(habit_id, two_weeks_ago_checks + one_week_ago_checks + current_week_checks)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    stats = response.json()

    assert stats["streak"] == 2, f"expected 2 day streak, got {stats["streak"]}"

@freeze_time("2026-05-03") # niedziela
def test_stats_blank_week_between_complete_ones():
    headers = authenticate()
    name = "test habit"
    habit_id = client.post("/habits", json={"name": name, "target_per_week": 2}, headers=headers).json()["id"]

    today = date.today()
    current_week_start = today - timedelta(days=today.weekday())
    one_week_ago_start = current_week_start - timedelta(days=7)
    two_weeks_ago_start = one_week_ago_start - timedelta(days=7)

    current_week_checks = [
        current_week_start,
        current_week_start + timedelta(days=3),
    ]

    two_weeks_ago_checks = [
        two_weeks_ago_start,
        two_weeks_ago_start + timedelta(days=1),
    ]

    seed_checkins(habit_id, two_weeks_ago_checks + current_week_checks)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    stats = response.json()

    assert stats["streak"] == 2, f"expected 2 day streak, got {stats["streak"]}"


def test_stats_not_increment_after_single_skip():
    headers = authenticate()
    habit_id = client.post("/habits", json={"name": "test"}, headers=headers).json()["id"]

    client.post(f"/habits/{habit_id}/skip", json={"day": date.today().isoformat()}, headers=headers)

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)
    assert response.status_code == 200

    stats_data = response.json()

    result = stats_data["checked_last_days"] == 0 and stats_data["streak"] == 0

    assert result, f"expected no last days checked and 0 day streak, got {stats_data["checked_last_days"]} last days and {stats_data["streak"]} day streak"

def test_stats_30_days_skip_between_checks():
    headers = authenticate()

    habit_id = client.post("/habits", json={"name": "test"}, headers=headers).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(30)]
    past_days.pop(9)

    seed_checkins(habit_id, past_days)

    skip_day = date.today() - timedelta(days=9)
    seed_skips(habit_id, [skip_day])

    response = client.get(f"/habits/{habit_id}/stats", headers=headers)

    stats_data = response.json()

    result = stats_data["checked_last_days"] == 9 and stats_data["streak"] == 29

    assert result, f"expected 9 last days checked and 29 day streak, got {stats_data["checked_last_days"]} last days and {stats_data["streak"]} day streak"