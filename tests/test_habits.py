from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_habit_and_check_twice_same_day_should_fail():
    # Tworzymy nawyk
    r = client.post("/habits", json={"name": "Drink water"})
    assert r.status_code == 201
    habit_id = r.json()["id"]

    day = "2026-02-24"
    # Pierwsze odhaczenie dnia
    r1 = client.post(f"/habits/{habit_id}/check", json={"day": day})
    assert r1.status_code == 201

    # Próba ponownego odhaczenia tego samego dnia - powinna zwrócić błąd 409
    r2 = client.post(f"/habits/{habit_id}/check", json={"day": day})
    assert r2.status_code == 409
    assert r2.json()["detail"] == "This day is already checked"