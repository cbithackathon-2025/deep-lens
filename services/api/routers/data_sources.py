from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/v1/data-sources", tags=["data-sources"])

DATA_SOURCES_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "copernicus-sentinel-1",
        "name": "Copernicus Sentinel-1 SAR",
        "provider": "European Space Agency (ESA)",
        "telemetry_type": "Synthetic Aperture Radar (SAR) C-band Level-1 GRD",
        "license": "CC-BY-SA 3.0 IGO / Open Access Copernicus",
        "update_frequency": "12-day repeat pass (sub-daily combined orbit)",
        "citation": "European Space Agency (2026), Copernicus Sentinel data",
        "status": "operational"
    },
    {
        "id": "noaa-crw",
        "name": "NOAA Coral Reef Watch (CRW)",
        "provider": "National Oceanic and Atmospheric Administration",
        "telemetry_type": "Daily 5km Satellite Sea Surface Temperature & Degree Heating Weeks",
        "license": "US Government Public Domain",
        "update_frequency": "Daily",
        "citation": "NOAA Coral Reef Watch (2026), Daily Global 5km Satellite Thermal Stress Telemetry",
        "status": "operational"
    },
    {
        "id": "global-fishing-watch",
        "name": "Global Fishing Watch AIS",
        "provider": "Global Fishing Watch",
        "telemetry_type": "Automatic Identification System (AIS) maritime tracking",
        "license": "CC BY-SA 4.0",
        "update_frequency": "Near real-time",
        "citation": "Global Fishing Watch (2026), Vessel Movement and Fishing Effort Data",
        "status": "operational"
    }
]

@router.get("", response_model=Dict[str, Any])
@router.get("/", response_model=Dict[str, Any])
def list_data_sources() -> Dict[str, Any]:
    """
    Returns ocean data provider provenance metadata catalog
    ensuring scientific reproducibility and data source attribution.
    """
    return {
        "total_sources": len(DATA_SOURCES_CATALOG),
        "sources": DATA_SOURCES_CATALOG
    }
