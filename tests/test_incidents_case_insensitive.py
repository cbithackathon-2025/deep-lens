from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

def test_export_geojson_case_insensitive_matching():
    # Lowercase match
    res_lower = client.get("/api/v1/incidents/export/geojson?category=oil_slick")
    assert res_lower.status_code == 200
    data_lower = res_lower.json()
    assert len(data_lower["features"]) == 1
    assert data_lower["features"][0]["properties"]["category"] == "oil_slick"

    # Uppercase match
    res_upper = client.get("/api/v1/incidents/export/geojson?category=OIL_SLICK")
    assert res_upper.status_code == 200
    data_upper = res_upper.json()
    assert len(data_upper["features"]) == 1
    assert data_upper["features"][0]["properties"]["category"] == "oil_slick"

    # Mixed case match with leading/trailing whitespace
    res_mixed = client.get("/api/v1/incidents/export/geojson?category=  Oil_Slick  ")
    assert res_mixed.status_code == 200
    data_mixed = res_mixed.json()
    assert len(data_mixed["features"]) == 1
