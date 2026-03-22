from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_habit_with_target_success():
    name = "TargetHabit"
    payload = {
        "name": name,
        "target_per_week": 5
    }
    response = client.post("/habits", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert "target_per_week" in data

def test_create_habit_invalid_weekly_target():
    name = "InvalidTarget"
    payload = {
        "name": name,
        "target_per_week": 8
    }
    response = client.post("/habits", json=payload)

    assert response.status_code in [400, 422]

# Test na target_per_week = 0 (powinien rzucić błąd walidacji 422)
def test_create_habit_with_zero_target_fail():
    name = "ZeroTarget"
    payload = {
        "name": name,
        "target_per_week": 0
    }
    response = client.post("/habits", json=payload)

    assert response.status_code == 422
    assert "target_per_week" in response.text

# Test na brak celu (tworzenie nawyku tylko z nazwą)
def test_create_habit_without_target_success():
    name = "NoTarget"
    payload = {
        "name": name
        # brak klucza target_per_week
    }
    response = client.post("/habits", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == name
    # Sprawdzamy, czy system zapisał to jako None
    assert data["target_per_week"] is None