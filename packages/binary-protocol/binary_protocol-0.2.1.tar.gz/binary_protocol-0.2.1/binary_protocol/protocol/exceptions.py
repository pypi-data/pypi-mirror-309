"""
Custom exceptions for the binary protocol implementation.
"""

class ProtocolError(Exception):
    """Base exception for all protocol-related errors"""
    pass

class MessageValidationError(ProtocolError):
    """Raised when message validation fails"""
    pass

class PayloadError(ProtocolError):
    """Raised when there are payload-related issues"""
    pass

class ConnectionError(ProtocolError):
    """Raised when connection-related issues occur"""
    pass

class AuthenticationError(ProtocolError):
    """Raised when authentication fails"""
    pass

class MessageNotFoundError(ProtocolError):
    """Raised when a message type or handler is not found"""
    pass

class MessageHandlerNotFoundError(MessageNotFoundError):
    """Raised when no handler is found for a message type"""
    pass

class MessageStructureNotFoundError(MessageNotFoundError):
    """Raised when no structure is defined for a message type"""
    pass 