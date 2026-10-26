import csv
import io
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Query, Response

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

@router.get("/export/csv")
def export_incidents_csv(
    category: str = Query(None, description="Filter incidents by category")
) -> Response:
    """
    Exports verified ocean incidents as a downloadable CSV file.
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

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "category", "severity", "latitude", "longitude", "timestamp"])

    for inc in sample_incidents:
        if category and inc["category"] != category:
            continue
        writer.writerow([
            inc["id"], inc["title"], inc["category"], 
            inc["severity"], inc["latitude"], inc["longitude"], inc["timestamp"]
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ocean_incidents.csv"}
    )
