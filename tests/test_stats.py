import time
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Czy statystyki poprawnie inicjalizują się po pierwszym odhaczeniu.
def test_stats_increment_after_single_checkin():
    unique_name = f"StatTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    client.post(f"/habits/{habit_id}/check", json={"day": date.today().isoformat()})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200

    stats_data = response.json()
    assert stats_data["streak"] == 1
    assert stats_data["checked_last_30_days"] == 1

# Weryfikacja wartości brzegowej - czy system poprawnie zlicza dokładnie 30 dni.
def test_stats_boundary_30_days():
    unique_name = f"Boundary30_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    for i in range(30):
        past_day = (date.today() - timedelta(days=i)).isoformat()
        client.post(f"/habits/{habit_id}/check", json={"day": past_day})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

    assert stats["checked_last_30_days"] == 30

# BUG - Weryfikacja licznika całkowitego przy 100 wpisach (system gubi dane powyżej 30 dni)
def test_stats_total_count_limit_check():
    unique_name = f"LimitTest_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}).json()["id"]

    for i in range(100):
        past_day = (date.today() - timedelta(days=i)).isoformat()
        client.post(f"/habits/{habit_id}/check", json={"day": past_day})

    response = client.get(f"/habits/{habit_id}/stats")
    stats = response.json()

   # wzięłam pole "checked_last_30_days", ponieważ nie znalazłam pola "total"
    actual_checks = stats.get("checked_last_30_days", 0)
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