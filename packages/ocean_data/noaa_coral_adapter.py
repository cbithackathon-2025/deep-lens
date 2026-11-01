from datetime import datetime, timezone
from typing import Any, Dict, List
from packages.ocean_data.base_adapter import BaseDataIngestionAdapter
from packages.schemas.coral import CoralThermalStress
from packages.schemas.observation import ObservationBase, ObservationType

class NOAACoralBleachingAdapter(BaseDataIngestionAdapter):
    """
    Ingestion adapter for NOAA Coral Reef Watch (CRW) Sea Surface Temperature (SST)
    and Degree Heating Weeks (DHW) thermal stress observations.
    """

    def fetch_raw_data(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Simulates or fetches raw NOAA CRW thermal stress telemetry.
        """
        return [
            {
                "station_id": "CRW_GALAPAGOS_01",
                "latitude": -0.74,
                "longitude": -90.31,
                "sst_celsius": 29.8,
                "dhw_degree_weeks": 8.5,
                "alert_level": 2,
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            {
                "station_id": "CRW_GBR_NORTH_02",
                "latitude": -16.25,
                "longitude": 145.78,
                "sst_celsius": 30.2,
                "dhw_degree_weeks": 12.1,
                "alert_level": 3,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ]

    def normalize_record(self, raw_record: Dict[str, Any]) -> ObservationBase:
        """
        Normalizes raw NOAA CRW telemetry to the unified ObservationBase schema.
        """
        obs_type = getattr(ObservationType, "THERMAL_STRESS", ObservationType.ENVIRONMENTAL)
        reported_alert_level = raw_record.get("alert_level")
        thermal_stress = CoralThermalStress(
            dhw_degree_weeks=raw_record["dhw_degree_weeks"],
            alert_level=(
                reported_alert_level
                if reported_alert_level is not None
                else 0
            ),
        )
        
        return ObservationBase(
            source="NOAA Coral Reef Watch",
            observation_type=obs_type,
            latitude=raw_record["latitude"],
            longitude=raw_record["longitude"],
            timestamp=raw_record.get("timestamp"),
            data={
                "station_id": raw_record.get("station_id"),
                "sst_celsius": raw_record.get("sst_celsius"),
                "dhw_degree_weeks": thermal_stress.dhw_degree_weeks,
                "alert_level": thermal_stress.alert_level.value
            }
        )
