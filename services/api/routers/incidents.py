from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

SAMPLE_INCIDENTS = [
    {
        "id": "INC-2026-001",
        "title": "Sentinel-1 Detected SAR Oil Slick",
        "category": "oil_slick",
        "severity": "high",
        "latitude": 27.50,
        "longitude": -91.20,
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": "INC-2026-002",
        "title": "AIS Transponder Blackout Incursion",
        "category": "vessel_blackout",
        "severity": "medium",
        "latitude": -0.85,
        "longitude": -89.40,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
]

@router.get("/export/geojson", response_model=Dict[str, Any])
def export_incidents_geojson(
    category: str = Query(None, description="Filter incidents by category")
) -> Dict[str, Any]:
    """
    Exports verified ocean incidents as a GeoJSON FeatureCollection 
    for spatial GIS tools, MapLibre GL JS, and QGIS integration.
    """
    features = []
    for inc in SAMPLE_INCIDENTS:
        if category and inc["category"] != category:
            continue
            
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [inc["longitude"], inc["latitude"]]
            },
            "properties": {
                "id": inc["id"],
                "title": inc["title"],
                "category": inc["category"],
                "severity": inc["severity"],
                "timestamp": inc["timestamp"]
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }

@router.get("/{incident_id}", response_model=Dict[str, Any])
def get_incident_by_id(incident_id: str) -> Dict[str, Any]:
    """
    Fetches detailed metadata and telemetry for a specific incident by ID.
    Raises 404 HTTPException if not found.
    """
    for inc in SAMPLE_INCIDENTS:
        if inc["id"].lower() == incident_id.strip().lower():
            return inc
    raise HTTPException(status_code=404, detail=f"Incident with ID '{incident_id}' not found")
