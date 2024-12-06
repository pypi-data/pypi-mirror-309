"""
Qdrant Adapter for Vector SDK
Implements the VectorDBInterface for Qdrant vector database.
"""

import json
from pathlib import Path
from typing import Any, Literal, Optional, Union

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    VectorParams,
)

from ..adapters.base_adapter import BaseAdapter
from ..core.vector_db_interface import DistanceMetric
from ..exceptions import ConnectionError, InvalidRequestError, OperationError
from ..utils.telemetry import Telemetry


class QdrantAdapter(BaseAdapter):
    """Adapter for Qdrant vector database."""

    DB_NAME_SLUG = "qdrant"

    def __init__(self, telemetry: Telemetry) -> None:
        """Initialize QdrantAdapter."""
        super().__init__(telemetry)
        self.client = None
        self.collection_name = None
        self.dimension = 384  # Default dimension for vectors

    def connect(self, config: dict[str, Any], **kwargs: Any) -> None:
        """Connect to Qdrant database."""
        try:
            if config.get("memory_mode"):
                self.client = QdrantClient(":memory:")
            else:
                self.client = QdrantClient(
                    host=config.get("host", "localhost"),
                    port=config.get("port", 6333),
                    prefer_grpc=config.get("prefer_grpc", True),
                    **kwargs,
                )
            self._is_connected = True
            self._track_operation(
                "connect", {"memory_mode": config.get("memory_mode", False)}
            )

        except Exception as err:
            raise OperationError(f"Failed to connect to Qdrant: {str(err)}") from err

    def create_collection(
        self,
        name: str,
        vector_size: int,
        distance_metric: Union[str, DistanceMetric] = DistanceMetric.COSINE,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Create a new collection in the database."""
        self._ensure_connected()
        try:
            # Convert distance metric
            qdrant_distance = Distance.COSINE
            if isinstance(distance_metric, DistanceMetric):
                qdrant_distance = getattr(Distance, distance_metric.value.upper())
            elif isinstance(distance_metric, str):
                qdrant_distance = getattr(Distance, distance_metric.upper())

            if self.client.collection_exists(name):
                raise InvalidRequestError(f"Collection {name} already exists")

            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=vector_size, distance=qdrant_distance),
                **kwargs,
            )

            self._track_operation(
                "create_collection",
                {
                    "name": name,
                    "vector_size": vector_size,
                    "distance_metric": str(distance_metric),
                },
            )

        except Exception as e:
            raise OperationError(f"Failed to create collection: {str(e)}")

    def upsert_vectors(
        self,
        collection_name: str,
        vectors: list[list[float]],
        *,
        ids: Optional[list[str]] = None,
        metadata: Optional[list[dict[str, Any]]] = None,
        batch_size: int = 100,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Insert or update vectors in a collection."""
        self._ensure_connected()
        try:
            # Validate inputs
            self._validate_vectors(vectors, ids=ids, metadata=metadata)

            # Prepare points for upsert
            points = []
            for idx, vector in enumerate(vectors):
                point = {
                    "id": ids[idx] if ids else str(idx),
                    "vector": vector,
                }
                if metadata and idx < len(metadata):
                    point["payload"] = metadata[idx]
                points.append(point)

            # Perform upsert in batches
            for i in range(0, len(points), batch_size):
                batch = points[i : i + batch_size]
                self.client.upsert(
                    collection_name=collection_name, points=batch, wait=True, **kwargs
                )

            result = {
                "inserted_count": len(points),
                "batch_count": (len(points) + batch_size - 1) // batch_size,
            }

            self._track_operation(
                "upsert_vectors",
                {
                    "collection": collection_name,
                    "vector_count": len(vectors),
                    "batch_size": batch_size,
                },
            )

            return result

        except Exception as e:
            raise OperationError(f"Failed to upsert vectors: {str(e)}")

    def search_vectors(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 10,
        filter_params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for similar vectors in a collection."""
        self._ensure_connected()
        try:
            # Prepare filter if provided
            search_filter = None
            if filter_params:
                conditions = []
                for key, value in filter_params.items():
                    conditions.append(
                        FieldCondition(key=key, match=MatchValue(value=value))
                    )
                search_filter = Filter(must=conditions)

            # Perform search
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=search_filter,
                **kwargs,
            )

            # Format results
            formatted_results = [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                    "vector": result.vector if hasattr(result, "vector") else None,
                }
                for result in results
            ]

            self._track_operation(
                "search_vectors",
                {
                    "collection": collection_name,
                    "limit": limit,
                    "has_filter": bool(filter_params),
                },
            )

            return formatted_results

        except Exception as e:
            raise OperationError(f"Failed to search vectors: {str(e)}")

    def delete_vectors(
        self,
        collection_name: str,
        vector_ids: list[str],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Delete vectors from a collection."""
        self._ensure_connected()
        try:
            # Perform deletion
            operation_result = self.client.delete(
                collection_name=collection_name,
                points_selector=vector_ids,
                wait=True,
                **kwargs,
            )

            result = {
                "deleted_count": len(vector_ids),
                "operation_id": str(operation_result.operation_id)
                if hasattr(operation_result, "operation_id")
                else None,
            }

            self._track_operation(
                "delete_vectors",
                {"collection": collection_name, "vector_count": len(vector_ids)},
            )

            return result

        except Exception as e:
            raise OperationError(f"Failed to delete vectors: {str(e)}")

    def list_collections(self) -> list[str]:
        """List all collections in the Qdrant database."""
        self._ensure_connected()
        try:
            collections = self.client.get_collections().collections
            collection_names = [collection.name for collection in collections]

            self._track_operation(
                "list_collections", {"collection_count": len(collection_names)}
            )

            return collection_names

        except Exception as e:
            raise OperationError(f"Failed to list collections: {str(e)}")

    def collection_info(self, name: str) -> dict[str, Any]:
        """Retrieve information about a specific collection."""
        self._ensure_connected()
        try:
            if not self.client.collection_exists(name):
                raise InvalidRequestError(f"Collection '{name}' does not exist")

            config = self.client.get_collection(name)
            info = {
                "name": name,
                "vector_size": config.config.params.vectors.size,
                "distance_metric": config.config.params.vectors.distance,
                "created_at": config.status.created_at.isoformat()
                if config.status.created_at
                else None,
                "updated_at": config.status.last_update.isoformat()
                if config.status.last_update
                else None,
                "vectors_count": config.status.vectors_count,
                "payload_count": config.status.payload_count,
            }

            self._track_operation("collection_info", {"collection": name})

            return info

        except Exception as e:
            raise OperationError(f"Failed to retrieve collection info: {str(e)}")

    def delete_collection(self, name: str) -> None:
        """Delete a collection from the Qdrant database."""
        self._ensure_connected()
        try:
            if not self.client.collection_exists(name):
                raise InvalidRequestError(f"Collection '{name}' does not exist")

            self.client.delete_collection(collection_name=name)

            self._track_operation("delete_collection", {"name": name})

        except Exception as e:
            raise OperationError(f"Failed to delete collection '{name}': {str(e)}")

    def export_collection(
        self,
        name: str,
        file_path: Union[str, Path],
        format: Literal["ndjson"] = "ndjson",
        **kwargs: Any,
    ) -> None:
        """Export a collection's data to a file."""
        self._ensure_connected()
        try:
            if not self.client.collection_exists(name):
                raise InvalidRequestError(f"Collection '{name}' does not exist")

            if format != "ndjson":
                raise InvalidRequestError(f"Unsupported export format: {format}")

            points = self.client.scroll(
                collection_name=name, limit=1000, with_payload=True, **kwargs
            )

            with open(file_path, "w", encoding="utf-8") as f:
                for point in points:
                    json_point = {
                        "id": point.id,
                        "vector": point.vector,
                        "payload": point.payload,
                    }
                    f.write(json.dumps(json_point) + "\n")

            self._track_operation(
                "export_collection",
                {"name": name, "file_path": str(file_path), "format": format},
            )

        except Exception as e:
            raise OperationError(f"Failed to export collection '{name}': {str(e)}")

    def import_collection(
        self,
        name: str,
        file_path: Union[str, Path],
        vector_size: int,
        distance_metric: Union[str, DistanceMetric] = DistanceMetric.COSINE,
        format: Literal["ndjson"] = "ndjson",
        **kwargs: Any,
    ) -> None:
        """Import data into a collection from a file."""
        self._ensure_connected()
        try:
            if self.client.collection_exists(name):
                self.client.delete_collection(collection_name=name)
                self._track_operation("delete_collection_before_import", {"name": name})

            # Create collection
            self.create_collection(
                name=name,
                vector_size=vector_size,
                distance_metric=distance_metric,
                **kwargs,
            )

            # Read and prepare points
            points = []
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line.strip())
                    point = {
                        "id": data["id"],
                        "vector": data["vector"],
                        "payload": data.get("payload", {}),
                    }
                    points.append(point)

            # Upsert points in batches
            batch_size = kwargs.get("batch_size", 100)
            for i in range(0, len(points), batch_size):
                batch = points[i : i + batch_size]
                self.client.upsert(collection_name=name, points=batch, wait=True)

            self._track_operation(
                "import_collection",
                {
                    "name": name,
                    "file_path": str(file_path),
                    "format": format,
                    "vector_count": len(points),
                },
            )

        except Exception as e:
            raise OperationError(f"Failed to import collection '{name}': {str(e)}")

    def embed_collection(
        self,
        name: str,
        documents: list[str],
        embedding_function: callable,
        metadata: Optional[list[dict[str, Any]]] = None,
        ids: Optional[list[str]] = None,
        batch_size: int = 100,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Embed documents and insert into the collection."""
        self._ensure_connected()
        try:
            # Embed documents
            embeddings = embedding_function(documents)
            vectors = [
                embed.tolist() if hasattr(embed, "tolist") else list(embed)
                for embed in embeddings
            ]

            # Upsert vectors
            result = self.upsert_vectors(
                collection_name=name,
                vectors=vectors,
                ids=ids,
                metadata=metadata,
                batch_size=batch_size,
                **kwargs,
            )

            self._track_operation(
                "embed_collection",
                {
                    "collection": name,
                    "document_count": len(documents),
                    "batch_size": batch_size,
                },
            )

            return result

        except Exception as e:
            raise OperationError(
                f"Failed to embed and insert documents into '{name}': {str(e)}"
            )

    def reembed_collection(
        self,
        name: str,
        new_embedding_function: callable,
        field: str = "text",
        batch_size: int = 100,
        filter_params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Re-embed documents in the collection with a new embedding function."""
        self._ensure_connected()
        try:
            # Search points to re-embed
            search_filter = None
            if filter_params:
                conditions = []
                for key, value in filter_params.items():
                    conditions.append(
                        FieldCondition(key=key, match=MatchValue(value=value))
                    )
                search_filter = Filter(must=conditions)

            points_to_reembed = self.client.scroll(
                collection_name=name,
                filter=search_filter,
                limit=batch_size,
                with_payload=True,
                **kwargs,
            )

            if not points_to_reembed:
                raise InvalidRequestError(
                    f"No points found to re-embed in collection '{name}'"
                )

            # Extract texts for embedding
            texts = [point.payload[field] for point in points_to_reembed]
            embeddings = new_embedding_function(texts)
            vectors = [
                embed.tolist() if hasattr(embed, "tolist") else list(embed)
                for embed in embeddings
            ]

            # Prepare upsert payload
            upsert_points = []
            for point, vector in zip(points_to_reembed, vectors, strict=True):
                upsert_points.append(
                    {"id": point.id, "vector": vector, "payload": point.payload}
                )

            # Upsert re-embedded vectors
            result = self.client.upsert(
                collection_name=name, points=upsert_points, wait=True, **kwargs
            )

            self._track_operation(
                "reembed_collection",
                {
                    "collection": name,
                    "reembedded_count": len(upsert_points),
                    "batch_size": batch_size,
                },
            )

            return {"reembedded_count": len(upsert_points)}

        except Exception as e:
            raise OperationError(f"Failed to re-embed collection '{name}': {str(e)}")

    def _ensure_connected(self) -> None:
        """Ensure that the adapter is connected to the database."""
        if not self._is_connected or not self.client:
            raise ConnectionError("Not connected to the Qdrant database")

    def _validate_vectors(
        self,
        vectors: list[list[float]],
        ids: Optional[list[str]] = None,
        metadata: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        """Validate the vectors, IDs, and metadata before upserting."""
        if not vectors:
            raise InvalidRequestError("Vectors list cannot be empty")

        vector_length = len(vectors[0])
        if vector_length != self.dimension:
            raise InvalidRequestError(
                f"Each vector must have {self.dimension} dimensions"
            )

        if ids and len(ids) != len(vectors):
            raise InvalidRequestError("Length of IDs must match length of vectors")

        if metadata and len(metadata) != len(vectors):
            raise InvalidRequestError("Length of metadata must match length of vectors")
