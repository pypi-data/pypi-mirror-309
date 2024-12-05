"""
Core message definitions and serialization logic for the binary protocol.
"""

from dataclasses import dataclass
import struct
from typing import Optional, Any, Dict
from .config import ProtocolConfig
import logging
from ..protocol.exceptions import PayloadError, MessageStructureNotFoundError

logger = logging.getLogger(__name__)

class Message:
    """
    Base message class representing the protocol's message structure
    
    Attributes:
        msg_type: Type identifier for the message
        payload: Raw binary data content
    """
    __slots__ = ('msg_type', 'payload', '_original_data')
    
    @classmethod
    def get_not_found_type(cls, header_format: str) -> int:
        """Calculate maximum possible value for the given header format"""
        not_found_type = (1 << (8 * struct.calcsize(header_format))) - 1
        logger.debug(f"Not found type: {not_found_type}")
        return not_found_type
    
    def __init__(self, msg_type: Any, payload: bytes = b'', original_data: Optional[Dict[str, Any]] = None):
        self.msg_type = msg_type
        self.payload = payload
        self._original_data = original_data
    
    @classmethod
    def create(cls, config: ProtocolConfig, msg_type: Any, data: Dict[str, Any]) -> 'Message':
        """Create a message using the provided configuration"""
        try:
            if not isinstance(msg_type, config.message_type_enum):
                # Just pass through the original type value
                return cls(msg_type, b'', data)
            
            structure = config.message_structures.get(msg_type)
            if not structure:
                logger.debug(f"No structure defined for message type {msg_type}")
                raise MessageStructureNotFoundError(f"No message structure defined for type {msg_type}")
            
            try:
                payload = structure.serialize(data)
                return cls(msg_type, payload, data)
            except Exception as e:
                logger.error(f"Message creation failed: {str(e)}")
                raise PayloadError(f"Failed to serialize message: {str(e)}")
        except Exception as e:
            logger.error(f"Message creation failed: {str(e)}")
            raise e
    
    def to_bytes(self, config: ProtocolConfig) -> bytes:
        """Convert message to bytes for transmission"""
        try:
            # Handle NOT_FOUND type specially
            if self.msg_type == self.get_not_found_type(config.header_format):
                return struct.pack(config.header_format, self.get_not_found_type(config.header_format))

            # Try to get message type value
            try:
                msg_type_val = int(self.msg_type)
            except (TypeError, ValueError):
                # If conversion fails, use original value
                msg_type_val = self.msg_type
            
            header = struct.pack(config.header_format, msg_type_val)
            
            # Get message structure if available
            structure = config.message_structures.get(self.msg_type)
            if not structure:
                # For undefined types, just send header with empty payload
                return header + self.payload

            # Fast path for fixed-length messages without checksum
            if not config.checksum_enabled and not structure.has_variable_length_fields():
                return header + self.payload

            # Variable length messages need length prefix
            if structure.has_variable_length_fields():
                length_prefix = struct.pack(">I", len(self.payload))
                message_bytes = header + length_prefix + self.payload
            else:
                message_bytes = header + self.payload
            
            # Only add checksum if explicitly enabled
            if config.checksum_enabled and config.checksum_func:
                message_bytes += config.checksum_func(message_bytes)
            
            return message_bytes
        except Exception as e:
            logger.error(f"Message serialization failed: {str(e)}")
            raise
    
    def deserialize(self, config: ProtocolConfig) -> Dict[str, Any]:
        """Deserialize payload into dictionary using message structure"""
        if self._original_data is not None:
            return self._original_data
            
        structure = config.message_structures.get(self.msg_type)
        if not structure:
            raise ValueError(f"No message structure defined for type {self.msg_type}")
            
        return structure.deserialize(self.payload)
    
    def validate(self, config: ProtocolConfig) -> None:
        """Validate message using configuration rules"""
        if not isinstance(self.msg_type, config.message_type_enum):
            raise ValueError(f"Invalid message type for {config.message_type_enum.__name__}")
            
        if len(self.payload) > config.max_payload_size:
            raise ValueError(f"Payload size exceeds maximum: {len(self.payload)} > {config.max_payload_size}")
            
        if config.validate_message:
            # Use original message for validation if available
            message_to_validate = self._original_data or self
            if not config.validate_message(message_to_validate):
                raise ValueError("Message failed custom validation")
    
    @classmethod
    def from_bytes(cls, data: bytes, config: ProtocolConfig) -> 'Message':
        """Create a message from bytes using the provided configuration"""
        if len(data) < config.header_size:
            raise ValueError(f"Data too short for header: {len(data)} < {config.header_size}")
        
        # Fast path when checksums are disabled
        if not config.checksum_enabled:
            msg_type_val = struct.unpack(config.header_format, data[:config.header_size])[0]
            try:
                msg_type = config.message_type_enum(msg_type_val)
            except ValueError:
                raise ValueError(f"Invalid message type: {msg_type_val}")
            
            structure = config.message_structures.get(msg_type)
            if not structure:
                raise ValueError(f"No message structure defined for type {msg_type}")
            
            if not structure.has_variable_length_fields():
                # Fast path for fixed-length messages
                payload = data[config.header_size:]
                return cls(msg_type, payload)
            
        # Original path for checksum verification or variable length messages
        # Extract and verify checksum if enabled
        if config.checksum_enabled:
            if len(data) < config.checksum_size:
                raise ValueError("Data too short for checksum")
            
            message_bytes = data[:-config.checksum_size]
            actual_checksum = data[-config.checksum_size:]
            
            if config.checksum_verify:
                if not config.checksum_verify(message_bytes, actual_checksum):
                    raise ValueError("Checksum verification failed")
            
            data = message_bytes
        
        # Unpack 2-byte message type
        msg_type_val = struct.unpack(config.header_format, data[:config.header_size])[0]
        
        try:
            msg_type = config.message_type_enum(msg_type_val)
        except ValueError:
            raise ValueError(f"Invalid message type: {msg_type_val}")

        structure = config.message_structures.get(msg_type)
        if not structure:
            raise ValueError(f"No message structure defined for type {msg_type}")

        data = data[config.header_size:]  # Remove header
        
        # For variable length messages, read 4-byte length prefix
        if structure.has_variable_length_fields():
            if len(data) < 4:
                raise ValueError("Data too short for payload length")
            payload_length = struct.unpack(">I", data[:4])[0]
            payload = data[4:]
            if len(payload) != payload_length:
                raise ValueError(f"Incomplete payload: expected {payload_length} bytes, got {len(payload)}")
        else:
            # For fixed length messages, use the structure's fixed size
            fixed_size = structure.get_fixed_size()
            payload = data
            if len(payload) != fixed_size:
                raise ValueError(f"Invalid payload length for fixed-size message: expected {fixed_size}, got {len(payload)}")
        
        return cls(msg_type, payload) 