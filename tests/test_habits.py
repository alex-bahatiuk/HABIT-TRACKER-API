from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta, datetime

from tests.conftest import authenticate
client = TestClient(app)

def test_create_habit_and_check_twice_same_day_should_fail():
    headers = authenticate()
    r = client.post("/habits", json={"name": "Drink water"}, headers=headers)
    assert r.status_code in (201, 409)
    print("create:", r.status_code, r.json())

    # получаем id (если уже был 409 — тест можно упростить под чистую базу)
    if r.status_code == 201:
        habit_id = r.json()["id"]
    else:
        # если привычка уже существует, найдём её через list
        habits = client.get("/habits", headers=headers).json()
        print("habits:", habits)
        habit_id = next(h["id"] for h in habits if h["name"] == "Drink water")

    day = date.today().isoformat()
    r1 = client.post(f"/habits/{habit_id}/check", json={"day": day}, headers=headers)
    print("first check:", r1.status_code, r1.json())
    
    assert r1.status_code in (201, 409)

    r2 = client.post(f"/habits/{habit_id}/check", json={"day": day}, headers=headers)
    print("second check:", r2.status_code, r2.json())
    assert r2.status_code == 409
    assert r2.json()["detail"] == "This day is already checked"