from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

class ObservationType(str, Enum):
    ENVIRONMENTAL = "environmental"
    THERMAL_STRESS = "thermal_stress"
    ACOUSTIC = "acoustic"
    SATELLITE = "satellite"
    POLLUTION = "pollution"
    VESSEL_TRACKING = "vessel_tracking"

class ObservationBase(BaseModel):
    source: str
    observation_type: ObservationType
    latitude: float
    longitude: float
    timestamp: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not (-90.0 <= v <= 90.0):
            raise ValueError(f"Latitude must be between -90 and 90, got {v}")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not (-180.0 <= v <= 180.0):
            raise ValueError(f"Longitude must be between -180 and 180, got {v}")
        return v
