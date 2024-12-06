"""
Qdrant Docker demo using Vector SDK
Shows how to perform basic vector operations using the SDK.
"""

from vector_sdk import VectorSDK
from vector_sdk.utils.telemetry import Telemetry


def main():
    """Test basic vector operations with Docker deployment."""
    # Initialize SDK with telemetry
    sdk = VectorSDK(telemetry=Telemetry())

    # Get Qdrant adapter
    adapter = sdk.get_adapter("qdrant")

    # Connect to Docker instance
    adapter.connect({"host": "localhost", "port": 6333, "prefer_grpc": True})
    print("Connected to Qdrant Docker instance")

    # Create collection
    collection_name = "test_collection"
    adapter.create_collection(
        name=collection_name, vector_size=4, distance_metric="DOT"
    )
    print(f"Collection '{collection_name}' created")

    # Insert vectors with payload
    vectors = [[0.05, 0.61, 0.76, 0.74], [0.19, 0.81, 0.75, 0.11]]
    ids = ["1", "2"]  # Note: SDK uses string IDs
    metadata = [{"city": "Berlin"}, {"city": "London"}]

    result = adapter.upsert_vectors(
        collection_name=collection_name,
        vectors=vectors,
        ids=ids,
        metadata=metadata,
    )
    print(f"Vectors inserted: {result}")

    # Search with filter
    search_results = adapter.search_vectors(
        collection_name=collection_name,
        query_vector=[0.2, 0.1, 0.9, 0.7],
        filter_params={"city": "London"},
        limit=1,
    )

    print("\nFiltered Search Results:")
    for result in search_results:
        print(f"City: {result['payload']['city']}, Score: {result['score']}")


if __name__ == "__main__":
    main()
