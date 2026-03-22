from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Weryfikacja pełnego cyklu życia: Tworzenie -> Odhaczanie -> Usuwanie -> Brak śladów
def test_delete_habit_with_cascade_cleanup():
    # 1. Tworzymy nawyk
    name = "Full Cycle Test"
    habit_resp = client.post("/habits", json={"name": name})
    habit_id = habit_resp.json()["id"]

    # 2. Odhaczamy go (żeby sprawdzić kaskadowe usuwanie checków)
    client.post(f"/habits/{habit_id}/check", json={"day": "2026-03-02"})

    # 3. Usuwamy nawyk
    delete_resp = client.delete(f"/habits/{habit_id}")
    assert delete_resp.status_code == 204

    # 4. Weryfikujemy, czy nawyk zniknął (404 Not Found)
    get_habit = client.get(f"/habits/{habit_id}")
    assert get_habit.status_code == 404

    # 5. Weryfikujemy, czy powiązane statystyki też zniknęły
    get_stats = client.get(f"/habits/{habit_id}/stats")
    assert get_stats.status_code == 404

# Weryfikacja: Próba usunięcia nawyku, który nie istnieje.
def test_delete_non_existent_habit_404():
    # Próbujemy usunąć ID, którego na pewno nie ma
    response = client.delete("/habits/888888")

    assert response.status_code == 404