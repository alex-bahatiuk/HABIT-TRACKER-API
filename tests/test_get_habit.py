from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_habit_happy_path():
    name = "HappyGet"
    create_resp = client.post("/habits", json={"name": name})
    habit_id = create_resp.json()["id"]

    response = client.get(f"/habits/{habit_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name
    assert data["id"] == habit_id

# Weryfikacja, czy system poprawnie zwraca 404 dla nieistniejącego ID.
def test_get_non_existent_habit_404():
    response = client.get("/habits/999999")

    assert response.status_code == 404