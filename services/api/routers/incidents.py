from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

@router.get("/export/geojson", response_model=Dict[str, Any])
def export_incidents_geojson(
    category: Optional[str] = Query(None, description="Filter incidents by category"),
    bbox: Optional[str] = Query(None, description="Spatial bounding box formatted as 'min_lon,min_lat,max_lon,max_lat'")
) -> Dict[str, Any]:
    """
    Exports verified ocean incidents as a GeoJSON FeatureCollection 
    for spatial GIS tools, MapLibre GL JS, and QGIS integration.
    Supports optional spatial bounding box (bbox) and category filtering.
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

    min_lon = min_lat = max_lon = max_lat = None
    if bbox:
        try:
            parts = [float(x.strip()) for x in bbox.split(",")]
            if len(parts) == 4:
                min_lon, min_lat, max_lon, max_lat = parts
            else:
                raise ValueError("BBOX must have exactly 4 numbers: min_lon,min_lat,max_lon,max_lat")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid bbox parameter format: {e}")

    features = []
    for inc in sample_incidents:
        if category and inc["category"] != category:
            continue
            
        if min_lon is not None:
            lon = inc["longitude"]
            lat = inc["latitude"]
            if not (min_lon <= lon <= max_lon and min_lat <= lat <= max_lat):
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
