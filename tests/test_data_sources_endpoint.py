from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_list_data_sources_success():
    response = client.get("/api/v1/data-sources")
    assert response.status_code == 200
    data = response.json()

    assert "total_sources" in data
    assert data["total_sources"] >= 3
    assert "sources" in data

    source_ids = [s["id"] for s in data["sources"]]
    assert "copernicus-sentinel-1" in source_ids
    assert "noaa-crw" in source_ids
    assert "global-fishing-watch" in source_ids

    # Validate schema fields on first source
    src = data["sources"][0]
    assert "provider" in src
    assert "telemetry_type" in src
    assert "license" in src
    assert "citation" in src
