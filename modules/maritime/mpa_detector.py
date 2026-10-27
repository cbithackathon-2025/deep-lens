from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass(frozen=True)
class MPAZone:
    id: str
    name: str
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float
    max_permitted_speed_knots: float

PROTECTED_AREAS: List[MPAZone] = [
    MPAZone(
        id="MPA-GALAPAGOS",
        name="Galapagos Marine Reserve",
        min_lon=-92.5,
        min_lat=-2.0,
        max_lon=-89.0,
        max_lat=2.0,
        max_permitted_speed_knots=10.0
    ),
    MPAZone(
        id="MPA-GBR",
        name="Great Barrier Reef Marine Park",
        min_lon=142.5,
        min_lat=-24.5,
        max_lon=154.0,
        max_lat=-10.5,
        max_permitted_speed_knots=12.0
    ),
    MPAZone(
        id="MPA-PMNM",
        name="Papahānaumokuākea Marine National Monument",
        min_lon=-180.0,
        min_lat=22.0,
        max_lon=-160.0,
        max_lat=32.0,
        max_permitted_speed_knots=8.0
    )
]

def check_mpa_incursion(
    latitude: float,
    longitude: float,
    speed_knots: float = 0.0,
    zones: Optional[List[MPAZone]] = None
) -> Optional[Dict[str, Any]]:
    """
    Evaluates vessel coordinates and speed against known Marine Protected Areas.
    Returns incursion details if vessel is inside an MPA, or None if in international waters.
    """
    active_zones = zones if zones is not None else PROTECTED_AREAS

    for zone in active_zones:
        if zone.min_lat <= latitude <= zone.max_lat and zone.min_lon <= longitude <= zone.max_lon:
            is_speeding = speed_knots > zone.max_permitted_speed_knots
            return {
                "incursion_detected": True,
                "mpa_id": zone.id,
                "mpa_name": zone.name,
                "latitude": latitude,
                "longitude": longitude,
                "speed_knots": speed_knots,
                "speed_limit_knots": zone.max_permitted_speed_knots,
                "violation_type": "SPEEDING_IN_RESTRICTED_ZONE" if is_speeding else "UNAUTHORIZED_ENTRY",
                "severity": "high" if is_speeding else "medium"
            }

    return None
