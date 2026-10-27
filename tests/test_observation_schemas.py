import pytest
from pydantic import ValidationError
from packages.schemas.observation import ObservationBase, ObservationType

def test_observation_base_valid_instantiation():
    obs = ObservationBase(
        source="NOAA Coral Reef Watch",
        observation_type=ObservationType.THERMAL_STRESS,
        latitude=-0.74,
        longitude=-90.31,
        timestamp="2026-10-27T12:00:00Z",
        data={"sst_celsius": 29.8, "dhw_degree_weeks": 8.5}
    )
    assert obs.source == "NOAA Coral Reef Watch"
    assert obs.observation_type == ObservationType.THERMAL_STRESS
    assert obs.latitude == -0.74
    assert obs.longitude == -90.31
    assert obs.data["sst_celsius"] == 29.8

def test_observation_base_invalid_latitude():
    with pytest.raises(ValidationError):
        ObservationBase(
            source="Test Station",
            observation_type=ObservationType.ENVIRONMENTAL,
            latitude=95.0,  # Invalid: > 90
            longitude=0.0
        )

def test_observation_base_invalid_longitude():
    with pytest.raises(ValidationError):
        ObservationBase(
            source="Test Station",
            observation_type=ObservationType.ENVIRONMENTAL,
            latitude=0.0,
            longitude=-195.0  # Invalid: < -180
        )

def test_observation_type_enum_values():
    assert ObservationType.THERMAL_STRESS.value == "thermal_stress"
    assert ObservationType.ENVIRONMENTAL.value == "environmental"
    assert ObservationType.POLLUTION.value == "pollution"
