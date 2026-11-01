from modules.maritime.ais_blackout_detector import detect_ais_blackout

def test_no_blackout_continuous_pings():
    # Pings every 1 hour (threshold is 4.0h)
    pings = [
        {"mmsi": "228001000", "timestamp": "2026-10-27T10:00:00Z", "latitude": 20.0, "longitude": -90.0},
        {"mmsi": "228001000", "timestamp": "2026-10-27T11:00:00Z", "latitude": 20.1, "longitude": -90.1},
        {"mmsi": "228001000", "timestamp": "2026-10-27T12:00:00Z", "latitude": 20.2, "longitude": -90.2},
    ]
    blackouts = detect_ais_blackout(pings, max_gap_hours=4.0)
    assert len(blackouts) == 0

def test_detect_blackout_medium_severity():
    # 6.5 hour gap
    pings = [
        {"mmsi": "228001000", "timestamp": "2026-10-27T00:00:00Z", "latitude": 20.0, "longitude": -90.0},
        {"mmsi": "228001000", "timestamp": "2026-10-27T06:30:00Z", "latitude": 21.0, "longitude": -90.5},
    ]
    blackouts = detect_ais_blackout(pings, max_gap_hours=4.0)
    assert len(blackouts) == 1
    assert blackouts[0]["gap_duration_hours"] == 6.5
    assert blackouts[0]["severity"] == "medium"
    assert blackouts[0]["suspicious"] is True

def test_detect_blackout_high_severity():
    # 18 hour blackout
    pings = [
        {"mmsi": "228001000", "timestamp": "2026-10-27T00:00:00Z", "latitude": 20.0, "longitude": -90.0},
        {"mmsi": "228001000", "timestamp": "2026-10-27T18:00:00Z", "latitude": 22.0, "longitude": -91.0},
    ]
    blackouts = detect_ais_blackout(pings, max_gap_hours=4.0)
    assert len(blackouts) == 1
    assert blackouts[0]["gap_duration_hours"] == 18.0
    assert blackouts[0]["severity"] == "high"

def test_insufficient_pings():
    assert detect_ais_blackout([]) == []
    assert detect_ais_blackout([{"mmsi": "1", "timestamp": "2026-10-27T00:00:00Z"}]) == []
