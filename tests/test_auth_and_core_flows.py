import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_and_login_flow():
    client = APIClient()

    # Register a user
    register_payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "Secret123!",
    }
    register_resp = client.post("/api/register/", register_payload, format="json")
    assert register_resp.status_code == 201
    register_data = register_resp.json()
    assert "access" in register_data
    assert "refresh" in register_data
    assert register_data["user"]["email"] == register_payload["email"]

    # Login with same credentials
    login_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"],
    }
    login_resp = client.post("/api/login/", login_payload, format="json")
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access" in login_data
    assert "refresh" in login_data

