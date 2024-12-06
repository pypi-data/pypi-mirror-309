from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, BinaryIO, Literal, TextIO, TypeVar, Union

Self = TypeVar("Self", bound="VectorDBInterface")


class DistanceMetric(Enum):
    """Supported distance metrics for vector similarity."""

    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"


class VectorDBInterface(ABC):
    """Base interface for all vector database adapters.

    This interface defines the standard CRUD operations that all vector database
    adapters must implement, following the LiteLLM pattern for consistency.
    """

    @abstractmethod
    def connect(self: Self, config: dict[str, Any], **kwargs: Any) -> None:
        """Connect to the vector database.

        Args:
            config: Configuration dictionary containing connection details
                   (e.g., host, port, api_key, etc.)
            **kwargs: Provider-specific connection parameters

        Raises:
            ConnectionError: If connection fails due to:
                - Invalid credentials
                - Network issues
                - Service unavailable
            InvalidRequestError: If config parameters are invalid
        """
        pass

    @abstractmethod
    def create_collection(
        self: Self,
        name: str,
        vector_size: int,
        distance_metric: Union[str, DistanceMetric] = DistanceMetric.COSINE,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,  # Provider-specific parameters
    ) -> None:
        """Create a new collection in the database.

        Args:
            name: Name of the collection
            vector_size: Dimensionality of vectors
            distance_metric: Metric for calculating vector similarity
            metadata: Optional collection-level metadata
            **kwargs: Provider-specific parameters

        Raises:
            InvalidRequestError: If parameters are invalid (e.g., invalid name, negative vector size)
            OperationError: If creation fails due to:
                - Collection already exists
                - Database operation failure
                - Resource limits exceeded
        """
        pass

    @abstractmethod
    def upsert_vectors(
        self: Self,
        collection_name: str,
        vectors: list[list[float]],
        *,
        ids: list[str] | None = None,
        metadata: list[dict[str, Any]] | None = None,
        batch_size: int = 100,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Insert or update vectors in a collection.

        This method handles both insertion of new vectors and updates to existing ones.
        If IDs are provided and they already exist, the vectors will be updated.
        If IDs are provided but don't exist, or if no IDs are provided, new vectors
        will be inserted.

        Args:
            collection_name: Target collection
            vectors: List of vector data
            ids: Optional list of IDs for the vectors. If provided for existing IDs,
                 those vectors will be updated instead of inserted
            metadata: Optional metadata for each vector
            batch_size: Size of batches for operation
            **kwargs: Provider-specific parameters

        Returns:
            Operation status information containing:
                - Number of vectors inserted
                - Number of vectors updated
                - Operation timing
                - Any provider-specific details

        Raises:
            InvalidRequestError: If input parameters are invalid:
                - Mismatched lengths of vectors, ids, or metadata
                - Invalid vector dimensions
                - Invalid metadata format
            OperationError: If operation fails due to:
                - Collection not found
                - Database operation failure
            ConnectionError: If connection is lost during operation
        """
        pass

    @abstractmethod
    def search_vectors(
        self: Self,
        collection_name: str,
        query_vector: list[float],
        *,
        limit: int = 10,
        filter: dict[str, Any] | None = None,
        include_metadata: bool = True,
        include_vectors: bool = False,
        **kwargs: Any,  # Provider-specific parameters
    ) -> list[dict[str, Any]]:
        """Search for similar vectors in the collection.

        Args:
            collection_name: Name of the collection to search
            query_vector: The vector to search against
            limit: Number of results to return
            filter: Optional filter for vectors to include in search
            include_metadata: Whether to include metadata in results
            include_vectors: Whether to include vector data in results
            **kwargs: Provider-specific parameters

        Returns:
            List of search results with vector details

        Raises:
            OperationError: If search fails due to:
                - Invalid collection name
                - Invalid query vector format
                - Invalid filter format
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def delete_vectors(
        self: Self,
        collection_name: str,
        ids: list[str],
        *,
        wait: bool = True,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Delete vectors from a collection.

        Args:
            collection_name: Name of the collection
            ids: List of vector IDs to delete
            wait: Whether to wait for the operation to complete
            **kwargs: Provider-specific parameters

        Returns:
            Operation status information

        Raises:
            OperationError: If deletion fails due to:
                - Invalid collection name
                - Invalid IDs format
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def list_collections(self: Self) -> list[str]:
        """List all available collections.

        Returns:
            List of collection names

        Raises:
            OperationError: If listing fails due to:
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def delete_collection(
        self: Self,
        name: str,
        **kwargs: Any,  # Provider-specific parameters
    ) -> None:
        """Delete a collection.

        Args:
            name: Name of the collection to delete
            **kwargs: Provider-specific parameters

        Raises:
            OperationError: If deletion fails due to:
                - Invalid collection name
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def collection_info(
        self: Self,
        name: str,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Get information about a collection.

        Args:
            name: Name of the collection

        Returns:
            Collection statistics and configuration

        Raises:
            OperationError: If retrieval fails due to:
                - Invalid collection name
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def export_collection(
        self: Self,
        collection_name: str,
        destination: str | Path | BinaryIO,
        *,
        format: Literal["json", "ndjson", "binary"] = "json",
        include_vectors: bool = True,
        include_metadata: bool = True,
        batch_size: int = 1000,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Export collection data to a file.

        Args:
            collection_name: Name of the collection to export
            destination: Destination path or file-like object
            format: Export file format
            include_vectors: Whether to include vectors in the export
            include_metadata: Whether to include metadata in the export
            batch_size: Number of records per export batch
            **kwargs: Provider-specific parameters

        Returns:
            Export operation status

        Raises:
            OperationError: If export fails due to:
                - Invalid collection name
                - Invalid destination format
                - Invalid format
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def import_collection(
        self: Self,
        collection_name: str,
        source: str | Path | BinaryIO | TextIO,
        *,
        format: Literal["json", "ndjson", "binary"] = "json",
        batch_size: int = 1000,
        update_existing: bool = False,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Import data into a collection.

        Args:
            collection_name: Name of the collection to import into
            source: Source path or file-like object
            format: Import file format
            batch_size: Number of records per import batch
            update_existing: Whether to update existing vectors
            **kwargs: Provider-specific parameters

        Returns:
            Import operation status

        Raises:
            OperationError: If import fails due to:
                - Invalid collection name
                - Invalid source format
                - Invalid format
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def embed_collection(
        self: Self,
        collection_name: str,
        model: str = "default",
        batch_size: int = 32,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Embed items in a collection.

        Args:
            collection_name: Name of the collection to embed
            model: Model to use for embedding
            batch_size: Number of items to embed at once
            **kwargs: Provider-specific parameters

        Returns:
            Dictionary containing embedding operation results

        Raises:
            OperationError: If embedding fails due to:
                - Invalid collection name
                - Invalid model
                - Provider-specific issues
        """
        pass

    @abstractmethod
    def reembed_collection(
        self: Self,
        collection_name: str,
        model: str = "default",
        field: str = "text",
        batch_size: int = 32,
        filter: dict[str, Any] | None = None,
        **kwargs: Any,  # Provider-specific parameters
    ) -> dict[str, Any]:
        """Re-embed vectors in a collection using a new model.

        Args:
            collection_name: Name of the collection to re-embed
            model: New embedding model to use
            field: Metadata field containing text to re-embed
            batch_size: Batch size for re-embedding
            filter: Optional filter for vectors to re-embed
            **kwargs: Provider-specific parameters

        Returns:
            Re-embedding operation status

        Raises:
            OperationError: If re-embedding fails due to:
                - Invalid collection name
                - Invalid model
                - Invalid field
                - Invalid filter format
                - Provider-specific issues
        """
        pass
