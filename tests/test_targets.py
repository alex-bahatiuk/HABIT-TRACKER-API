import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# BUG: System pozwala stworzyć nawyk, ale ignoruje pole 'target'. W bazie danych nie ma kolumny na cel tygodniowy.
def test_create_habit_with_target_is_ignored():
    unique_name = f"TargetHabit_{time.time()}"
    payload = {
        "name": unique_name,
        "target": 5
    }
    response = client.post("/habits", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert "target" in data

# BUG przez brak pola target - Weryfikacja walidacji: Cel tygodniowy nie może być większy niż 7.
def test_create_habit_invalid_weekly_target():
    unique_name = f"InvalidTarget_{time.time()}"
    payload = {
        "name": unique_name,
        "target": 8
    }
    response = client.post("/habits", json=payload)

    assert response.status_code in [400, 422]