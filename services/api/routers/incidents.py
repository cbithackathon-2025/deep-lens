from fastapi import APIRouter, Query
from typing import Dict, Any
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

@router.get("/export/geojson", response_model=Dict[str, Any])
def export_incidents_geojson(
    category: str = Query(None, description="Filter incidents by category")
) -> Dict[str, Any]:
    """
    Exports verified ocean incidents as a GeoJSON FeatureCollection 
    for spatial GIS tools, MapLibre GL JS, and QGIS integration.
    """
    sample_incidents = [
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

    features = []
    category_norm = category.strip().lower() if category else None
    for inc in sample_incidents:
        if category_norm and inc["category"].lower() != category_norm:
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
