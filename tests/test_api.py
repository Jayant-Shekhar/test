"""Automated test suite for User Authentication Service."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Verify health endpoint responds with 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_success():
    """Verify valid credentials return 200 and an access token."""
    response = client.post(
        "/login",
        json={"username": "alice", "password": "correct_horse_battery_staple"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["username"] == "alice"
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    """
    Verify invalid credentials MUST return HTTP 401 Unauthorized.
    
    (Target test failing due to bug in app/main.py returning HTTP 200)
    """
    response = client.post(
        "/login",
        json={"username": "alice", "password": "wrong_password_attempt"},
    )
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}"


def test_login_unknown_user():
    """Verify non-existent user returns HTTP 401 Unauthorized."""
    response = client.post(
        "/login",
        json={"username": "mallory_hacker", "password": "any_password"},
    )
    assert response.status_code == 401, f"Expected HTTP 401, got {response.status_code}"


def test_login_validation_error():
    """Verify missing required parameters returns 422 Unprocessable Entity."""
    response = client.post("/login", json={"username": "alice"})
    assert response.status_code == 422
