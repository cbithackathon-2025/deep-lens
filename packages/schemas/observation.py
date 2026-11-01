"""Observation data schemas."""
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ObservationType(str, Enum):
    ENVIRONMENTAL = "environmental"
    THERMAL_STRESS = "thermal_stress"
    ACOUSTIC = "acoustic"
    SATELLITE = "satellite"
    POLLUTION = "pollution"
    VESSEL_TRACKING = "vessel_tracking"
    OIL_SLICK = "oil_slick"
    VESSEL_ANOMALY = "vessel_anomaly"
    CITIZEN_REPORT = "citizen_report"


class ObservationBase(BaseModel):
    """
    Unified base observation model representing normalized ocean telemetry.
    """
    source: str = Field(..., description="Name or identifier of observation telemetry source")
    observation_type: ObservationType = Field(..., description="Category of ocean observation")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="WGS-84 Latitude (-90 to 90)")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="WGS-84 Longitude (-180 to 180)")
    timestamp: Optional[str] = Field(None, description="ISO-8601 observation timestamp")
    data: Dict[str, Any] = Field(default_factory=dict, description="Raw or processed observation metrics payload")
