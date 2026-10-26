from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class ObservationType(str, Enum):
    ENVIRONMENTAL = "environmental"
    THERMAL_STRESS = "thermal_stress"
    ACOUSTIC = "acoustic"
    SATELLITE = "satellite"
    OIL_SLICK = "oil_slick"

class ObservationBase(BaseModel):
    source: str
    observation_type: ObservationType
    latitude: float
    longitude: float
    timestamp: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
