from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "deep-lens-api"
    assert "version" in data
    assert "timestamp" in data

def test_api_v1_health_alias():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
