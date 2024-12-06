"""
Pinecone Vector Database Demo
Basic operations with Pinecone's Python client.
"""

import os

import pinecone


def test_pinecone():
    # Initialize client
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV")
    )
    print("Connected to Pinecone")

    # Create index
    pinecone.create_index("demo-index", dimension=8)
    index = pinecone.Index("demo-index")
    print("Index created")

    # Upsert vectors
    index.upsert(
        [("vec1", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], {"category": "test"})]
    )
    print("Vectors upserted")


if __name__ == "__main__":
    test_pinecone()
