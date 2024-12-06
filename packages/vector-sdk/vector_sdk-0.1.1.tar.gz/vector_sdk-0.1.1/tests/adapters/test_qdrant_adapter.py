import unittest
from unittest.mock import MagicMock

from src.vector_sdk.adapters.qdrant_adapter import QdrantAdapter
from src.vector_sdk.utils.telemetry import Telemetry


class TestQdrantAdapter(unittest.TestCase):
    def setUp(self):
        self.telemetry = MagicMock(spec=Telemetry)
        self.adapter = QdrantAdapter(telemetry=self.telemetry)
        self.adapter.client = MagicMock()
        self.adapter._is_connected = True

    def test_list_collections(self):
        # Mock the client response
        mock_collections = MagicMock()
        mock_collections.collections = [
            MagicMock(name="collection1"),
            MagicMock(name="collection2"),
        ]
        self.adapter.client.get_collections.return_value = mock_collections

        collections = self.adapter.list_collections()
        self.assertEqual(collections, ["collection1", "collection2"])
        self.adapter.client.get_collections.assert_called_once()
        self.telemetry.track_operation.assert_called_with(
            "list_collections", {"collection_count": 2}
        )

    # Add more tests for other methods...


if __name__ == "__main__":
    unittest.main()
