"""
Qdrant Memory Mode Demo
This example shows how to use Qdrant in memory mode for development and testing.
"""

from qdrant_client import QdrantClient


def test_memory():
    """Test basic vector operations in memory mode."""
    client = QdrantClient(":memory:")
    print("Memory mode initialized")
    # Rest of the code...


if __name__ == "__main__":
    test_memory()
