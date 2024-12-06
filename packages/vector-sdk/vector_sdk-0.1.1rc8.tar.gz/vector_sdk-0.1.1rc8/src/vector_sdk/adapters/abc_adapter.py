from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, BinaryIO, Literal, TextIO, Union

from ..core.vector_db_interface import DistanceMetric, VectorDBInterface


class ABCAdapter(VectorDBInterface, ABC):
    """Abstract base class for vector database adapters.

    This class defines the core interface that all vector database adapters must implement,
    along with basic type definitions and docstrings. Implementation details are left to
    the concrete adapter classes.
    """

    DB_NAME_SLUG: str

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Connection status of the adapter."""
        pass

    @abstractmethod
    def _track_operation(
        self, operation: str, properties: dict[str, Any] = None
    ) -> None:
        """Track an operation via telemetry.

        Args:
            operation: Name of the operation being performed
            properties: Additional properties to track
        """
        pass

    @abstractmethod
    def _ensure_connected(self) -> None:
        """Verify that the adapter is connected before operations.

        Raises:
            ConnectionError: If the adapter is not connected
        """
        pass

    @abstractmethod
    def _validate_vectors(
        self,
        vectors: list[list[float]],
        vector_size: int | None = None,
        ids: list[str] | None = None,
        metadata: list[dict[str, Any]] | None = None,
    ) -> None:
        """Validate vector data and related parameters.

        Args:
            vectors: List of vectors to validate
            vector_size: Expected vector dimensionality
            ids: Optional vector IDs to validate
            metadata: Optional metadata to validate

        Raises:
            InvalidRequestError: If validation fails
        """
        pass

    @abstractmethod
    def _normalize_distance_metric(
        self, metric: Union[str, DistanceMetric]
    ) -> DistanceMetric:
        """Normalize distance metric input to DistanceMetric enum.

        Args:
            metric: Distance metric as string or enum

        Returns:
            Normalized DistanceMetric enum value

        Raises:
            InvalidRequestError: If metric is invalid
        """
        pass

    @abstractmethod
    def _validate_file_format(
        self, format: Literal["json", "ndjson", "binary"]
    ) -> None:
        """Validate file format for import/export operations.

        Args:
            format: File format to validate

        Raises:
            InvalidRequestError: If format is invalid
        """
        pass

    @abstractmethod
    def _resolve_file_path(
        self, path_or_file: Union[str, Path, BinaryIO, TextIO]
    ) -> Path:
        """Resolve file path from string, Path, or file-like object.

        Args:
            path_or_file: File path or file-like object

        Returns:
            Resolved Path object

        Raises:
            InvalidRequestError: If path is invalid
        """
        pass
