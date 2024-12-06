"""Vector SDK Exception Hierarchy.

This module defines standardized exceptions for vector database operations,
following a similar pattern to LiteLLM's exception mapping approach.
"""


class VectorDBError(Exception):
    """Base exception class for Vector SDK.

    All Vector SDK exceptions inherit from this class, allowing for
    catch-all error handling similar to LiteLLM's approach.
    """

    def __init__(
        self, message: str, status_code: int | None = None, provider: str | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.provider = provider


class ConnectionError(VectorDBError):
    """Raised when connection to vector database fails.

    Maps to HTTP 500-level errors for API connections.
    """

    pass


class AuthenticationError(ConnectionError):
    """Raised when authentication fails.

    Maps to HTTP 401 errors.
    """

    pass


class InvalidRequestError(VectorDBError):
    """Raised when request parameters are invalid.

    Maps to HTTP 400 errors.
    """

    pass


class ResourceNotFoundError(VectorDBError):
    """Raised when requested resource doesn't exist.

    Maps to HTTP 404 errors.
    """

    pass


class ResourceExistsError(InvalidRequestError):
    """Raised when attempting to create a resource that already exists.

    Maps to HTTP 409 errors.
    """

    pass


class OperationError(VectorDBError):
    """Raised when a vector database operation fails.

    Generic error for operation failures, maps to HTTP 500 errors.
    """

    pass


class RateLimitError(VectorDBError):
    """Raised when rate limits are exceeded.

    Maps to HTTP 429 errors.
    """

    pass


class DimensionalityError(InvalidRequestError):
    """Raised for vector dimensionality mismatches.

    Specific type of InvalidRequestError for vector operations.
    """

    pass
