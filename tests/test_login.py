from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_valid_data_success():
    email = "user@mail.com"
    password = "password"
    client.post("/auth/register", json={"email": email, "password": password})

    login_res = client.post("/auth/login", data={"username": email, "password": password})

    assert login_res.status_code == 200

def test_login_unregistered_email_failure():
    email = "user@mail.com"
    password = "password"
    client.post("/auth/register", json={"email": email, "password": password})

    unregistered_email = "admin@mail.net"
    login_res = client.post("/auth/login", data={"username": unregistered_email, "password": password})

    assert login_res.status_code == 400

def test_login_invalid_password_failure():
    email = "user@mail.com"
    password = "password"
    client.post("/auth/register", json={"email": email, "password": password})

    invalid_password = "drowssap"
    login_res = client.post("/auth/login", data={"username": email, "password": invalid_password})

    assert login_res.status_code == 400