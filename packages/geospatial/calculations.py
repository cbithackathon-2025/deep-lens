import math
from typing import Tuple

EARTH_RADIUS_KM = 6371.0

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validates that latitude is within [-90.0, 90.0] and longitude is within [-180.0, 180.0].
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return False
    if math.isnan(latitude) or math.isnan(longitude):
        return False
    return -90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates great-circle distance between two geographic points in kilometers
    using the Haversine formula.
    """
    if not (validate_coordinates(lat1, lon1) and validate_coordinates(lat2, lon2)):
        raise ValueError("Invalid coordinate provided to haversine_distance_km")

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(EARTH_RADIUS_KM * c, 4)

def initial_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates initial forward azimuth (compass bearing) in degrees from point 1 to point 2 [0, 360).
    """
    if not (validate_coordinates(lat1, lon1) and validate_coordinates(lat2, lon2)):
        raise ValueError("Invalid coordinate provided to initial_bearing")

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)

    y = math.sin(delta_lambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    theta = math.atan2(y, x)

    bearing = (math.degrees(theta) + 360.0) % 360.0
    return round(bearing, 2)

def is_point_in_bbox(
    lat: float,
    lon: float,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float
) -> bool:
    """
    Checks if a (lat, lon) point lies within the bounding box [min_lon, min_lat, max_lon, max_lat].
    """
    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon
