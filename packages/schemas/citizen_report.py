from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CitizenThreatCategory(str, Enum):
    OIL_SLICK = "oil_slick"
    MARINE_DEBRIS = "marine_debris"
    VESSEL_BLACKOUT = "vessel_blackout"
    CORAL_BLEACHING = "coral_bleaching"
    ALGAL_BLOOM = "algal_bloom"
    OTHER = "other"

class ReportConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CitizenReportCreate(BaseModel):
    """
    Validation schema for community coastal field observations and citizen science reports.
    """
    observer_alias: Optional[str] = Field(default="Anonymous Marine Observer", max_length=100)
    category: CitizenThreatCategory
    latitude: float
    longitude: float
    description: str = Field(min_length=10, max_length=2000, description="Detailed observation description")
    observed_at: Optional[str] = None
    photo_url: Optional[str] = Field(default=None, max_length=500)
    confidence: ReportConfidenceLevel = ReportConfidenceLevel.MEDIUM

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not (-90.0 <= v <= 90.0):
            raise ValueError(f"Latitude must be between -90 and 90 degrees, got {v}")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not (-180.0 <= v <= 180.0):
            raise ValueError(f"Longitude must be between -180 and 180 degrees, got {v}")
        return v

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 10:
            raise ValueError("Observation description must contain at least 10 non-whitespace characters")
        return clean
