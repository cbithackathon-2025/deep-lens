"""Base data ingestion adapter interface."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from packages.schemas.observation import ObservationBase


class BaseDataIngestionAdapter(ABC):
    """
    Abstract base interface for all external ocean data ingestion adapters.
    Provides standard contract for raw telemetry acquisition and standardized normalization.
    """

    @abstractmethod
    def fetch_raw_data(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch raw observational telemetry records from external APIs or local sources.
        """
        pass

    @abstractmethod
    def normalize_record(self, raw_record: Dict[str, Any]) -> Any:
        """
        Normalize an external raw telemetry dictionary into the unified ObservationBase schema.
        """
        pass
