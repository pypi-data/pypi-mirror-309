"""
Constants used throughout the binary protocol implementation.
"""

# Header constants
HEADER_SIZE = 2  # bytes (just message type)
MESSAGE_TYPE_SIZE = 2  # bytes
PAYLOAD_LENGTH_SIZE = 4  # bytes (for variable length messages)

# Protocol limits
MAX_PAYLOAD_SIZE = 1024 * 1024  # 1MB
MIN_PAYLOAD_SIZE = 0
MAX_MESSAGE_SIZE = HEADER_SIZE + PAYLOAD_LENGTH_SIZE + MAX_PAYLOAD_SIZE

# Timeout values (in seconds)
DEFAULT_CONNECT_TIMEOUT = 30.0
DEFAULT_READ_TIMEOUT = 30.0
DEFAULT_WRITE_TIMEOUT = 30.0

# Buffer sizes
DEFAULT_BUFFER_SIZE = 8192  # 8KB