import asyncio
import logging
from typing import Optional, Dict, Any, Tuple

from binary_protocol.server import BinaryServer
from binary_protocol.protocol.messages import Message
from shared_config import MessageType, config

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True # Suppress other loggers
)

logger = logging.getLogger(__name__)

# Get the calculated NOT_FOUND value for this configuration
PROTOCOL_NOT_FOUND = Message.get_not_found_type(config.header_format)

def success_status():
    """Return a status OK message with no payload"""
    return MessageType.STATUS_OK, None
    
def error_status():
    """Return a status ERROR message with no payload"""
    return MessageType.STATUS_ERROR, None
    
def not_implemented_status():
    """Return a status NOT IMPLEMENTED message with no payload"""
    return MessageType.STATUS_NOT_IMPLEMENTED, None

def invalid_request_status():
    """Return a status INVALID REQUEST message with no payload"""
    return MessageType.STATUS_INVALID_REQUEST, None
    
def invalid_data_status():
    """Return a status INVALID DATA message with no payload"""
    return MessageType.STATUS_INVALID_DATA, None
    
def echo_chat(data: Dict[str, Any]) -> Optional[Tuple[MessageType, Dict[str, Any]]]:
    """Echo back chat messages with server prefix"""
    return MessageType.CHAT, {
        "username": "Server",
        "content": f"Echo: {data['content']}"
    }

async def handle_chat(msg_type: MessageType, data: Dict[str, Any]) -> Optional[Tuple[MessageType, Dict[str, Any]]]:
    """Handle chat messages with custom logic"""
    print(f"Chat from {data['username']}: {data['content']}")
    return echo_chat(data)

async def handle_file_transfer(msg_type: MessageType, data: Dict[str, Any]) -> Optional[Tuple[MessageType, Dict[str, Any]]]:
    """Handle file transfer messages"""
    print(f"File transfer from {data['username']}: {data['filename']} ({len(data['data'])} bytes)")
    return success_status()
    
async def handle_sensor_data(msg_type: MessageType, data: Dict[str, Any]) -> Optional[Tuple[MessageType, Dict[str, Any]]]:
    """Handle sensor data messages"""
    print(f"Sensor data: {data['sensor_1']} - {data['sensor_2']} - {data['sensor_3']} - {data['sensor_4']}")
    return success_status()

async def handle_not_found(msg_type: Any, data: Dict[str, Any]) -> Optional[Tuple[Any, Dict[str, Any]]]:
    """Handle not found messages"""
    print(f"Not found: {msg_type}")
    # Use either the configured value or protocol's calculated value
    return config.not_found_type or PROTOCOL_NOT_FOUND, None

async def handle_invalid_request(msg_type: MessageType, data: Dict[str, Any]) -> Optional[Tuple[MessageType, Dict[str, Any]]]:
    """Handle invalid request messages"""
    print(f"Invalid request: {msg_type}")
    if msg_type == PROTOCOL_NOT_FOUND:
        print("Warning: Received protocol-level NOT_FOUND type")
    return invalid_request_status()

async def main():
    server = BinaryServer(config)
    
    logger.info(f"Protocol NOT_FOUND value: 0x{PROTOCOL_NOT_FOUND:X}")
    logger.info(f"Config NOT_FOUND value: {config.not_found_type}")
    
    # Register default handler
    server.register_default_handler(handle_not_found)
    
    # Register handlers for different message types
    server.register_handler(MessageType.CHAT, handle_chat)
    server.register_handler(MessageType.FILE_TRANSFER, handle_file_transfer)
    server.register_handler(MessageType.SENSOR_DATA, handle_sensor_data)
    
    # Optional: Register handler for protocol-level NOT_FOUND if needed
    if PROTOCOL_NOT_FOUND not in MessageType.__members__.values():
        logger.warning(f"Note: Protocol NOT_FOUND (0x{PROTOCOL_NOT_FOUND:X}) is not in MessageType enum")
    
    # Register handlers for status messages
    server.register_handler(MessageType.STATUS_NOT_IMPLEMENTED, handle_invalid_request)
    server.register_handler(MessageType.STATUS_INVALID_REQUEST, handle_invalid_request)
    server.register_handler(MessageType.STATUS_INVALID_DATA, handle_invalid_request)
    
    try:
        logger.info("Starting chat server on localhost:8888...")
        await server.start('127.0.0.1', 8888)
    except KeyboardInterrupt:
        logger.info("\nShutting down server...")
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())