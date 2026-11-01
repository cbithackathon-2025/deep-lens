from datetime import datetime
from typing import List, Dict, Any

def parse_iso_timestamp(ts: str) -> datetime:
    """
    Parses ISO 8601 timestamp string into datetime object.
    Supports 'Z' suffix or standard ISO offset.
    """
    clean_ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(clean_ts)

def detect_ais_blackout(
    pings: List[Dict[str, Any]],
    max_gap_hours: float = 4.0
) -> List[Dict[str, Any]]:
    """
    Analyzes chronological AIS telemetry for a vessel to detect suspicious transponder
    tracking gaps exceeding the threshold hours (default 4.0h).
    """
    if len(pings) < 2:
        return []

    # Sort pings chronologically
    sorted_pings = sorted(pings, key=lambda p: parse_iso_timestamp(p["timestamp"]))
    blackouts = []

    for i in range(1, len(sorted_pings)):
        prev_p = sorted_pings[i - 1]
        curr_p = sorted_pings[i]

        t_prev = parse_iso_timestamp(prev_p["timestamp"])
        t_curr = parse_iso_timestamp(curr_p["timestamp"])

        delta_hours = (t_curr - t_prev).total_seconds() / 3600.0

        if delta_hours > max_gap_hours:
            severity = "high" if delta_hours >= 12.0 else "medium"
            blackouts.append({
                "mmsi": curr_p.get("mmsi") or prev_p.get("mmsi"),
                "last_known_ping": {
                    "timestamp": prev_p["timestamp"],
                    "latitude": prev_p.get("latitude"),
                    "longitude": prev_p.get("longitude")
                },
                "reacquired_ping": {
                    "timestamp": curr_p["timestamp"],
                    "latitude": curr_p.get("latitude"),
                    "longitude": curr_p.get("longitude")
                },
                "gap_duration_hours": round(delta_hours, 2),
                "threshold_hours": max_gap_hours,
                "severity": severity,
                "suspicious": True
            })

    return blackouts
