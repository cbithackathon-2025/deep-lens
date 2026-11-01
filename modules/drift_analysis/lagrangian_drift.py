import math
from typing import List, Dict, Any

METERS_PER_DEGREE_LAT = 111139.0

def simulate_particle_drift(
    start_lat: float,
    start_lon: float,
    current_u_mps: float,
    current_v_mps: float,
    wind_u_mps: float = 0.0,
    wind_v_mps: float = 0.0,
    wind_leeway_factor: float = 0.03,
    time_step_hours: float = 1.0,
    total_hours: float = 24.0
) -> List[Dict[str, Any]]:
    """
    Simulates 2D forward Lagrangian particle advection under surface currents
    and an empirical 3% wind leeway velocity factor.
    Returns simulated trajectory waypoints over time.
    """
    trajectory = []
    curr_lat = start_lat
    curr_lon = start_lon
    total_dist_meters = 0.0

    # Net advection velocity (m/s)
    v_x = current_u_mps + (wind_leeway_factor * wind_u_mps)
    v_y = current_v_mps + (wind_leeway_factor * wind_v_mps)

    dt_seconds = time_step_hours * 3600.0
    steps = int(total_hours / time_step_hours)

    trajectory.append({
        "hour": 0.0,
        "latitude": round(curr_lat, 5),
        "longitude": round(curr_lon, 5),
        "cumulative_distance_km": 0.0
    })

    for step in range(1, steps + 1):
        dx = v_x * dt_seconds
        dy = v_y * dt_seconds
        step_dist = math.sqrt(dx ** 2 + dy ** 2)
        total_dist_meters += step_dist

        d_lat = dy / METERS_PER_DEGREE_LAT
        cos_lat = math.cos(math.radians(curr_lat))
        # Prevent division by zero near poles
        d_lon = dx / (METERS_PER_DEGREE_LAT * (cos_lat if abs(cos_lat) > 1e-6 else 1e-6))

        curr_lat += d_lat
        curr_lon += d_lon

        trajectory.append({
            "hour": round(step * time_step_hours, 1),
            "latitude": round(curr_lat, 5),
            "longitude": round(curr_lon, 5),
            "cumulative_distance_km": round(total_dist_meters / 1000.0, 3)
        })

    return trajectory
