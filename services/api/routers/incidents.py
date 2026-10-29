from fastapi import APIRouter, Query
from typing import Dict, Any
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

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

@router.get("/export/geojson", response_model=Dict[str, Any])
def export_incidents_geojson(
    category: str = Query(None, description="Filter incidents by category")
) -> Dict[str, Any]:
    """
    Exports verified ocean incidents as a GeoJSON FeatureCollection 
    for spatial GIS tools, MapLibre GL JS, and QGIS integration.
    """
    features = []
    for inc in sample_incidents:
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

@router.get("/stats", response_model=Dict[str, Any])
def get_incident_statistics() -> Dict[str, Any]:
    """
    Returns aggregate summary metrics across verified ocean incidents
    for dashboard KPI indicator cards and analytical charts.
    """
    total = len(sample_incidents)
    by_category = {}
    by_severity = {}

    for inc in sample_incidents:
        cat = inc.get("category", "unknown")
        sev = inc.get("severity", "unknown")
        by_category[cat] = by_category.get(cat, 0) + 1
        by_severity[sev] = by_severity.get(sev, 0) + 1

    return {
        "total_incidents": total,
        "by_category": by_category,
        "by_severity": by_severity,
        "active_threats": total,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
