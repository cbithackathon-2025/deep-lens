from modules.maritime.mpa_detector import check_mpa_incursion, MPAZone

def test_vessel_inside_galapagos_mpa_normal_speed():
    # Coordinates inside Galapagos Marine Reserve (-0.85, -89.40) at 6.0 knots
    result = check_mpa_incursion(latitude=-0.85, longitude=-89.40, speed_knots=6.0)
    assert result is not None
    assert result["incursion_detected"] is True
    assert result["mpa_id"] == "MPA-GALAPAGOS"
    assert result["violation_type"] == "UNAUTHORIZED_ENTRY"
    assert result["severity"] == "medium"

def test_vessel_inside_galapagos_mpa_speeding():
    # Coordinates inside Galapagos Marine Reserve (-0.85, -89.40) at 16.5 knots (limit 10.0)
    result = check_mpa_incursion(latitude=-0.85, longitude=-89.40, speed_knots=16.5)
    assert result is not None
    assert result["violation_type"] == "SPEEDING_IN_RESTRICTED_ZONE"
    assert result["severity"] == "high"

def test_vessel_in_open_international_waters():
    # Mid-Atlantic open waters (0.0, -30.0)
    result = check_mpa_incursion(latitude=0.0, longitude=-30.0, speed_knots=14.0)
    assert result is None
