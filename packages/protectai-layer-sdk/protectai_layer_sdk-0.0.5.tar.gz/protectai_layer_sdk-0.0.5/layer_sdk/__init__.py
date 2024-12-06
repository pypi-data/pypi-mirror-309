"""Init file for the Layer SDK."""

from .auth import AuthProvider, OIDCClientCredentials
from .client import Client
from .schemas import (
    SessionRequest,
    SessionActionKind,
    SessionActionError,
    SessionActionRequest,
    SessionActionScanner,
)
from .exceptions import (
    LayerAuthError,
    LayerHTTPError,
    LayerRequestError,
    LayerSDKException,
    LayerRequestPreparationError,
    LayerMissingRequiredConfigurationError,
)

layer = Client()

__all__ = [
    "layer",
    "AuthProvider",
    "SessionActionKind",
    "SessionRequest",
    "SessionActionError",
    "SessionActionRequest",
    "SessionActionScanner",
    "OIDCClientCredentials",
    "LayerAuthError",
    "LayerHTTPError",
    "LayerSDKException",
    "LayerMissingRequiredConfigurationError",
    "LayerRequestPreparationError",
    "LayerRequestError",
]
