import sys
import os
from datetime import date, timedelta
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.core.database import SessionLocal
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
    name = "StatTest"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    client.post(f"/habits/{habit_id}/check", json={"day": date.today().isoformat()})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200

    stats_data = response.json()
    assert stats_data["streak"] == 1
    assert stats_data["checked_last_days"] == 1


def test_stats_30_days():
    name = "30days"
    # Tworzymy nawyk przez API
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    # Przygotowujemy listę dat (30 dni wstecz)
    past_days = [(date.today() - timedelta(days=i)) for i in range(30)]

    # Wstrzykujemy je prosto do bazy (omijamy walidację API)
    seed_checkins(habit_id, past_days)

    # Sprawdzamy, czy statystyki je widzą
    response = client.get(f"/habits/{habit_id}/stats")
    assert response.json()["checked_last_days"] == 30


def test_stats_total_count_limit_check():
    name = "LimitTest"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    # Generujemy listę 100 dat (od dziś do 99 dni wstecz)
    past_days = [date.today() - timedelta(days=i) for i in range(100)]

    # Wstrzykujemy wszystko do bazy
    seed_checkins(habit_id, past_days)

    # Sprawdzamy, czy statystyki z parametrem days=100 widzą wszystko
    response = client.get(f"/habits/{habit_id}/stats", params={"days": 100})
    stats = response.json()

    assert stats.get("checked_last_days", 0) == 100


# Weryfikacja, czy przerwa w dniach poprawnie przerywa streak.
def test_stats_streak_calculation_with_gap():
    name = "GapTest"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    # Grupa 1: Ciąg 3 dni (dzisiaj, wczoraj, przedwczoraj) -> Streak powinien być 3
    streak_days = [date.today() - timedelta(days=i) for i in range(3)]

    # Grupa 2: Pojedynczy wpis 5 dni temu (po luce 4 dni temu) -> Nie powinien przedłużać streaka
    old_day = [date.today() - timedelta(days=5)]

    # Wrzucamy wszystko do bazy (razem 4 wpisy)
    seed_checkins(habit_id, streak_days + old_day)

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # Streak powinien wynosić 3 (tylko najnowszy ciąg wstecz od dzisiaj)
    assert stats["streak"] == 3


def test_stats_should_allow_more_than_365_days():
    name = "LongTerm"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    # 1. Wstrzykujemy 400 dni
    past_days = [date.today() - timedelta(days=i) for i in range(400)]
    seed_checkins(habit_id, past_days)

    # 2. Pytamy o 400 dni
    response = client.get(f"/habits/{habit_id}/stats", params={"days": 400})
    assert response.status_code == 200

    # 3. Sprawdzamy, czy licznik nie uciął danych na 365
    stats = response.json()
    assert stats["checked_last_days"] == 400


def test_stats_streak_grace_period_ux():
    name = "UX_Test"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    # Odhaczamy tylko wczoraj
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    client.post(f"/habits/{habit_id}/check", json={"day": yesterday})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # Oczekiwanie: Streak wynosi 1 (utrzymanie passy z wczoraj do końca bieżącego dnia)
    assert stats["streak"] == 1


# Streak przy celu 3/tydzień (oczekujemy utrzymania streaka)
def test_weekly_streak_with_gap_but_target_met():

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

    # Sprawdzamy, czy system widzi 5 dni streaka (3 z tamtego tygodnia + 2 z tego)
    assert stats["streak"] == 5, f"Oczekiwano 5 dni streaka, a system pokazał {stats['streak']}."