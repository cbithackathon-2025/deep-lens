from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseDataIngestionAdapter(ABC):
    """
    Abstract base class for all ocean data ingestion adapters.
    Provides standard contract for raw telemetry acquisition and standardized normalization.
    """

    @abstractmethod
    def fetch_raw_data(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetches or simulates raw payload records from external sources,
        satellite data streams, or sensor telemetry APIs.
        """
        pass

    @abstractmethod
    def normalize_record(self, raw_record: Dict[str, Any]) -> Any:
        """
        Normalizes a raw telemetry dictionary into a unified observation schema.
        """
        pass
