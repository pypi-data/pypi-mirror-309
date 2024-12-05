import asyncio
import logging
from typing import Optional, Any, Dict, Tuple
from ..protocol.messages import Message
from ..protocol.exceptions import ConnectionError, ProtocolError, PayloadError, MessageValidationError, MessageStructureNotFoundError
from ..protocol.config import ProtocolConfig, TransportType
import struct
import socket

logger = logging.getLogger(__name__)

class BinaryClient:
    """Unified client implementation supporting both TCP and UDP transports"""
    
    def __init__(self, config: ProtocolConfig):
        self.config = config
        self._connected = False
        
        # TCP-specific attributes
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        
        # UDP-specific attributes
        self.sock: Optional[socket.socket] = None
        self.addr: Optional[Tuple[str, int]] = None

    @property
    def connected(self) -> bool:
        if self.config.transport_type == TransportType.TCP:
            return self._connected and self.writer is not None and not self.writer.is_closing()
        else:  # UDP
            return self._connected and self.sock is not None

    async def connect(self, host: str, port: int) -> None:
        """Unified connection method for both TCP and UDP"""
        try:
            if self.config.transport_type == TransportType.TCP:
                self.reader, self.writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port),
                    timeout=self.config.connect_timeout
                )
            else:  # UDP
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.addr = (host, port)
                
            self._connected = True
            logger.info(f"Connected to {host}:{port} using {self.config.transport_type.name}")
            
        except (asyncio.TimeoutError, OSError) as e:
            raise ConnectionError(f"Failed to connect to {host}:{port} - {str(e)}")

    async def disconnect(self) -> None:
        """Unified disconnection method"""
        try:
            if self.config.transport_type == TransportType.TCP:
                if self.writer:
                    self.writer.close()
                    await self.writer.wait_closed()
            else:  # UDP
                if self.sock:
                    self.sock.close()
        finally:
            self._connected = False
            self.writer = self.reader = self.sock = self.addr = None
            logger.info("Disconnected from server")

    async def send_message(self, msg_type: Any, data: Dict[str, Any]) -> None:
        """Unified message sending for both transports"""
        if not self.connected:
            raise ConnectionError("Not connected to server")
            
        try:
            message = Message.create(self.config, msg_type, data)
            message_bytes = message.to_bytes(self.config)
            
            if self.config.transport_type == TransportType.TCP:
                self.writer.write(message_bytes)
                await self.writer.drain()
            else:  # UDP
                if len(message_bytes) > 65507:  # UDP size limit
                    raise PayloadError("UDP message too large")
                self.sock.sendto(message_bytes, self.addr)
                
            logger.debug(f"Sent {len(message_bytes)} bytes via {self.config.transport_type.name}")
            
        except Exception as e:
            logger.error(f"Send failed: {str(e)}")
            await self.disconnect()
            raise ProtocolError(f"Failed to send message: {str(e)}")

    async def receive_message(self) -> Tuple[Any, Dict[str, Any]]:
        """Unified message receiving for both transports"""
        if not self.connected:
            raise ConnectionError("Not connected to server")
        
        try:
            if self.config.transport_type == TransportType.TCP:
                # TCP receiving logic
                header = await asyncio.wait_for(
                    self.reader.readexactly(self.config.header_size),
                    timeout=self.config.read_timeout
                )
                
                msg_type_val = struct.unpack(self.config.header_format, header)[0]
                
                # Check if it's a NOT_FOUND response
                if msg_type_val == self.config.not_found_type:
                    return msg_type_val, {}
                
                # Try to convert to enum type
                try:
                    msg_type = self.config.message_type_enum(msg_type_val)
                except ValueError:
                    return msg_type_val, {}
                
                structure = self.config.message_structures.get(msg_type)
                if not structure:
                    raise ValueError(f"No message structure defined for type {msg_type}")
                
                # Read payload based on message type
                if structure.has_variable_length_fields():
                    length_bytes = await asyncio.wait_for(
                        self.reader.readexactly(4),
                        timeout=self.config.read_timeout
                    )
                    total_length = struct.unpack(">I", length_bytes)[0]
                    payload = await asyncio.wait_for(
                        self.reader.readexactly(total_length),
                        timeout=self.config.read_timeout
                    )
                    message_bytes = header + length_bytes + payload
                else:
                    fixed_size = structure.get_fixed_size()
                    payload = await asyncio.wait_for(
                        self.reader.readexactly(fixed_size),
                        timeout=self.config.read_timeout
                    )
                    message_bytes = header + payload
                    
            else:  # UDP
                # UDP receiving logic
                loop = asyncio.get_event_loop()
                try:
                    self.sock.settimeout(self.config.read_timeout)
                    data, _ = await loop.run_in_executor(None, 
                        lambda: self.sock.recvfrom(65507))  # Max UDP size
                except socket.timeout:
                    raise TimeoutError("UDP receive timed out")
                    
                # Parse the complete message
                message = Message.from_bytes(data, self.config)
                return message.msg_type, message.deserialize(self.config)
                
            # Handle checksum for TCP (UDP checksums handled in Message.from_bytes)
            if self.config.transport_type == TransportType.TCP and self.config.checksum_enabled:
                checksum = await asyncio.wait_for(
                    self.reader.readexactly(self.config.checksum_size),
                    timeout=self.config.read_timeout
                )
                if not self.config.checksum_verify(message_bytes, checksum):
                    raise ValueError("Checksum verification failed")
                
            # For TCP, deserialize the payload
            if self.config.transport_type == TransportType.TCP:
                data = structure.deserialize(payload)
                return msg_type, data
                
        except Exception as e:
            logger.error(f"Receive failed: {str(e)}")
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