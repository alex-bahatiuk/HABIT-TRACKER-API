import time
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from tests.test_stats import seed_checkins
client = TestClient(app)

# get habit strength of nonexistent habit (expected 404)
def test_nonexistent_habit_strength():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    fake_habit_id = habit_id + 1

    target_resp = client.get(f"/habits/{fake_habit_id}/strength")

    assert target_resp.status_code == 404
    assert "Habit not found" in target_resp.text

# get habit strength of new empty habit (expected 200 and 0 strength)
def test_new_habit_strength():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]

    target_resp = client.get(f"/habits/{habit_id}/strength")

    assert target_resp.status_code == 200
    data = target_resp.json()
    assert data["habit_id"] == habit_id
    assert data["strength"] == 0.0

# get habit strength when checked everyday for 3 days (expected 200 and 100 strength)
def test_habit_strength_3_checks_3_days():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(3)]

    seed_checkins(habit_id, past_days)

    target_resp = client.get(f"/habits/{habit_id}/strength")

    assert target_resp.status_code == 200
    data = target_resp.json()
    assert data["habit_id"] == habit_id
    assert data["strength"] == 100.0

# get habit strength when checked 5 times in last 10 days (expected 200 and 50 strength)
def test_habit_strength_5_checks_10_days():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]

    past_days = [(date.today() - timedelta(days=1 + i)) for i in range(0, 10, 2)]

    seed_checkins(habit_id, past_days)

    target_resp = client.get(f"/habits/{habit_id}/strength")

    assert target_resp.status_code == 200
    data = target_resp.json()
    assert data["habit_id"] == habit_id
    assert data["strength"] == 50.0

# get habit strength when checked 20 times in last 35 days, but 15 times in last 30 days (expected 200 and 50 strength)
def test_habit_strength_20_checks_35_days_15_checks_30_days():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]

    past_days = [(date.today() - timedelta(days=i)) for i in range(0, 30, 2)]
    past_days = past_days + [(date.today() - timedelta(days=30+i)) for i in range(5)]

    seed_checkins(habit_id, past_days)

    target_resp = client.get(f"/habits/{habit_id}/strength")

    assert target_resp.status_code == 200
    data = target_resp.json()
    assert data["habit_id"] == habit_id
    assert data["strength"] == 50.0