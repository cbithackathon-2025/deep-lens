import pytest
import math
from packages.geospatial.calculations import (
    validate_coordinates,
    haversine_distance_km,
    initial_bearing,
    is_point_in_bbox
)

def test_validate_coordinates():
    assert validate_coordinates(0.0, 0.0) is True
    assert validate_coordinates(-90.0, 180.0) is True
    assert validate_coordinates(90.0, -180.0) is True
    assert validate_coordinates(90.1, 0.0) is False
    assert validate_coordinates(0.0, 180.1) is False
    assert validate_coordinates(float("nan"), 0.0) is False
    assert validate_coordinates("invalid", 10.0) is False

def test_haversine_distance_known_points():
    # Equator half quadrant (0,0) to (0,90) is ~10,007.5 km (pi/2 * 6371)
    dist = haversine_distance_km(0.0, 0.0, 0.0, 90.0)
    expected = (math.pi / 2.0) * 6371.0
    assert abs(dist - expected) < 1.0

    # Same point distance is 0
    assert haversine_distance_km(27.5, -91.2, 27.5, -91.2) == 0.0

def test_haversine_distance_invalid_coordinates():
    with pytest.raises(ValueError):
        haversine_distance_km(100.0, 0.0, 0.0, 0.0)

def test_initial_bearing_cardinal_directions():
    # Due North: (0, 0) to (10, 0) -> 0 degrees
    assert initial_bearing(0.0, 0.0, 10.0, 0.0) == 0.0
    # Due East along equator: (0, 0) to (0, 10) -> 90 degrees
    assert initial_bearing(0.0, 0.0, 0.0, 10.0) == 90.0
    # Due South: (10, 0) to (0, 0) -> 180 degrees
    assert initial_bearing(10.0, 0.0, 0.0, 0.0) == 180.0
    # Due West along equator: (0, 10) to (0, 0) -> 270 degrees
    assert initial_bearing(0.0, 10.0, 0.0, 0.0) == 270.0

def test_is_point_in_bbox():
    assert is_point_in_bbox(27.5, -91.2, -100.0, 20.0, -80.0, 35.0) is True
    assert is_point_in_bbox(45.0, 0.0, -100.0, 20.0, -80.0, 35.0) is False
