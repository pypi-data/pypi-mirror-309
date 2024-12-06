import unittest

from src.vector_sdk.adapters.qdrant_adapter import QdrantAdapter
from src.vector_sdk.utils.telemetry import Telemetry


class TestQdrantAdapterIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.telemetry = Telemetry()
        cls.adapter = QdrantAdapter(telemetry=cls.telemetry)
        config = {"host": "localhost", "port": 6333, "memory_mode": False}
        cls.adapter.connect(config)

    def test_full_crud_operations(self):
        collection_name = "integration_test_collection"

        # Create Collection
        self.adapter.create_collection(
            name=collection_name, vector_size=4, distance_metric="DOT"
        )

        # List Collections
        collections = self.adapter.list_collections()
        self.assertIn(collection_name, collections)

        # Upsert Vectors
        vectors = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]]
        ids = ["vec1", "vec2"]
        metadata = [{"info": "first"}, {"info": "second"}]
        upsert_result = self.adapter.upsert_vectors(
            collection_name=collection_name, vectors=vectors, ids=ids, metadata=metadata
        )
        self.assertEqual(upsert_result["inserted_count"], 2)

        # Search Vectors
        search_result = self.adapter.search_vectors(
            collection_name=collection_name, query_vector=[0.1, 0.2, 0.3, 0.4], limit=1
        )
        self.assertGreaterEqual(len(search_result), 1)
        self.assertEqual(search_result[0]["id"], "vec1")

        # Delete Vectors
        delete_result = self.adapter.delete_vectors(
            collection_name=collection_name, vector_ids=["vec1"]
        )
        self.assertEqual(delete_result["deleted_count"], 1)

        # Delete Collection
        self.adapter.delete_collection(collection_name=collection_name)


if __name__ == "__main__":
    unittest.main()
