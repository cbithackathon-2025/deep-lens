from fastapi import APIRouter

from packages.ocean_data.noaa_coral_adapter import NOAACoralBleachingAdapter
from packages.schemas.coral import CoralObservationRequest
from packages.schemas.observation import ObservationBase

router = APIRouter(prefix="/api/v1/coral", tags=["coral"])


@router.post("/observations", response_model=ObservationBase)
def normalize_coral_observation(
    observation: CoralObservationRequest,
) -> ObservationBase:
    """Validate and normalize a NOAA coral thermal-stress observation."""
    adapter = NOAACoralBleachingAdapter()
    return adapter.normalize_record(observation.model_dump(mode="json"))