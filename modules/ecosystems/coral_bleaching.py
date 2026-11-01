from typing import Dict, Any, List

def classify_thermal_stress(
    sst_anomaly_celsius: float,
    dhw_degree_weeks: float
) -> Dict[str, Any]:
    """
    Classifies Sea Surface Temperature (SST) anomaly and Degree Heating Weeks (DHW)
    into standardized NOAA Coral Reef Watch (CRW) Alert Levels.
    """
    if sst_anomaly_celsius <= 0.0:
        return {
            "alert_level": 0,
            "status": "NO_STRESS",
            "risk": "none",
            "description": "No thermal stress detected. Corals within safe thermal envelope.",
            "sst_anomaly": sst_anomaly_celsius,
            "dhw": dhw_degree_weeks
        }
    elif sst_anomaly_celsius < 1.0:
        return {
            "alert_level": 1,
            "status": "BLEACHING_WATCH",
            "risk": "low",
            "description": "HotSpot > 0; low level thermal stress developing.",
            "sst_anomaly": sst_anomaly_celsius,
            "dhw": dhw_degree_weeks
        }
    elif dhw_degree_weeks < 4.0:
        return {
            "alert_level": 2,
            "status": "BLEACHING_WARNING",
            "risk": "medium",
            "description": "HotSpot >= 1; potential bleaching stress accumulating.",
            "sst_anomaly": sst_anomaly_celsius,
            "dhw": dhw_degree_weeks
        }
    elif dhw_degree_weeks < 8.0:
        return {
            "alert_level": 3,
            "status": "ALERT_LEVEL_1",
            "risk": "high",
            "description": "Significant coral bleaching likely across susceptible taxa.",
            "sst_anomaly": sst_anomaly_celsius,
            "dhw": dhw_degree_weeks
        }
    else:
        return {
            "alert_level": 4,
            "status": "ALERT_LEVEL_2",
            "risk": "critical",
            "description": "Severe multi-species bleaching and ecologically significant mortality expected.",
            "sst_anomaly": sst_anomaly_celsius,
            "dhw": dhw_degree_weeks
        }

def calculate_degree_heating_weeks(daily_hotspots_12_weeks: List[float]) -> float:
    """
    Calculates Degree Heating Weeks (DHW) by accumulating positive thermal anomalies
    where HotSpot >= 1.0 deg C over the past 12-week (84-day) window.
    DHW = Sum(HotSpot / 7) for daily measurements.
    """
    accumulated_dhw = sum(h / 7.0 for h in daily_hotspots_12_weeks if h >= 1.0)
    return round(accumulated_dhw, 2)
