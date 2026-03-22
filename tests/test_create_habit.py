from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

# 1. Happy Path - Poprawna nazwa
def test_create_habit_success():
    name = "Poprawny Nawyk"
    payload = {"name": name}
    response = client.post("/habits", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == name

# 2. Wartość brzegowa - Za krótka nazwa (pusty string)
def test_create_habit_too_short():
    payload = {"name": ""}
    response = client.post("/habits", json=payload)
    # FastAPI/Pydantic automatycznie wyrzuci 422 Unprocessable Entity
    assert response.status_code == 422

# 3. Wartość brzegowa - Za długa nazwa (121 znaków)
def test_create_habit_too_long():
    payload = {"name": "a" * 121}
    response = client.post("/habits", json=payload)
    assert response.status_code == 422

# 4. Błąd danych - Brak pola name w JSON
def test_create_habit_missing_field():
    payload = {}
    response = client.post("/habits", json=payload)
    assert response.status_code == 422