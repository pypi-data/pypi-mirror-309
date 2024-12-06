from dataclasses import dataclass
from typing import List, Any, Type, Dict, Optional
import struct
import logging

@dataclass
class FieldDefinition:
    name: str
    field_type: Type
    fixed_length: Optional[int] = None
    format_string: Optional[str] = None  # For struct.pack/unpack

@dataclass
class FieldInfo:
    """Pre-calculated field information for faster serialization/deserialization"""
    name: str
    field_type: Type
    format_string: Optional[str] = None
    fixed_length: Optional[int] = None
    fixed_offset: Optional[int] = None
    size: Optional[int] = None

class MessageStructure:
    """Message structure definition with optional fields"""
    def __init__(self, fields: List[FieldDefinition] = None):
        self.fields = fields or []
        self._field_info = self._prepare_field_info()
        self._fixed_size = self._calculate_fixed_size()
        self._is_fixed_length = not any(f.field_type in (str, bytes) and not f.fixed_length for f in self.fields)
        self._is_empty = len(self.fields) == 0
    
    def _prepare_field_info(self) -> List[FieldInfo]:
        """Pre-calculate field information for optimization"""
        field_info = []
        current_offset = 0
        
        for field in self.fields:
            size = None
            fixed_offset = None
            
            if field.field_type in (int, float):
                size = struct.calcsize(field.format_string)
                fixed_offset = current_offset
                current_offset += size
            elif field.field_type in (str, bytes) and field.fixed_length:
                size = field.fixed_length
                fixed_offset = current_offset
                current_offset += size
                
            field_info.append(FieldInfo(
                name=field.name,
                field_type=field.field_type,
                format_string=field.format_string,
                fixed_length=field.fixed_length,
                fixed_offset=fixed_offset,
                size=size
            ))
            
        return field_info

    def _validate_fields(self):
        for field in self.fields:
            if field.field_type not in (str, int, float, bytes):
                raise ValueError(f"Unsupported field type: {field.field_type}")
            if field.field_type in (int, float) and not field.format_string:
                raise ValueError(f"Format string required for {field.field_type}")

    def serialize(self, data: Dict[str, Any]) -> bytes:
        """Serialize data according to the message structure"""
        if self._is_empty:
            return b''
        if self._is_fixed_length:
            return self._serialize_fixed(data)
        return self._serialize_variable(data)
            
    def _serialize_fixed(self, data: Dict[str, Any]) -> bytes:
        """Serialize fixed-length data"""
        result = bytearray(self._fixed_size)
        
        for info in self._field_info:
            value = data[info.name]
            if info.field_type in (int, float):
                struct.pack_into(info.format_string, result, info.fixed_offset, value)
            elif info.field_type in (str, bytes):
                encoded = value.encode('utf-8') if info.field_type == str else value
                result[info.fixed_offset:info.fixed_offset + info.size] = encoded.ljust(info.size, b'\0')
                
        return bytes(result)
        
    def _serialize_variable(self, data: Dict[str, Any]) -> bytes:
        """Serialize variable-length data"""
        result = bytearray()
        
        for field in self.fields:
            value = data[field.name]
            
            if field.field_type in (int, float):
                result.extend(struct.pack(field.format_string, value))
            elif field.field_type == str:
                encoded = value.encode('utf-8')
                result.extend(struct.pack('>I', len(encoded)))
                result.extend(encoded)
            elif field.field_type == bytes:
                result.extend(struct.pack('>I', len(value)))
                result.extend(value)
                
        return bytes(result)

    def deserialize(self, data: bytes) -> Dict[str, Any]:
        """Deserialize binary data into a dictionary"""
        if self._is_empty:
            return {}
        if self._is_fixed_length:
            return self._deserialize_fixed(data)
        return self._deserialize_variable(data)
        
    def _deserialize_fixed(self, data: bytes) -> Dict[str, Any]:
        """Deserialize fixed-length data"""
        result = {}
        for info in self._field_info:
            if info.field_type in (int, float):
                value = struct.unpack_from(info.format_string, data, info.fixed_offset)[0]
            elif info.field_type in (str, bytes):
                raw = data[info.fixed_offset:info.fixed_offset + info.size]
                if info.field_type == str:
                    value = raw.split(b'\0', 1)[0].decode('utf-8')
                else:
                    value = raw
            result[info.name] = value
        return result
        
    def _deserialize_variable(self, data: bytes) -> Dict[str, Any]:
        """Deserialize variable-length data"""
        result = {}
        offset = 0
        
        for field in self.fields:
            if field.field_type in (int, float):
                size = struct.calcsize(field.format_string)
                value = struct.unpack(field.format_string, data[offset:offset + size])[0]
                offset += size
            elif field.field_type in (str, bytes):
                length = struct.unpack('>I', data[offset:offset + 4])[0]
                offset += 4
                value = data[offset:offset + length]
                if field.field_type == str:
                    value = value.decode('utf-8')
                offset += length
            result[field.name] = value
            
        return result

    def has_variable_length_fields(self) -> bool:
        return not self._is_fixed_length

    def get_fixed_size(self) -> int:
        return self._fixed_size
    
    def _calculate_fixed_size(self) -> int:
        """Calculate total size of all fixed-length fields"""
        size = 0
        for info in self._field_info:
            if info.size is not None:
                size += info.size
        return size

    def debug_serialize(self, data: Dict[str, Any]) -> bytes:
        """Debug version of serialize that logs each step"""
        result = bytearray()
        
        for field in self.fields:
            value = data[field.name]
            logging.debug(f"Serializing field {field.name}: {value}")
            
            if field.field_type == str:
                encoded = value.encode('utf-8')
                if field.fixed_length:
                    if len(encoded) > field.fixed_length:
                        raise ValueError(f"String too long for field {field.name}")
                    encoded = encoded.ljust(field.fixed_length, b'\0')
                    result.extend(encoded)
                    logging.debug(f"Fixed length string: {encoded.hex()}")
                else:
                    # Add length prefix for variable length strings
                    length_prefix = struct.pack('>I', len(encoded))
                    result.extend(length_prefix)
                    result.extend(encoded)
                    logging.debug(f"Variable length string: {length_prefix.hex()} + {encoded.hex()}")
            
            elif field.field_type in (int, float):
                packed = struct.pack(field.format_string, value)
                result.extend(packed)
                logging.debug(f"Numeric value: {packed.hex()}")
            
            elif field.field_type == bytes:
                if field.fixed_length:
                    if len(value) > field.fixed_length:
                        raise ValueError(f"Bytes too long for field {field.name}")
                    padded = value.ljust(field.fixed_length, b'\0')
                    result.extend(padded)
                    logging.debug(f"Fixed length bytes: {padded.hex()}")
                else:
                    length_prefix = struct.pack('>I', len(value))
                    result.extend(length_prefix)
                    result.extend(value)
                    logging.debug(f"Variable length bytes: {length_prefix.hex()} + {value.hex()}")
        
        return bytes(result)

    def serialize_fixed(self, data: Dict[str, Any], header: bytes) -> bytes:
        """Fast path for fixed-length messages combining header and payload"""
        if not self._is_fixed_length:
            raise ValueError("serialize_fixed only supports fixed-length messages")
        
        # Pre-allocate exact size buffer
        total_size = len(header) + self._fixed_size
        result = bytearray(total_size)
        
        # Copy header
        result[:len(header)] = header
        
        # Direct struct packing for numeric fields
        for info in self._field_info:
            value = data[info.name]
            if info.field_type in (int, float):
                struct.pack_into(info.format_string, result, len(header) + info.fixed_offset, value)
            elif info.field_type in (str, bytes):
                encoded = value.encode('utf-8') if info.field_type == str else value
                result[len(header) + info.fixed_offset:len(header) + info.fixed_offset + info.size] = \
                    encoded.ljust(info.size, b'\0')
                
        return bytes(result)