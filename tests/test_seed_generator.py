from packages.ocean_data.seed_generator import (
    generate_basin_seed_observations,
    OCEAN_BASIN_CENTROIDS
)

def test_generate_all_basins_seed():
    records = generate_basin_seed_observations(records_per_basin=2)
    expected_total = len(OCEAN_BASIN_CENTROIDS) * 2
    assert len(records) == expected_total

    # Verify key attributes on each generated record
    for rec in records:
        assert "id" in rec
        assert "basin" in rec
        assert "latitude" in rec
        assert "longitude" in rec
        assert "category" in rec
        assert "timestamp" in rec

def test_generate_single_basin_seed():
    records = generate_basin_seed_observations(basin_key="galapagos", records_per_basin=3)
    assert len(records) == 3
    assert all(r["basin_key"] == "galapagos" for r in records)
    assert all(r["category"] == "vessel_blackout" for r in records)

def test_generate_unknown_basin_fallback():
    # Unknown basin falls back to all basins
    records = generate_basin_seed_observations(basin_key="atlantis", records_per_basin=1)
    assert len(records) == len(OCEAN_BASIN_CENTROIDS)
