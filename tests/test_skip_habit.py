from app.models.check import HabitStatus
from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

from tests.test_stats import seed_checkins, seed_skips

client = TestClient(app)

# skip today's habit (happy path)
def test_skip_habit_today():
    name = "Nawyk Dzisiaj"
    habit_resp = client.post("/habits", json={"name": name})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    skip_date = date.today().isoformat()
    
    skip_resp = client.post(f"/habits/{habit_id}/skip", json={"day": skip_date})

    assert skip_resp.status_code == 201
    assert skip_resp.json()["habit_id"] == habit_id
    assert skip_resp.json()["status"] == HabitStatus.SKIPPED

# skip yesterday's habit (allowed)
def test_skip_habit_yesterday():
    name = "Habit Yesterday"
    habit_resp = client.post("/habits", json={"name": name})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    skip_date = (date.today() - timedelta(days=1)).isoformat()
    
    skip_resp = client.post(f"/habits/{habit_id}/skip", json={"day": skip_date})

    assert skip_resp.status_code == 201
    assert skip_resp.json()["habit_id"] == habit_id
    assert skip_resp.json()["status"] == HabitStatus.SKIPPED

# skip habit from two days ago (not allowed)
def test_skip_habit_two_days_ago():
    name = "Habit Two Days Ago"
    habit_resp = client.post("/habits", json={"name": name})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    skip_date = (date.today() - timedelta(days=2)).isoformat()
    
    skip_resp = client.post(f"/habits/{habit_id}/skip", json={"day": skip_date})

    assert skip_resp.status_code == 400
    assert "Cannot skip habit more than 1 day ago" in skip_resp.text

# skip habit tomorrow (not allowed)
def test_skip_habit_tomorrow():
    name = "Habit Tomorrow"
    habit_resp = client.post("/habits", json={"name": name})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    skip_date = (date.today() + timedelta(days=1)).isoformat()
    
    skip_resp = client.post(f"/habits/{habit_id}/skip", json={"day": skip_date})

    assert skip_resp.status_code == 400
    assert "Cannot skip habit for future day" in skip_resp.text

# skip habit that does not exist (no action)
def test_skip_habit_that_does_not_exist():
    name = "Test Habit"
    habit_resp = client.post("/habits", json={"name": name})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    fake_habit_id = habit_id + 1
    skip_date = date.today().isoformat()
    
    skip_resp = client.post(f"/habits/{fake_habit_id}/skip", json={"day": skip_date})

    assert skip_resp.status_code == 404
    assert "Habit not found" in skip_resp.text

# skip habit that has already been checked (allowed/not allowed)
def test_skip_habit_that_has_already_been_checked():
    habit_resp = client.post("/habits", json={"name": "Test Habit"})

    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["id"]
    today = date.today().isoformat()
    response = client.post(f"/habits/{habit_id}/check", json={"day": today})

    assert response.status_code == 201
    assert response.json()["habit_id"] == habit_id

    skip_response = client.post(f"/habits/{habit_id}/skip", json={"day": today})
    assert skip_response.status_code == 201
    # assert skip_response.status_code == 400
    # assert "Cannot skip day that has already been checked" in response.text

# undo today's skip
def test_undo_skip_habit_today():
    name = "Test Habit"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]
    skip_date = date.today().isoformat()

    client.post(f"/habits/{habit_id}/skip", json={"day": skip_date})

    response = client.delete(f"/habits/{habit_id}/check", params={"day": skip_date})

    assert response.status_code == 204

# undo skip from two days ago
def test_undo_skip_habit_from_two_days_ago():
    name = "Test Habit"
    habit_id = client.post("/habits", json={"name": name}).json()["id"]

    skip_date = (date.today() - timedelta(days=2))
    past_days = [skip_date]

    seed_skips(habit_id, past_days)

    response = client.delete(f"/habits/{habit_id}/check", params={"day": skip_date.isoformat()})

    assert response.status_code == 400
    assert "Cannot undo skip more than 1 day ago" in response.text

def test_stats_not_increment_after_single_skip():
    habit_id = client.post("/habits", json={"name": "test"}).json()["id"]

    client.post(f"/habits/{habit_id}/skip", json={"day": date.today().isoformat()})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200

    stats_data = response.json()
    assert stats_data["checked_last_days"] == 0, f"expected no last days checked, got {stats_data["checked_last_days"]}"
    assert stats_data["streak"] == 0, f"expected 0 day streak, got {stats_data["streak"]}" 