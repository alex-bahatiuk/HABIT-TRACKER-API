import time
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import authenticate

client = TestClient(app)

def test_create_habit_with_target_success():
    headers = authenticate()

    unique_name = f"TargetHabit_{time.time()}"
    payload = {
        "name": unique_name,
        "target_per_week": 5
    }
    response = client.post("/habits", json=payload, headers=headers)
    data = response.json()

    assert response.status_code == 201
    assert "target_per_week" in data

def test_create_habit_invalid_weekly_target():
    headers = authenticate()
    unique_name = f"InvalidTarget_{time.time()}"
    payload = {
        "name": unique_name,
        "target_per_week": 8
    }
    response = client.post("/habits", json=payload, headers=headers)

    assert response.status_code in [400, 422]

# Test na target_per_week = 0 (powinien rzucić błąd walidacji 422)
def test_create_habit_with_zero_target_fail():
    headers = authenticate()
    unique_name = f"ZeroTarget_{time.time()}"
    payload = {
        "name": unique_name,
        "target_per_week": 0
    }
    response = client.post("/habits", json=payload, headers=headers)

    assert response.status_code == 422
    assert "target_per_week" in response.text

# Test na brak celu (tworzenie nawyku tylko z nazwą)
def test_create_habit_without_target_success():
    headers = authenticate()
    unique_name = f"NoTarget_{time.time()}"
    payload = {
        "name": unique_name
        # brak klucza target_per_week
    }
    response = client.post("/habits", json=payload, headers=headers)
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == unique_name
    # Sprawdzamy, czy system zapisał to jako None
    assert data["target_per_week"] is None