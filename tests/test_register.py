from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

valid_email = "user@mail.com"
strong_password = "c6CDpo&JGZ"

def test_register_valid_data_success():
    register_res = client.post("/auth/register", json={"email": valid_email, "password": strong_password})

    assert register_res.status_code == 201

    assert register_res.json()["email"] == valid_email

def test_register_invalid_email_format_failure():
    invalid_email = "user.mail.com"
    register_res = client.post("/auth/register", json={"email": invalid_email, "password": strong_password})

    assert register_res.status_code == 422

def test_register_empty_password_failure():
    register_res = client.post("/auth/register", json={"email": valid_email, "password": ""})

    assert register_res.status_code == 422

def test_register_very_long_password_failure():
    password = "x" * 100
    register_res = client.post("/auth/register", json={"email": valid_email, "password": password})

    assert register_res.status_code == 422

def test_register_very_short_password_failure():
    password = "abcd"
    register_res = client.post("/auth/register", json={"email": valid_email, "password": password})

    assert register_res.status_code == 422

def test_register_very_simple_password_failure():
    password = "a" * 8
    register_res = client.post("/auth/register", json={"email": valid_email, "password": password})

    assert register_res.status_code == 422

def test_register_very_common_password_failure():
    password = "Password1!"
    register_res = client.post("/auth/register", json={"email": valid_email, "password": password})

    assert register_res.status_code == 422