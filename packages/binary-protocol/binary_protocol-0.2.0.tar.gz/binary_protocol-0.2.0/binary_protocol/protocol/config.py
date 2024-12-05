"""
Configuration class for customizing protocol behavior
"""

from dataclasses import dataclass
from typing import Type, Optional, Any, Callable, Dict, Tuple
from enum import IntEnum
import struct

from .message_structure import MessageStructure
from .constants import MAX_PAYLOAD_SIZE, DEFAULT_CONNECT_TIMEOUT, DEFAULT_READ_TIMEOUT, DEFAULT_WRITE_TIMEOUT, DEFAULT_BUFFER_SIZE

class TransportType(IntEnum):
    TCP = 1
    UDP = 2

@dataclass
class ProtocolConfig:
    """
    Configuration class for customizing protocol behavior
    
    Attributes:
        message_type_enum: The enum class defining message types
        message_structures: Dictionary of message structures per message type
        header_format: Format string for struct packing/unpacking header
        max_payload_size: Maximum allowed payload size in bytes
        header_size: Size of message header in bytes (computed from header_format)
        connect_timeout: Connection timeout in seconds
        read_timeout: Read operation timeout in seconds
        write_timeout: Write operation timeout in seconds
        buffer_size: Network buffer size in bytes
        validate_message: Optional custom message validation function
        serialize_message: Optional custom message serialization function
        deserialize_message: Optional custom message deserialization function
        checksum_size: Size of checksum in bytes
        checksum_enabled: Whether checksum is enabled
        checksum_func: Custom checksum function
        checksum_verify: Custom checksum verification function
        error_handler: Optional custom error handler function
        not_found_type: Custom NOT_FOUND type
        transport_type: Transport type
        enable_performance_improvements: Whether to enable performance improvements
    """
    def __init__(self, 
                 message_type_enum: Any,
                 message_structures: Dict[Any, 'MessageStructure'],
                 transport_type: TransportType = TransportType.TCP,
                 header_format: str = ">H",  # 2-byte unsigned short
                 max_payload_size: int = 1024 * 1024,  # 1MB
                 connect_timeout: float = 30.0,
                 read_timeout: float = 30.0,
                 write_timeout: float = DEFAULT_WRITE_TIMEOUT,
                 buffer_size: int = DEFAULT_BUFFER_SIZE,
                 not_found_type: Optional[Any] = None,  # Allow custom NOT_FOUND type
                 validate_message: Optional[Callable[[Any], bool]] = None,
                 serialize_message: Optional[Callable[[Any], bytes]] = None,
                 deserialize_message: Optional[Callable[[bytes, IntEnum], Any]] = None,
                 checksum_size: int = 4,  # Default 4 bytes for CRC32
                 checksum_enabled: bool = False,
                 checksum_func: Optional[Callable[[bytes], bytes]] = None,
                 checksum_verify: Optional[Callable[[bytes, bytes], bool]] = None,
                 error_handler: Optional[Callable[[str], Tuple[Any, Dict[str, Any]]]] = None,
                 enable_performance_improvements: bool = True):
        self.message_type_enum = message_type_enum
        self.message_structures = message_structures
        self.header_format = header_format
        self.not_found_type = not_found_type if not_found_type is not None else \
            (1 << (8 * struct.calcsize(header_format))) - 1
        self.header_size = struct.calcsize(header_format)  # 2 bytes default
        self.max_payload_size = max_payload_size
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.write_timeout = write_timeout
        self.buffer_size = buffer_size
        self.validate_message = validate_message
        self.serialize_message = serialize_message
        self.deserialize_message = deserialize_message
        
        # Checksum configuration
        self.checksum_size = checksum_size
        self.checksum_enabled = checksum_enabled
        self.checksum_func = checksum_func
        self.checksum_verify = checksum_verify
        self.error_handler = error_handler
        self.transport_type = transport_type
        self.enable_performance_improvements = enable_performance_improvements

    def __post_init__(self):
        # Compute header size from format string
        self.header_size = struct.calcsize(self.header_format)
        
        # Validate enum class
        if not issubclass(self.message_type_enum, IntEnum):
            raise ValueError("message_type_enum must be a subclass of IntEnum")
            
        # Validate message structures
        for msg_type in self.message_type_enum:
            if msg_type not in self.message_structures:
                raise ValueError(f"Missing message structure for type {msg_type}")