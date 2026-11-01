import pytest
from pydantic import ValidationError
from packages.schemas.citizen_report import (
    CitizenReportCreate,
    CitizenThreatCategory,
    ReportConfidenceLevel
)

def test_valid_citizen_report():
    report = CitizenReportCreate(
        observer_alias="Coastal Ranger Mike",
        category=CitizenThreatCategory.OIL_SLICK,
        latitude=27.55,
        longitude=-91.15,
        description="Visible sheen and diesel odor observed near harbor mouth.",
        confidence=ReportConfidenceLevel.HIGH
    )
    assert report.observer_alias == "Coastal Ranger Mike"
    assert report.category == CitizenThreatCategory.OIL_SLICK
    assert report.latitude == 27.55
    assert report.confidence == ReportConfidenceLevel.HIGH

def test_invalid_coordinates():
    with pytest.raises(ValidationError):
        CitizenReportCreate(
            category=CitizenThreatCategory.MARINE_DEBRIS,
            latitude=110.0,  # Invalid
            longitude=0.0,
            description="Discarded ghost nets floating near shoreline."
        )

def test_short_description_rejection():
    with pytest.raises(ValidationError):
        CitizenReportCreate(
            category=CitizenThreatCategory.OTHER,
            latitude=10.0,
            longitude=20.0,
            description="too short"  # < 10 chars
        )

def test_default_alias_and_confidence():
    report = CitizenReportCreate(
        category=CitizenThreatCategory.ALGAL_BLOOM,
        latitude=25.0,
        longitude=-80.0,
        description="Red tide coloration in shallow coastal lagoon."
    )
    assert report.observer_alias == "Anonymous Marine Observer"
    assert report.confidence == ReportConfidenceLevel.MEDIUM
