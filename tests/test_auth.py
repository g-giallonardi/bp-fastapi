import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

NUSER_DATA = {
    "email": "nuser@example.com",
    "password": "nuser123"
}

def test_register_success(client, db):
    """
    Test the successful registration of a user.

    Args:
        client: The test client for making HTTP requests.
        db: The test database.

    Returns:
        None
    """
    response = client.post("/api/v1/auth/register", json=NUSER_DATA)
    assert response.status_code == 201
    assert "token" in response.json()


def test_login_success(client,db):
    response = client.post("/api/v1/auth/login", json=NUSER_DATA)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail(client, db):
    response = client.post("/api/v1/auth/login", json={"email": "wrong@example.com", "password": "wrongpassword"})
    assert response.status_code == 401