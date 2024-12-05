"""
Binary Protocol API
A lightweight binary protocol implementation for efficient client-server communication.
"""

from .protocol.config import ProtocolConfig
from .protocol.exceptions import (
    ProtocolError,
    MessageValidationError,
    PayloadError,
    ConnectionError,
    AuthenticationError
)

from .client import BinaryClient
from .server import BinaryServer

__version__ = "0.1.0"
__all__ = [
    'ProtocolConfig',
    'BinaryClient',
    'BinaryServer',
    'ProtocolError',
    'MessageValidationError',
    'PayloadError',
    'ConnectionError',
    'AuthenticationError'
]