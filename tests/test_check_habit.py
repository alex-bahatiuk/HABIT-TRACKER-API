import time
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import authenticate
from tests.test_stats import seed_checkins

client = TestClient(app)

# Odhaczanie dzisiaj (happy path)
def test_check_habit_today_success():
    # Dodajemy timestamp do nazwy, żeby nazwa była unikalna i test nie traktował ich jako duplikaty
    headers = authenticate()
    unique_name = f"Nawyk {time.time()}"
    habit_resp = client.post("/habits", json={"name": unique_name}, headers=headers)

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    today = date.today().isoformat()
    response = client.post(f"/habits/{habit_id}/check", json={"day": today}, headers=headers)

    assert response.status_code == 201
    assert response.json()["habit_id"] == habit_id

# Odhaczanie wczoraj (Dozwolone)
def test_check_habit_yesterday_success():
    headers = authenticate()
    unique_name = f"Nawyk {time.time()}"
    habit_resp = client.post("/habits", json={"name": unique_name}, headers=headers)
    habit_id = habit_resp.json()["id"]
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    response = client.post(f"/habits/{habit_id}/check", json={"day": yesterday}, headers=headers)
    assert response.status_code == 201

# Odhaczanie przedwczoraj
def test_check_habit_two_days_ago():
    headers = authenticate()
    unique_name = f"Nawyk {time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()

    response = client.post(f"/habits/{habit_id}/check", json={"day": two_days_ago}, headers=headers)
    assert response.status_code == 400

# Odhaczanie w przyszłości (Zabronione)
def test_check_habit_future_fail():
    headers = authenticate()
    unique_name = f"Nawyk {time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    response = client.post(f"/habits/{habit_id}/check", json={"day": tomorrow}, headers=headers)
    assert response.status_code == 400

# Podwójne odhaczenie tego samego dnia (Zabronione)
def test_check_habit_twice_same_day_fail():
    headers = authenticate()
    unique_name = f"Nawyk {time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]
    today = date.today().isoformat()

    # Pierwszy raz - OK
    client.post(f"/habits/{habit_id}/check", json={"day": today}, headers=headers)
    # Drugi raz - Błąd
    response = client.post(f"/habits/{habit_id}/check", json={"day": today}, headers=headers)
    assert response.status_code == 409

# check habit that does not exist (no action)
def test_check_habit_that_does_not_exist():
    headers = authenticate()
    habit_resp = client.post("/habits", json={"name": "Test Habit"}, headers=headers)

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    fake_habit_id = habit_id + 1
    check_date = date.today().isoformat()
    
    check_resp = client.post(f"/habits/{fake_habit_id}/skip", json={"day": check_date}, headers=headers)

    assert check_resp.status_code == 404
    assert "Habit not found" in check_resp.text

# check habit that has already been skipped (allowed/not allowed)
def test_check_habit_that_has_already_been_skipped():
    headers = authenticate()
    habit_resp = client.post("/habits", json={"name": "Test Habit"}, headers=headers)

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    today = date.today().isoformat()
    skip_response = client.post(f"/habits/{habit_id}/skip", json={"day": today}, headers=headers)

    assert skip_response.status_code == 201
    assert skip_response.json()["habit_id"] == habit_id

    check_response = client.post(f"/habits/{habit_id}/check", json={"day": today}, headers=headers)
    print(check_response.status_code)
    print(check_response.text)
    assert check_response.status_code == 201

# Cofanie odhaczenia (Usuwanie)
def test_uncheck_habit_success():
    headers = authenticate()
    unique_name = f"Nawyk_{time.time()}"
    habit_id = client.post("/habits", json={"name": unique_name}, headers=headers).json()["id"]
    today_iso = date.today().isoformat()

    client.post(f"/habits/{habit_id}/check", json={"day": today_iso}, headers=headers)

    response = client.delete(f"/habits/{habit_id}/check", params={"day": today_iso}, headers=headers)

    assert response.status_code == 204

# sprawdzamy czy można odhaczyć 2 różne nawyki w ten sam dzień (powinno się dać)
def test_check_different_habits_same_day():
    headers = authenticate()
    h1 = client.post("/habits", json={"name": f"H1_{time.time()}"}, headers=headers).json()["id"]
    h2 = client.post("/habits", json={"name": f"H2_{time.time()}"}, headers=headers).json()["id"]

    today = date.today().isoformat()

    resp1 = client.post(f"/habits/{h1}/check", json={"day": today}, headers=headers)
    resp2 = client.post(f"/habits/{h2}/check", json={"day": today}, headers=headers)

    assert resp1.status_code == 201
    assert resp2.status_code == 201