from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_habit_and_check_twice_same_day_should_fail():
    r = client.post("/habits", json={"name": "Drink water"})
    assert r.status_code in (201, 409)

    # получаем id (если уже был 409 — тест можно упростить под чистую базу)
    if r.status_code == 201:
        habit_id = r.json()["id"]
    else:
        # если привычка уже существует, найдём её через list
        habits = client.get("/habits").json()
        habit_id = next(h["id"] for h in habits if h["name"] == "Drink water")

    day = "2026-02-24"
    r1 = client.post(f"/habits/{habit_id}/check", json={"day": day})
    assert r1.status_code in (201, 409)

    r2 = client.post(f"/habits/{habit_id}/check", json={"day": day})
    assert r2.status_code == 409
    assert r2.json()["detail"] == "This day is already checked"