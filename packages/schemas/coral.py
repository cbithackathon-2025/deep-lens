"""Schemas for NOAA Coral Reef Watch thermal-stress observations."""
from enum import IntEnum

from pydantic import BaseModel, Field, model_validator


class CoralAlertLevel(IntEnum):
    NO_ALERT = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4


class CoralThermalStress(BaseModel):
    dhw_degree_weeks: float = Field(
        ge=0,
        allow_inf_nan=False,
        description="Degree Heating Weeks (DHW) thermal-stress index",
    )
    alert_level: CoralAlertLevel = Field(
        default=CoralAlertLevel.NO_ALERT,
        description="NOAA Coral Reef Watch alert level",
    )

    @model_validator(mode="after")
    def classify_alert_level(self) -> "CoralThermalStress":
        if self.dhw_degree_weeks >= 16.0:
            self.alert_level = CoralAlertLevel.LEVEL_4
        elif self.dhw_degree_weeks >= 12.0:
            self.alert_level = CoralAlertLevel.LEVEL_3
        elif self.dhw_degree_weeks >= 8.0:
            self.alert_level = CoralAlertLevel.LEVEL_2
        elif self.dhw_degree_weeks >= 4.0:
            self.alert_level = CoralAlertLevel.LEVEL_1
        else:
            self.alert_level = CoralAlertLevel.NO_ALERT
        return self


class CoralObservationRequest(CoralThermalStress):
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)
    station_id: str | None = None
    sst_celsius: float | None = None
    timestamp: str | None = None
