"""
Qdrant Docker Mode Demo
This example shows how to use Qdrant with Docker deployment.
"""

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    VectorParams,
)


def test_docker():
    """Test basic vector operations with Docker deployment."""
    # Connect to Docker instance
    client = QdrantClient(host="localhost", port=6333)
    print("Connected to Qdrant Docker instance")

    # Create collection
    collection_name = "test_collection"
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )
    print(f"Collection '{collection_name}' created")

    # Insert vectors with payload
    operation_info = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=[
            {
                "id": 1,
                "vector": [0.05, 0.61, 0.76, 0.74],
                "payload": {"city": "Berlin"},
            },
            {
                "id": 2,
                "vector": [0.19, 0.81, 0.75, 0.11],
                "payload": {"city": "London"},
            },
        ],
    )
    print(f"Vectors inserted: {operation_info}")

    # Search with filter
    search_result = client.search(
        collection_name=collection_name,
        query_vector=[0.2, 0.1, 0.9, 0.7],
        query_filter=Filter(
            must=[FieldCondition(key="city", match=MatchValue(value="London"))]
        ),
        limit=1,
    )

    print("\nFiltered Search Results:")
    for result in search_result:
        print(f"City: {result.payload['city']}, Score: {result.score}")


if __name__ == "__main__":
    test_docker()
