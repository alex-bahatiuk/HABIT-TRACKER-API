import time
from fastapi.testclient import TestClient
from app.main import app
from app.services.dependencies import oauth2_scheme
from tests.conftest import authenticate
client = TestClient(app)

# 1. Happy Path - Poprawna nazwa
def test_create_habit_success():
    unique_name = f"Nawyk {time.time()}"
    payload = {"name": unique_name}
    response = client.post("/habits", headers=authenticate(), json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == unique_name

# 2. Wartość brzegowa - Za krótka nazwa (pusty string)
def test_create_habit_too_short():
    payload = {"name": ""}
    response = client.post("/habits", json=payload, headers=authenticate())
    # FastAPI/Pydantic automatycznie wyrzuci 422 Unprocessable Entity
    assert response.status_code == 422

# 3. Wartość brzegowa - Za długa nazwa (121 znaków)
def test_create_habit_too_long():
    payload = {"name": "a" * 121}
    response = client.post("/habits", json=payload, headers=authenticate())
    assert response.status_code == 422

# 4. Błąd danych - Brak pola name w JSON
def test_create_habit_missing_field():
    payload = {}
    response = client.post("/habits", json=payload, headers=authenticate())
    assert response.status_code == 422