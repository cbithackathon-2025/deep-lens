from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

OCEAN_BASIN_CENTROIDS: Dict[str, Dict[str, Any]] = {
    "gulf_of_mexico": {
        "name": "Gulf of Mexico",
        "latitude": 27.50,
        "longitude": -91.20,
        "default_threat": "oil_slick",
        "typical_sst": 28.5
    },
    "galapagos": {
        "name": "Galapagos Marine Reserve",
        "latitude": -0.85,
        "longitude": -89.40,
        "default_threat": "vessel_blackout",
        "typical_sst": 29.8
    },
    "great_barrier_reef": {
        "name": "Great Barrier Reef",
        "latitude": -16.25,
        "longitude": 145.78,
        "default_threat": "coral_bleaching",
        "typical_sst": 30.2
    },
    "malacca_strait": {
        "name": "Strait of Malacca",
        "latitude": 3.00,
        "longitude": 101.00,
        "default_threat": "vessel_blackout",
        "typical_sst": 29.1
    },
    "north_sea": {
        "name": "North Sea Offshore",
        "latitude": 56.00,
        "longitude": 3.50,
        "default_threat": "oil_slick",
        "typical_sst": 14.2
    }
}

def generate_basin_seed_observations(
    basin_key: Optional[str] = None,
    records_per_basin: int = 2
) -> List[Dict[str, Any]]:
    """
    Generates realistic multi-basin simulated telemetry seed records
    for offline development, unit tests, and demo mode.
    """
    selected_basins = (
        {basin_key: OCEAN_BASIN_CENTROIDS[basin_key]}
        if basin_key and basin_key in OCEAN_BASIN_CENTROIDS
        else OCEAN_BASIN_CENTROIDS
    )

    records = []
    now_iso = datetime.now(timezone.utc).isoformat()

    for key, basin in selected_basins.items():
        for i in range(records_per_basin):
            lat_jitter = (i * 0.05) - 0.025
            lon_jitter = (i * 0.05) - 0.025
            rec_id = f"SEED-{key[:3].upper()}-{100 + i}"

            records.append({
                "id": rec_id,
                "basin": basin["name"],
                "basin_key": key,
                "latitude": round(basin["latitude"] + lat_jitter, 4),
                "longitude": round(basin["longitude"] + lon_jitter, 4),
                "category": basin["default_threat"],
                "sea_surface_temp_celsius": basin["typical_sst"],
                "source": "Deep Lens Demo Telemetry Generator",
                "timestamp": now_iso
            })

    return records
