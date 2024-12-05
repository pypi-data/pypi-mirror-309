import asyncio
import logging
from binary_protocol.client import BinaryClient
from shared_config import MessageType, config
from binary_protocol.protocol.messages import Message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True # Suppress other loggers
)

# Get the calculated NOT_FOUND value for this configuration
PROTOCOL_NOT_FOUND = Message.get_not_found_type(config.header_format)

async def main():
    client = BinaryClient(config)
    await client.connect('127.0.0.1', 8888)
    
    try:
        # Test 1: Send a chat message
        print("\n--- Testing Chat Message ---")
        await client.send_message(MessageType.CHAT, {
            "username": "Alice",
            "content": "Hello, server!"
        })
        msg_type, response = await client.receive_message()
        print(f"Chat response: {response}")

        # Test 2: Send sensor data
        print("\n--- Testing Sensor Data ---")
        await client.send_message(MessageType.SENSOR_DATA, {
            "sensor_1": 23.5,
            "sensor_2": 98.6,
            "sensor_3": 0.125,
            "sensor_4": -42.0
        })
        msg_type, response = await client.receive_message()
        print(f"Sensor response type: {msg_type}")

        # Test 3: Send a small file transfer
        print("\n--- Testing File Transfer ---")
        await client.send_message(MessageType.FILE_TRANSFER, {
            "username": "Alice",
            "filename": "test.txt",
            "data": b"Hello, World!"
        })
        msg_type, response = await client.receive_message()
        print(f"File transfer response type: {msg_type}")
        
        # Test 4: Send an unimplemented message type
        print("\n--- Testing Not Found Message ---")
        await client.send_message(34, {"username": "Alice", "content": "This won't work"})
        try:
            msg_type, response = await client.receive_message()
            print(f"Not found response type: {msg_type}")
        except Exception as e:
            print(f"Got expected error: {e}")
        
    finally:
        await client.disconnect()
        
    # Create a single-use client
    single_client = BinaryClient.create_single_use(config, '127.0.0.1', 8888)

    # Test 5: Send a single message and disconnect
    print("\n--- Testing Single Message ---")
    await single_client.send(MessageType.CHAT, {
        "username": "Alice",
        "content": "Hello, server!"
    })

    # Test 6: Send a single message with response
    print("\n--- Testing Single Message with Response ---")
    msg_type, response = await single_client.send_and_receive(MessageType.CHAT, {
        "username": "Alice",
        "content": "Hello, server!"
    })
    print(f"Single message response type: {msg_type}")

if __name__ == "__main__":
    asyncio.run(main())