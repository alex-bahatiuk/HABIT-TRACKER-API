from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from tests.test_stats import seed_checkins

client = TestClient(app)

# Odhaczanie dzisiaj (happy path)
def test_check_habit_today_success():
    name = "Nawyk Dzisiaj"
    habit_resp = client.post("/habits", json={"name": name})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    today = date.today().isoformat()
    response = client.post(f"/habits/{habit_id}/check", json={"day": today})

    assert response.status_code == 201
    assert response.json()["habit_id"] == habit_id

# Odhaczanie wczoraj (Dozwolone)
def test_check_habit_yesterday_success():
    name = "Nawyk Wczoraj"
    habit_resp = client.post("/habits", json={"name": name})
    habit_id = habit_resp.json()["id"]
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    response = client.post(f"/habits/{habit_id}/check", json={"day": yesterday})
    assert response.status_code == 201

# Odhaczanie przedwczoraj (zabronione)
def test_cannot_check_habit_two_days_ago():
    name = "Nawyk Przedwczoraj"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    # Data sprzed 2 dni
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()

    response = client.post(
        f"/habits/{habit_id}/check",
        json={"day": two_days_ago}
    )

    assert response.status_code == 400
    assert "Cannot check habit more than 1 day ago" in response.text

# Odhaczanie w przyszłości (Zabronione)
def test_check_habit_future_fail():
    name = "Nawyk Przyszłość"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    response = client.post(f"/habits/{habit_id}/check", json={"day": tomorrow})
    assert response.status_code == 400

# Podwójne odhaczenie tego samego dnia (Zabronione)
def test_check_habit_twice_same_day_fail():
    name = "Nawyk Podwójny"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]
    today = date.today().isoformat()

    # Pierwszy raz - OK
    client.post(f"/habits/{habit_id}/check", json={"day": today})
    # Drugi raz - Błąd
    response = client.post(f"/habits/{habit_id}/check", json={"day": today})
    assert response.status_code == 409

# check habit that does not exist (no action)
def test_check_habit_that_does_not_exist():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    fake_habit_id = habit_id + 1
    check_date = date.today().isoformat()
    
    check_resp = client.post(f"/habits/{fake_habit_id}/skip", json={"day": check_date})

    assert check_resp.status_code == 404
    assert "Habit not found" in check_resp.text

# check habit that has already been skipped (allowed/not allowed)
def test_check_habit_that_has_already_been_skipped():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    today = date.today().isoformat()
    skip_response = client.post(f"/habits/{habit_id}/skip", json={"day": today})

    assert skip_response.status_code == 201
    assert skip_response.json()["habit_id"] == habit_id

    check_response = client.post(f"/habits/{habit_id}/check", json={"day": today})
    print(check_response.status_code)
    print(check_response.text)
    assert check_response.status_code == 201

# Cofanie odhaczenia (Usuwanie)
def test_uncheck_habit_success():
    name = "Nawyk Usuwanie"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]
    today_iso = date.today().isoformat()

    client.post(f"/habits/{habit_id}/check", json={"day": today_iso})

    response = client.delete(f"/habits/{habit_id}/check", params={"day": today_iso})

    assert response.status_code == 204

# uncheck habit two days ago (not allowed)
def test_uncheck_habit_two_days_ago():
    name = "Nawyk Usuwanie"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(3)]

    seed_checkins(habit_id, past_days)

    two_days_ago = (date.today() - timedelta(days=2)).isoformat()

    response = client.delete(f"/habits/{habit_id}/check", params={"day": two_days_ago})

    assert response.status_code == 400
    assert "Cannot uncheck habit more than 1 day ago" in response.text

# sprawdzamy czy można odhaczyć 2 różne nawyki w ten sam dzień (powinno się dać)
def test_check_different_habits_same_day():
    h1 = client.post("/habits", json={"name": "H1"}).json()["id"]
    h2 = client.post("/habits", json={"name": "H2"}).json()["id"]

    today = date.today().isoformat()

    resp1 = client.post(f"/habits/{h1}/check", json={"day": today})
    resp2 = client.post(f"/habits/{h2}/check", json={"day": today})

    assert resp1.status_code == 201
    assert resp2.status_code == 201