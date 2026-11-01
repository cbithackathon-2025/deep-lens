import pytest
from fastapi.testclient import TestClient

from services.api.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("dhw", "expected_alert"),
    [
        (12.0, 3),
        (15.99, 3),
        (16.0, 4),
        (20.0, 4),
    ],
)
def test_post_coral_observation_returns_dhw_classification(dhw, expected_alert):
    response = client.post(
        "/api/v1/coral/observations",
        json={
            "latitude": -16.25,
            "longitude": 145.78,
            "dhw_degree_weeks": dhw,
        },
    )

    assert response.status_code == 200
    observation = response.json()
    assert observation["source"] == "NOAA Coral Reef Watch"
    assert observation["observation_type"] == "thermal_stress"
    assert observation["latitude"] == -16.25
    assert observation["longitude"] == 145.78
    assert observation["data"]["dhw_degree_weeks"] == dhw
    assert observation["data"]["alert_level"] == expected_alert


def test_post_coral_observation_rejects_invalid_coordinates():
    response = client.post(
        "/api/v1/coral/observations",
        json={
            "latitude": 91,
            "longitude": 145.78,
            "dhw_degree_weeks": 16.0,
        },
    )

    assert response.status_code == 422