"""
Qdrant Collection Inspector
This script inspects existing collections in Qdrant.
"""

from qdrant_client import QdrantClient


def inspect_collections():
    """Inspect existing Qdrant collections."""
    client = QdrantClient(host="localhost", port=6333)
    collections = client.get_collections()

    print("\nExisting Collections:")
    print("--------------------")
    for collection in collections.collections:
        print(f"Collection Name: {collection.name}")
        config = client.get_collection(collection.name)
        print(f"Vector Size: {config.config.params.vectors.size}")
        print(f"Distance: {config.config.params.vectors.distance}\n")


if __name__ == "__main__":
    inspect_collections()
