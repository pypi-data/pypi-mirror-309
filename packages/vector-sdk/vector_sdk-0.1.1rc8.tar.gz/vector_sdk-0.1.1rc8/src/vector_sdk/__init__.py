"""Vector SDK initialization module."""

from vector_sdk.core.sdk import VectorSDK
from vector_sdk.utils.telemetry import Telemetry


def hello() -> str:
    """Return a greeting message.

    Returns:
        str: A greeting message from the SDK
    """
    return "Hello from vector-sdk!"


__all__ = ["VectorSDK", "Telemetry"]

__version__ = "0.1.1rc8"
