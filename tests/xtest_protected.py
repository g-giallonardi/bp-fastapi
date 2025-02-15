from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_protected_route():
    login_response = client.post("/api/v1/auth/login", json={"email": "admin@example.com", "password": "admin123"})
    token = login_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/protected/", headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Access granted"}