import asyncio
import logging
from typing import Optional, Any, Dict, Tuple
from ..protocol.messages import Message
from ..protocol.exceptions import ConnectionError, ProtocolError, PayloadError, MessageValidationError, MessageStructureNotFoundError
from ..protocol.config import ProtocolConfig
import struct

logger = logging.getLogger(__name__)

class BinaryClient:
    """
    Asynchronous client implementation for the binary protocol
    
    Attributes:
        config: Protocol configuration
        reader: Async stream reader
        writer: Async stream writer
    """
    
    def __init__(self, config: ProtocolConfig):
        self.config = config
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected and self.writer is not None and not self.writer.is_closing()

    async def connect(self, host: str, port: int) -> None:
        """Establish connection to the server"""
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.config.connect_timeout
            )
            self._connected = True
            logger.info(f"Connected to {host}:{port}")
        except (asyncio.TimeoutError, OSError) as e:
            raise ConnectionError(f"Failed to connect to {host}:{port} - {str(e)}")

    async def disconnect(self) -> None:
        """Close the connection gracefully"""
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            finally:
                self._connected = False
                self.writer = None
                self.reader = None
                logger.info("Disconnected from server")

    async def send_message(self, msg_type: Any, data: Dict[str, Any]) -> None:
        """Optimized message sending"""
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        try:
            message = Message.create(self.config, msg_type, data)
            message_bytes = message.to_bytes(self.config)
            logger.debug(f"Sending message type {msg_type}, size: {len(message_bytes)}")
            
            self.writer.write(message_bytes)
            await self.writer.drain()
        except Exception as e:
            logger.error(f"Unexpected error while sending message: {str(e)}")
            await self.disconnect()
            raise ProtocolError(f"Failed to send message: {str(e)}")

    async def receive_message(self) -> Tuple[Any, Dict[str, Any]]:
        """Receive and parse a message"""
        try:
            header = await asyncio.wait_for(
                self.reader.readexactly(self.config.header_size),
                timeout=self.config.read_timeout
            )
            
            msg_type_val = struct.unpack(self.config.header_format, header)[0]
            
            # Check if it's a NOT_FOUND response using configured value
            if msg_type_val == self.config.not_found_type:
                return msg_type_val, {}
            
            # Try to convert to enum type
            try:
                msg_type = self.config.message_type_enum(msg_type_val)
            except ValueError:
                # Unknown message type
                return msg_type_val, {}
            
            structure = self.config.message_structures.get(msg_type)
            if not structure:
                raise ValueError(f"No message structure defined for type {msg_type}")
            
            # Read payload based on message type
            if structure.has_variable_length_fields():
                # Read length prefix
                length_bytes = await asyncio.wait_for(
                    self.reader.readexactly(4),
                    timeout=self.config.read_timeout
                )
                total_length = struct.unpack(">I", length_bytes)[0]
                
                # Read payload
                payload = await asyncio.wait_for(
                    self.reader.readexactly(total_length),
                    timeout=self.config.read_timeout
                )
                message_bytes = header + length_bytes + payload
            else:
                # Fixed length message
                fixed_size = structure.get_fixed_size()
                payload = await asyncio.wait_for(
                    self.reader.readexactly(fixed_size),
                    timeout=self.config.read_timeout
                )
                message_bytes = header + payload
            
            # Read and verify checksum if enabled
            if self.config.checksum_enabled:
                checksum = await asyncio.wait_for(
                    self.reader.readexactly(self.config.checksum_size),
                    timeout=self.config.read_timeout
                )
                if not self.config.checksum_verify(message_bytes, checksum):
                    raise ValueError("Checksum verification failed")
            
            # Deserialize payload
            data = structure.deserialize(payload)
            return msg_type, data
            
        except Exception as e:
            await self.disconnect()
            raise ProtocolError(f"Failed to receive message: {str(e)}")

    @classmethod
    async def send_single(cls, config: ProtocolConfig, host: str, port: int, 
                           msg_type: Any, data: Dict[str, Any]) -> None:
        """Send a single message and disconnect immediately"""
        client = cls(config)
        try:
            await client.connect(host, port)
            await client.send_message(msg_type, data)
        finally:
            await client.disconnect()

    @classmethod
    async def send_and_receive_single(cls, config: ProtocolConfig, host: str, port: int,
                                      msg_type: Any, data: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Send a single message, wait for response, and disconnect"""
        client = cls(config)
        try:
            await client.connect(host, port)
            await client.send_message(msg_type, data)
            return await client.receive_message()
        finally:
            await client.disconnect()

    @classmethod
    def create_single_use(cls, config: ProtocolConfig, host: str, port: int) -> 'SingleUseClient':
        """Create a pre-configured client for single-use operations"""
        return SingleUseClient(config, host, port)

class SingleUseClient:
    """Wrapper for single-use operations with pre-configured connection details"""
    def __init__(self, config: ProtocolConfig, host: str, port: int):
        self.config = config
        self.host = host
        self.port = port

    async def send(self, msg_type: Any, data: Dict[str, Any]) -> None:
        """Send a single message and disconnect"""
        await BinaryClient.send_single(self.config, self.host, self.port, msg_type, data)

    async def send_and_receive(self, msg_type: Any, data: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Send a single message, wait for response, and disconnect"""
        return await BinaryClient.send_and_receive_single(self.config, self.host, self.port, msg_type, data)