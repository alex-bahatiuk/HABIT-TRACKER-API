import time
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


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

    for i in range(30):
        past_day = (date.today() - timedelta(days=i)).isoformat()
        client.post(f"/habits/{habit_id}/check", json={"day": past_day})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    assert stats["checked_last_days"] == 30


def test_stats_total_count_limit_check():
    unique_name = f"LimitTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    for i in range(100):
        past_day = (date.today() - timedelta(days=i)).isoformat()
        client.post(f"/habits/{habit_id}/check", json={"day": past_day})

    response = client.get(f"/habits/{habit_id}/stats", params={"days": 100})
    stats = response.json()

    actual_checks = stats.get("checked_last_days", 0)
    assert actual_checks == 100


#  Weryfikacja, czy przerwa w dniach poprawnie przerywa streak.
def test_stats_streak_calculation_with_gap():
    unique_name = f"GapTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    # Ciąg 3 dni (dzisiaj, wczoraj, przedwczoraj)
    for i in range(3):
        day = (date.today() - timedelta(days=i)).isoformat()
        client.post(f"/habits/{habit_id}/check", json={"day": day})

    # Dzień przerwy (4 dni temu puste) i wpis 5 dni temu
    five_days_ago = (date.today() - timedelta(days=4)).isoformat()
    client.post(f"/habits/{habit_id}/check", json={"day": five_days_ago})

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


def test_stats_streak_grace_period_ux():
    unique_name = f"UX_Test_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    # Odhaczamy tylko wczoraj
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    client.post(f"/habits/{habit_id}/check", json={"day": yesterday})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # Oczekiwanie: Streak wynosi 1 (utrzymanie passy z wczoraj do końca bieżącego dnia)
    assert stats["streak"] == 1


# Streak przy celu 3/tydzień (oczekujemy utrzymania streaka)
def test_stats_streak_should_persist_with_target():
    unique_name = f"TargetLogic_{time.time()}"
    # Tworzymy nawyk z celem 3 razy w tygodniu
    habit_id = client.post("/habits",
                           json={"name": unique_name, "target_per_week": 3}).json()["id"]

    # Użytkownik odhaczył wczoraj i przedwczoraj (realizuje plan 3/tydzień)
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    client.post(f"/habits/{habit_id}/check", json={"day": yesterday})
    client.post(f"/habits/{habit_id}/check", json={"day": two_days_ago})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # My oczekujemy, że streak wynosi co najmniej 2 (bo wczoraj i przedwczoraj było OK).
    assert stats["streak"] >= 2


def test_stats_streak_should_ignore_gaps_within_target_logic():
    unique_name = f"TargetLogic_Gap_{time.time()}"
    # Tworzymy nawyk: cel 3 razy w tygodniu.

    habit_id = client.post("/habits",
                           json={"name": unique_name, "target_per_week": 3}).json()["id"]

    # Scenariusz: Odhaczone dzisiaj i 2 dni temu. Wczoraj był zaplanowany dzień wolny.
    today = date.today().isoformat()
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()

    client.post(f"/habits/{habit_id}/check", json={"day": today})
    client.post(f"/habits/{habit_id}/check", json={"day": two_days_ago})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    # Logika celu (3/tydzień) mówi, że to nadal jest streak, bo plan jest realizowany.
    # Obecna pętla 'while' w stats_service.py tu "pęknie" i zwróci tylko 1 (za dziś).
    assert stats["streak"] >= 2, "Streak powinien przetrwać zaplanowaną przerwę wewnątrz celu tygodniowego"
