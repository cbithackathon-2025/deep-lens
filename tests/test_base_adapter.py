import pytest
from typing import List, Dict, Any
from packages.ocean_data.base_adapter import BaseDataIngestionAdapter

class DummyAdapter(BaseDataIngestionAdapter):
    def fetch_raw_data(self, **kwargs) -> List[Dict[str, Any]]:
        return [{"sample_id": 1, "value": 42.0}]

    def normalize_record(self, raw_record: Dict[str, Any]) -> Any:
        return {"id": raw_record["sample_id"], "normalized": True}

def test_base_adapter_abstract_instantiation():
    # Attempting to instantiate BaseDataIngestionAdapter directly must fail
    with pytest.raises(TypeError):
        BaseDataIngestionAdapter()

def test_concrete_adapter_implementation():
    adapter = DummyAdapter()
    data = adapter.fetch_raw_data()
    assert len(data) == 1
    assert data[0]["sample_id"] == 1

    record = adapter.normalize_record(data[0])
    assert record["id"] == 1
    assert record["normalized"] is True
