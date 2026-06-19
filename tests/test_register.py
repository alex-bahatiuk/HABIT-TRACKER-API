from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_valid_data_success():
    email = "user@mail.com"
    password = "password"
    register_res = client.post("/auth/register", json={"email": email, "password": password})

    assert register_res.status_code == 201

    assert register_res.json()["email"] == email

def test_register_invalid_email_format_failure():
    email = "user.mail.com"
    password = "password"
    register_res = client.post("/auth/register", json={"email": email, "password": password})

    print("print res: ", register_res)
    print(register_res.json())
    assert register_res.status_code == 422

def test_register_empty_password_failure():
    email = "user@mail.com"
    password = ""
    register_res = client.post("/auth/register", json={"email": email, "password": password})

    assert register_res.status_code == 422

