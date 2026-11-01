from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_get_incident_by_id_success():
    response = client.get("/api/v1/incidents/INC-2026-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "INC-2026-001"
    assert data["category"] == "oil_slick"
    assert data["severity"] == "high"

def test_get_incident_by_id_case_insensitive():
    response = client.get("/api/v1/incidents/inc-2026-002")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "INC-2026-002"

def test_get_incident_by_id_not_found():
    response = client.get("/api/v1/incidents/INC-NONEXISTENT")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()
