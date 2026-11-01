import pytest
from packages.ocean_data.noaa_coral_adapter import NOAACoralBleachingAdapter

def test_noaa_coral_adapter_fetch_and_normalize():
    adapter = NOAACoralBleachingAdapter()
    raw_records = adapter.fetch_raw_data()
    assert len(raw_records) > 0

    first_record = raw_records[0]
    normalized = adapter.normalize_record(first_record)

    assert normalized.latitude == first_record["latitude"]
    assert normalized.longitude == first_record["longitude"]
    assert normalized.source == "NOAA Coral Reef Watch"
    assert "dhw_degree_weeks" in normalized.data
    assert normalized.data["dhw_degree_weeks"] == first_record["dhw_degree_weeks"]


@pytest.mark.parametrize(
    ("dhw", "expected_alert"),
    [
        (11.99, 2),
        (12.0, 3),
        (15.99, 3),
        (16.0, 4),
        (20.0, 4),
    ],
)
def test_noaa_coral_adapter_classifies_dhw_alert_levels(dhw, expected_alert):
    adapter = NOAACoralBleachingAdapter()
    normalized = adapter.normalize_record(
        {
            "latitude": -16.25,
            "longitude": 145.78,
            "dhw_degree_weeks": dhw,
            "alert_level": expected_alert,
        }
    )

    assert normalized.data["dhw_degree_weeks"] == dhw
    assert normalized.data["alert_level"] == expected_alert


def test_noaa_coral_adapter_rejects_unsupported_reported_alert_level():
    adapter = NOAACoralBleachingAdapter()
    raw_record = {
        "latitude": -16.25,
        "longitude": 145.78,
        "dhw_degree_weeks": 16.0,
        "alert_level": 5,
    }

    with pytest.raises(ValueError):
        adapter.normalize_record(raw_record)


def test_noaa_coral_adapter_classifies_from_dhw_when_reported_level_differs():
    adapter = NOAACoralBleachingAdapter()
    normalized = adapter.normalize_record(
        {
            "latitude": -16.25,
            "longitude": 145.78,
            "dhw_degree_weeks": 15.99,
            "alert_level": 4,
        }
    )

    assert normalized.data["alert_level"] == 3
