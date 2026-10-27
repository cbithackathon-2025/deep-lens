from modules.drift_analysis.lagrangian_drift import simulate_particle_drift

def test_stationary_current_and_wind():
    trajectory = simulate_particle_drift(
        start_lat=0.0,
        start_lon=0.0,
        current_u_mps=0.0,
        current_v_mps=0.0,
        total_hours=5.0
    )
    assert len(trajectory) == 6
    assert trajectory[-1]["latitude"] == 0.0
    assert trajectory[-1]["longitude"] == 0.0
    assert trajectory[-1]["cumulative_distance_km"] == 0.0

def test_northward_advection():
    # 1.0 m/s northward current for 10 hours -> 36,000 meters ~ 36 km
    trajectory = simulate_particle_drift(
        start_lat=10.0,
        start_lon=-80.0,
        current_u_mps=0.0,
        current_v_mps=1.0,
        total_hours=10.0
    )
    assert len(trajectory) == 11
    assert trajectory[-1]["latitude"] > 10.0
    assert trajectory[-1]["longitude"] == -80.0
    assert 35.0 < trajectory[-1]["cumulative_distance_km"] < 37.0

def test_wind_leeway_contribution():
    # Only wind leeway pushing eastward
    traj_no_wind = simulate_particle_drift(0.0, 0.0, 0.5, 0.0, wind_u_mps=0.0, total_hours=5.0)
    traj_with_wind = simulate_particle_drift(0.0, 0.0, 0.5, 0.0, wind_u_mps=10.0, total_hours=5.0)

    assert traj_with_wind[-1]["cumulative_distance_km"] > traj_no_wind[-1]["cumulative_distance_km"]
