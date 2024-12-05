"""
Asynchronous server implementation for the binary protocol.
"""

import asyncio
import logging
import struct
from typing import Optional, Dict, Callable, Awaitable, Any, Tuple
from ..protocol.messages import Message
from ..protocol.exceptions import ProtocolError, PayloadError, MessageStructureNotFoundError, MessageValidationError
from ..protocol.config import ProtocolConfig

logger = logging.getLogger(__name__)

MessageHandler = Callable[[Any, Dict[str, Any]], Awaitable[Optional[Tuple[Any, Dict[str, Any]]]]]

class BinaryServer:
    """
    Asynchronous server implementation for handling binary protocol connections
    """
    
    def __init__(self, config: ProtocolConfig):
        self.config = config
        self.handlers: Dict[Any, MessageHandler] = {}
        self._server: Optional[asyncio.Server] = None
        self.default_handler = self._default_not_found_handler
        
    def register_handler(self, msg_type: Any, handler: MessageHandler) -> None:
        """Register a message handler for a specific message type"""
        if not isinstance(msg_type, self.config.message_type_enum):
            raise ValueError(f"Message type must be an instance of {self.config.message_type_enum.__name__}")
        self.handlers[msg_type] = handler
        
    def register_default_handler(self, handler: MessageHandler) -> None:
        """Register a default handler for unhandled message types"""
        self.default_handler = handler
        
    async def start(self, host: str, port: int) -> None:
        """Start the server"""
        try:
            self._server = await asyncio.start_server(
                self._handle_client,
                host,
                port,
                backlog=100
            )
            addr = self._server.sockets[0].getsockname()
            logger.info(f'Server started on {addr[0]}:{addr[1]}')
            
            async with self._server:
                await self._server.serve_forever()
        except Exception as e:
            logger.error(f"Failed to start server: {str(e)}")
            raise
        
    async def stop(self) -> None:
        """Stop the server gracefully"""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
            logger.info("Server stopped")
        
    async def _default_not_found_handler(self, msg_type: Any, data: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        """Default handler that returns empty response with configured NOT_FOUND type"""
        return (self.config.not_found_type, {})
        
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle individual client connections"""
        peer = writer.get_extra_info('peername')
        logger.debug(f"New connection from {peer}")
        
        try:
            while True:
                try:
                    # Read header first
                    header = await reader.readexactly(self.config.header_size)
                    msg_type_val = struct.unpack(self.config.header_format, header)[0]
                    
                    # Skip processing if we receive a NOT_FOUND type
                    if msg_type_val == self.config.not_found_type:
                        logger.debug(f"Received NOT_FOUND type from {peer}")
                        continue
                    
                    # Try to convert to enum type
                    try:
                        msg_type = self.config.message_type_enum(msg_type_val)
                    except (ValueError, AttributeError):
                        logger.debug(f"Unknown message type {msg_type_val} from {peer}")
                        response = await self.default_handler(msg_type_val, {})
                        if response:
                            resp_type, resp_data = response
                            resp_message = Message.create(self.config, resp_type, resp_data)
                            writer.write(resp_message.to_bytes(self.config))
                            await writer.drain()
                        continue

                    structure = self.config.message_structures.get(msg_type)
                    if not structure:
                        logger.debug(f"No structure for message type {msg_type} from {peer}")
                        response = await self.default_handler(msg_type, {})
                        if response:
                            resp_type, resp_data = response
                            resp_message = Message.create(self.config, resp_type, resp_data)
                            writer.write(resp_message.to_bytes(self.config))
                            await writer.drain()
                        continue
                    
                    # Fast path for fixed-length messages without checksum
                    if not self.config.checksum_enabled and not structure.has_variable_length_fields():
                        payload = await reader.readexactly(structure.get_fixed_size())
                        data = structure.deserialize(payload)
                        
                        # Handle message
                        handler = self.handlers.get(msg_type, self.default_handler)
                        if handler:
                            response = await handler(msg_type, data)
                            if response:
                                resp_type, resp_data = response
                                resp_message = Message.create(self.config, resp_type, resp_data)
                                resp_bytes = resp_message.to_bytes(self.config)
                                writer.write(resp_bytes)
                                await writer.drain()
                        continue

                    # Need to implement the variable length/checksum path here
                    if structure.has_variable_length_fields():
                        # Read length prefix
                        length_bytes = await reader.readexactly(4)
                        total_length = struct.unpack(">I", length_bytes)[0]
                        
                        # Read payload
                        payload = await reader.readexactly(total_length)
                    else:
                        # Fixed length message
                        payload = await reader.readexactly(structure.get_fixed_size())
                    
                    # Handle checksum if enabled
                    if self.config.checksum_enabled:
                        checksum = await reader.readexactly(self.config.checksum_size)
                        message_bytes = header + (length_bytes + payload if structure.has_variable_length_fields() else payload)
                        if not self.config.checksum_verify(message_bytes, checksum):
                            raise ValueError("Checksum verification failed")
                    
                    # Deserialize and handle message
                    data = structure.deserialize(payload)
                    handler = self.handlers.get(msg_type, self.default_handler)
                    if handler:
                        response = await handler(msg_type, data)
                        if response:
                            resp_type, resp_data = response
                            resp_message = Message.create(self.config, resp_type, resp_data)
                            resp_bytes = resp_message.to_bytes(self.config)
                            writer.write(resp_bytes)
                            await writer.drain()
                        
                except MessageStructureNotFoundError as e:
                    logger.warning(f"Message structure not found: {str(e)}")
                    continue
                except PayloadError as e:
                    logger.error(f"Payload error from {peer}: {str(e)}")
                    continue
                except MessageValidationError as e:
                    logger.error(f"Validation error from {peer}: {str(e)}")
                    continue
                except asyncio.IncompleteReadError:
                    logger.debug(f"Client {peer} disconnected gracefully")
                    break
                except ConnectionError as e:
                    logger.warning(f"Connection error with client {peer}: {str(e)}")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error handling client {peer}: {str(e)}")
                    break
                
        finally:
            writer.close()
            await writer.wait_closed()
            logger.debug(f"Connection closed for {peer}")