from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_export_geojson_within_bbox():
    # Bbox covering Gulf of Mexico (contains INC-2026-001 at lon -91.20, lat 27.50)
    response = client.get("/api/v1/incidents/export/geojson?bbox=-100.0,20.0,-80.0,35.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["features"]) == 1
    assert data["features"][0]["properties"]["id"] == "INC-2026-001"

def test_export_geojson_outside_bbox():
    # Bbox covering European North Sea (contains neither sample incident)
    response = client.get("/api/v1/incidents/export/geojson?bbox=0.0,50.0,10.0,60.0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["features"]) == 0

def test_export_geojson_invalid_bbox_format():
    response = client.get("/api/v1/incidents/export/geojson?bbox=invalid,bbox")
    assert response.status_code == 400
    assert "Invalid bbox" in response.json()["detail"]
