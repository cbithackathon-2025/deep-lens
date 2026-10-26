from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseDataIngestionAdapter(ABC):
    """
    Abstract base class for all ocean data ingestion adapters.
    """

    @abstractmethod
    def fetch_raw_data(self, **kwargs) -> List[Dict[str, Any]]:
        """Fetch raw payload records from external sources or telemetry streams."""
        pass

    @abstractmethod
    def normalize_record(self, raw_record: Dict[str, Any]) -> Any:
        """Normalize raw payload dictionary into standardized Observation schema."""
        pass
