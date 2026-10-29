from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_get_incident_statistics():
    response = client.get("/api/v1/incidents/stats")
    assert response.status_code == 200
    data = response.json()

    assert "total_incidents" in data
    assert data["total_incidents"] >= 2
    assert "by_category" in data
    assert "oil_slick" in data["by_category"]
    assert "vessel_blackout" in data["by_category"]
    assert "by_severity" in data
    assert "high" in data["by_severity"]
    assert "timestamp" in data
