import time
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import authenticate

client = TestClient(app)

def test_get_habit_happy_path():
    headers = authenticate()
    unique_name = f"HappyGet_{time.time()}"
    create_resp = client.post("/habits", json={"name": unique_name}, headers=headers)
    habit_id = create_resp.json()["id"]

    response = client.get(f"/habits/{habit_id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == unique_name
    assert data["id"] == habit_id

# Weryfikacja, czy system poprawnie zwraca 404 dla nieistniejącego ID.
def test_get_non_existent_habit_404():
    headers = authenticate()
    response = client.get("/habits/999999", headers=headers)

    assert response.status_code == 404