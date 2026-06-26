import time
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import authenticate

client = TestClient(app)

# Weryfikacja pełnego cyklu życia: Tworzenie -> Odhaczanie -> Usuwanie -> Brak śladów
def test_delete_habit_with_cascade_cleanup():
    headers = authenticate()
    # 1. Tworzymy nawyk
    unique_name = f"FullCycleTest_{time.time()}"
    habit_resp = client.post("/habits", json={"name": unique_name}, headers=headers)
    habit_id = habit_resp.json()["id"]

    # 2. Odhaczamy go (żeby sprawdzić kaskadowe usuwanie checków)
    client.post(f"/habits/{habit_id}/check", json={"day": "2026-03-02"}, headers=headers)

    # 3. Usuwamy nawyk
    delete_resp = client.delete(f"/habits/{habit_id}", headers=headers)
    assert delete_resp.status_code == 204

    # 4. Weryfikujemy, czy nawyk zniknął (404 Not Found)
    get_habit = client.get(f"/habits/{habit_id}", headers=headers)
    assert get_habit.status_code == 404

    # 5. Weryfikujemy, czy powiązane statystyki też zniknęły
    get_stats = client.get(f"/habits/{habit_id}/stats", headers=headers)
    assert get_stats.status_code == 404

# Weryfikacja: Próba usunięcia nawyku, który nie istnieje.
def test_delete_non_existent_habit_404():
    headers = authenticate()
    # Próbujemy usunąć ID, którego na pewno nie ma
    response = client.delete("/habits/888888", headers=headers)

    assert response.status_code == 404