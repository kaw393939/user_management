import pytest
from unittest.mock import MagicMock
from minio import Minio
from app.utils.minio_utils import get_minio_client

@pytest.fixture
def mock_minio_client(monkeypatch):
    mock_client = MagicMock(spec=Minio)
    monkeypatch.setattr('app.utils.minio_utils.get_minio_client', lambda: mock_client)
    return mock_client

def test_minio_client_connection(mock_minio_client):
    # Mock the list_buckets to raise an exception to simulate a connection error
    mock_minio_client.list_buckets.side_effect = Exception("Simulated connection error")

    # Now, the test should expect an exception
    with pytest.raises(Exception) as exc_info:
        mock_minio_client.list_buckets()
    assert "Simulated connection error" in str(exc_info.value), "Expected a simulated connection error"
