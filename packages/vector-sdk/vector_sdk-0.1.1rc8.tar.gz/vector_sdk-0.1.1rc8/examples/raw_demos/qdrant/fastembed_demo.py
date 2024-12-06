"""
Qdrant FastEmbed Demo
This example shows how to use Qdrant with FastEmbed for text embeddings.
"""

import time

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


def test_fastembed():
    """Test text embedding and search using FastEmbed."""
    # Initialize client with FastEmbed
    client = QdrantClient(host="localhost", port=6333, prefer_grpc=True)
    print("Connected to Qdrant")

    # Delete existing collection if it exists
    collection_name = "demo_collection"
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
        print(f"Existing collection '{collection_name}' deleted")

    # Create collection with FastEmbed's default dimension (384)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    print(f"Collection '{collection_name}' created")

    # Verify collection parameters
    collection_info = client.get_collection(collection_name)
    print(
        f"Collection '{collection_name}' parameters: {collection_info.config.params.vectors}"
    )

    # Prepare documents and metadata
    docs = [
        "Qdrant has Langchain integrations",
        "Qdrant also has Llama Index integrations",
        "Qdrant supports semantic search with FastEmbed",
        "Vector databases are used for similarity search",
    ]
    metadata = [
        {"source": "Langchain-docs", "category": "integration"},
        {"source": "Linkedin-docs", "category": "integration"},
        {"source": "Qdrant-docs", "category": "feature"},
        {"source": "Wiki", "category": "general"},
    ]
    ids = [1, 2, 3, 4]

    # Add documents with metadata
    try:
        # Initialize the embedding model with specific parameters
        embedding_model = TextEmbedding(
            model_name="BAAI/bge-small-en", max_length=512, cache_dir="./model_cache"
        )

        # Generate embeddings and ensure they're lists
        embeddings = list(embedding_model.embed(docs))

        points = []
        for id, embedding, doc, meta in zip(
            ids, embeddings, docs, metadata, strict=True
        ):
            # Convert numpy array to list and ensure proper structure
            vector_list = (
                embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
            )
            points.append(
                {
                    "id": id,
                    "vector": vector_list,
                    "payload": {
                        "text": doc,
                        "source": meta["source"],
                        "category": meta["category"],
                    },
                }
            )

        client.upsert(collection_name=collection_name, points=points, wait=True)
        print("Documents added successfully")

        # Add delay to ensure collection is updated
        time.sleep(1)

    except Exception as e:
        print(f"Failed to add documents: {e}")
        return  # Exit if document addition fails

    # Search using text query
    try:
        query = "What integrations are available?"
        query_embedding = embedding_model.embed([query])[0]  # Changed to embed()

        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_embedding.tolist(),
            limit=2,
        )

        print("\nSearch Results:")
        for result in search_result:
            print(f"Document: {result.payload['text']}")
            print(f"Source: {result.payload['source']}")
            print(f"Category: {result.payload['category']}")
            print(f"Score: {result.score}\n")
    except Exception as e:
        print(f"Failed to query documents: {e}")


if __name__ == "__main__":
    test_fastembed()
