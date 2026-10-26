from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.api.routers.incidents import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_export_incidents_csv():
    response = client.get("/api/v1/incidents/export/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "id,title,category,severity" in response.text
    assert "INC-2026-001" in response.text
