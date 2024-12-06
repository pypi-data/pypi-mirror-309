from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Literal,
    Self,
    TextIO,
    Union,
)

from ..core.vector_db_interface import DistanceMetric
from ..exceptions import ConnectionError, InvalidRequestError
from ..utils.telemetry import Telemetry
from .abc_adapter import ABCAdapter

# Type hints for concrete implementations
VectorType = list[float]
VectorsType = list[VectorType]
MetadataType = dict[str, Any]
MetadataListType = list[MetadataType]
CollectionConfigType = dict[str, Any]
SearchResultType = dict[str, Any]


class BaseAdapter(ABCAdapter):
    """Base adapter class implementing common functionality for vector database adapters.

    This class provides shared implementation details and utility methods that can be
    used across different vector database adapters.
    """

    DB_NAME_SLUG: str = "base"  # Override in subclasses with specific DB name

    def __init__(self, telemetry: Telemetry) -> None:
        """Initialize the base adapter.

        Args:
            telemetry: Telemetry instance for usage tracking
        """
        self.telemetry = telemetry
        self._is_connected = False

    @property
    def is_connected(self) -> bool:
        """Get the connection status."""
        return self._is_connected

    def _track_operation(
        self, operation: str, properties: dict[str, Any] = None
    ) -> None:
        """Track an operation via telemetry."""
        if properties is None:
            properties = {}

        properties["db_type"] = self.DB_NAME_SLUG
        self.telemetry.track_event(operation, properties)

    def _ensure_connected(self) -> None:
        """Verify that the adapter is connected before operations."""
        if not self._is_connected:
            raise ConnectionError(
                "Not connected to database. Call connect() before performing operations.",
                provider=self.DB_NAME_SLUG,
            )

    def _validate_vectors(
        self,
        vectors: list[list[float]],
        vector_size: int | None = None,
        ids: list[str] | None = None,
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        """Validate vector data and related parameters."""
        if not vectors:
            raise InvalidRequestError(
                "Vector list cannot be empty",
                provider=self.DB_NAME_SLUG,
            )

        if vector_size is not None:
            for i, vec in enumerate(vectors):
                if len(vec) != vector_size:
                    raise InvalidRequestError(
                        f"Vector at index {i} has incorrect dimensionality. "
                        f"Expected {vector_size}, got {len(vec)}",
                        provider=self.DB_NAME_SLUG,
                    )

        if ids is not None and len(ids) != len(vectors):
            raise InvalidRequestError(
                f"Number of IDs ({len(ids)}) does not match number of vectors ({len(vectors)})",
                provider=self.DB_NAME_SLUG,
            )

        if metadata is not None and len(metadata) != len(vectors):
            raise InvalidRequestError(
                f"Number of metadata entries ({len(metadata)}) does not match number of vectors ({len(vectors)})",
                provider=self.DB_NAME_SLUG,
            )

    def _normalize_distance_metric(
        self, metric: Union[str, DistanceMetric]
    ) -> DistanceMetric:
        """Normalize distance metric input to DistanceMetric enum."""
        if isinstance(metric, DistanceMetric):
            return metric

        try:
            return DistanceMetric(metric.lower())
        except ValueError as err:
            raise InvalidRequestError(
                f"Invalid distance metric: {metric}. "
                f"Supported metrics: {[m.value for m in DistanceMetric]}",
                provider=self.DB_NAME_SLUG,
            ) from err

    def _validate_file_format(
        self, format: Literal["json", "ndjson", "binary"]
    ) -> None:
        """Validate file format for import/export operations."""
        valid_formats = ["json", "ndjson", "binary"]
        if format not in valid_formats:
            raise InvalidRequestError(
                f"Invalid file format: {format}. Supported formats: {valid_formats}",
                provider=self.DB_NAME_SLUG,
            )

    def _resolve_file_path(
        self, path_or_file: Union[str, Path, BinaryIO, TextIO]
    ) -> Path:
        """Resolve file path from string, Path, or file-like object."""
        if isinstance(path_or_file, str | Path):
            return Path(path_or_file)
        elif hasattr(path_or_file, "name"):
            return Path(path_or_file.name)
        else:
            raise InvalidRequestError(
                "Invalid file path or file-like object",
                provider=self.DB_NAME_SLUG,
            )

    def connect(self: Self, config: dict[str, Any], **kwargs: Any) -> None:
        """Connect to the vector database."""
        self._track_operation("connect", {"config_keys": list(config.keys()), **kwargs})
        raise NotImplementedError("Connection not implemented for this adapter")

    def create_collection(
        self: Self,
        name: str,
        vector_size: int,
        distance_metric: Union[str, DistanceMetric] = DistanceMetric.COSINE,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Create a new collection in the database."""
        self._ensure_connected()
        self._track_operation(
            "create_collection",
            {
                "name": name,
                "vector_size": vector_size,
                "distance_metric": str(distance_metric),
                "has_metadata": metadata is not None,
                **kwargs,
            },
        )
        raise NotImplementedError(
            "Collection creation not implemented for this adapter"
        )

    def upsert_vectors(
        self: Self,
        collection_name: str,
        vectors: list[list[float]],
        ids: list[str],
        metadata: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Insert or update vectors in the collection."""
        self._ensure_connected()
        self._validate_vectors(vectors, ids=ids, metadata=metadata)

        self._track_operation(
            "upsert_vectors",
            {
                "collection": collection_name,
                "vector_count": len(vectors),
                "has_metadata": metadata is not None,
                **kwargs,
            },
        )
        raise NotImplementedError("Vector upsert not implemented for this adapter")

    def search_vectors(
        self: Self,
        collection_name: str,
        query_vectors: list[list[float]],
        k: int = 10,
        include_vectors: bool = True,
        include_metadata: bool = True,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for similar vectors in the collection."""
        self._ensure_connected()
        self._validate_collection_name(collection_name)
        self._validate_vectors(query_vectors)
        self._validate_search_params(
            query_vectors[0], k, include_vectors, include_metadata
        )

        self._track_operation(
            "search_vectors",
            {
                "collection": collection_name,
                "query_count": len(query_vectors),
                "k": k,
                "include_vectors": include_vectors,
                "include_metadata": include_metadata,
                "has_filter": filter is not None,
                **kwargs,
            },
        )
        raise NotImplementedError("Vector search not implemented for this adapter")

    def delete_vectors(
        self: Self,
        collection_name: str,
        ids: list[str],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Delete vectors from the collection."""
        self._ensure_connected()

        self._track_operation(
            "delete_vectors",
            {
                "collection": collection_name,
                "id_count": len(ids),
                **kwargs,
            },
        )
        raise NotImplementedError("Vector deletion not implemented for this adapter")

    def list_collections(self: Self) -> list[str]:
        """List all available collections."""
        self._ensure_connected()
        self._track_operation("list_collections")
        raise NotImplementedError("Collection listing not implemented for this adapter")

    def delete_collection(
        self: Self,
        name: str,
        **kwargs: Any,
    ) -> None:
        """Delete a collection."""
        self._ensure_connected()
        self._track_operation("delete_collection", {"name": name, **kwargs})
        raise NotImplementedError(
            "Collection deletion not implemented for this adapter"
        )

    def collection_info(
        self: Self,
        name: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Get information about a collection."""
        self._ensure_connected()
        self._track_operation("collection_info", {"name": name, **kwargs})
        raise NotImplementedError("Collection info not implemented for this adapter")

    def export_collection(
        self: Self,
        collection_name: str,
        destination: Union[str, Path, BinaryIO],
        *,
        format: Literal["json", "ndjson", "binary"] = "json",
        include_vectors: bool = True,
        include_metadata: bool = True,
        batch_size: int = 1000,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Export collection data to a file."""
        self._ensure_connected()
        self._validate_file_format(format)

        # Path validation result stored for use by concrete implementations
        dest_path = self._resolve_file_path(destination)

        self._track_operation(
            "export_collection",
            {
                "collection": collection_name,
                "format": format,
                "include_vectors": include_vectors,
                "include_metadata": include_metadata,
                "batch_size": batch_size,
                **kwargs,
            },
        )
        raise NotImplementedError("Collection export not implemented for this adapter")

    def import_collection(
        self: Self,
        collection_name: str,
        source: Union[str, Path, BinaryIO, TextIO],
        *,
        format: Literal["json", "ndjson", "binary"] = "json",
        batch_size: int = 1000,
        update_existing: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Import data into a collection."""
        self._ensure_connected()
        self._validate_file_format(format)

        # Path validation result stored for use by concrete implementations
        src_path = self._resolve_file_path(source)

        self._track_operation(
            "import_collection",
            {
                "collection": collection_name,
                "format": format,
                "batch_size": batch_size,
                "update_existing": update_existing,
                **kwargs,
            },
        )
        raise NotImplementedError("Collection import not implemented for this adapter")

    def embed_collection(
        self: Self,
        collection_name: str,
        model: str = "default",
        batch_size: int = 32,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Embed items in a collection.

        Args:
            collection_name: Name of the collection to embed
            model: Model to use for embedding
            batch_size: Number of items to embed at once
            **kwargs: Additional provider-specific parameters

        Returns:
            Dictionary containing embedding operation results

        Raises:
            NotImplementedError: When adapter doesn't implement embedding
        """
        self._ensure_connected()
        self._validate_collection_name(collection_name)
        self._validate_batch_size(batch_size)

        self._track_operation(
            "embed_collection",
            {
                "collection": collection_name,
                "model": model,
                "batch_size": batch_size,
                **kwargs,
            },
        )
        raise NotImplementedError(
            "Collection embedding not implemented for this adapter"
        )

    def reembed_collection(
        self: Self,
        collection_name: str,
        model: str = "default",
        field: str = "text",
        batch_size: int = 32,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Re-embed vectors in a collection using a new model."""
        self._ensure_connected()

        self._track_operation(
            "reembed_collection",
            {
                "collection": collection_name,
                "model": model,
                "field": field,
                "batch_size": batch_size,
                "has_filter": filter is not None,
                **kwargs,
            },
        )
        raise NotImplementedError(
            "Collection re-embedding not implemented for this adapter"
        )

    def _get_concrete_adapter_info(self) -> dict[str, Any]:
        """Get information about the concrete adapter implementation.

        This method should be called by concrete adapters to provide
        implementation-specific details for telemetry and debugging.

        Returns:
            Dictionary containing adapter information
        """
        return {
            "adapter_name": self.DB_NAME_SLUG,
            "adapter_class": self.__class__.__name__,
        }

    def _validate_implementation(self) -> None:
        """Validate that all required methods are implemented.

        This method should be called during initialization of concrete adapters
        to ensure all required functionality is implemented.

        Raises:
            NotImplementedError: If any required methods are not implemented
        """
        required_methods = [
            # Core CRUD Operations
            "connect",  # Connection management
            "create_collection",  # Create
            "upsert_vectors",  # Create/Update
            "search_vectors",  # Read
            "delete_vectors",  # Delete
            # Collection Management
            "list_collections",  # Read
            "delete_collection",  # Delete
            "collection_info",  # Read
            # Data Import/Export
            "export_collection",  # Read
            "import_collection",  # Create/Update
            # Embedding Operations
            "embed_collection",  # Create
            "reembed_collection",  # Update
        ]

        for method in required_methods:
            if getattr(self, method).__func__ == getattr(BaseAdapter, method).__func__:
                raise NotImplementedError(
                    f"Method '{method}' must be implemented by concrete adapter"
                )
