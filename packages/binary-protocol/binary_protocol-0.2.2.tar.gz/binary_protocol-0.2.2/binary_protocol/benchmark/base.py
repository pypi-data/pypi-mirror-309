from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, TypeVar, Generic, Type
from copy import deepcopy
from ..protocol.config import ProtocolConfig
import time
import logging
import asyncio
import random

logger = logging.getLogger(__name__)

class MessageProtocol(Protocol):
    """Protocol defining required message interface"""
    async def send_message(self, message_type: Any, payload: Dict[str, Any]) -> None:
        ...
    
    async def receive_message(self) -> tuple[Any, Dict[str, Any]]:
        ...
        
    async def connect(self, host: str, port: int) -> None:
        ...
        
    async def disconnect(self) -> None:
        ...

T = TypeVar('T', bound=MessageProtocol)

@dataclass
class BenchmarkConfig:
    """Configuration for benchmark runs"""
    iterations: int = 1000
    warmup_iterations: int = 20
    batch_size: int = 100
    duration: float = 10.0
    host: str = "127.0.0.1"
    port: int = 8888
    message_size: int = 1024
    message_type: Any = None
    custom_config: Dict[str, Any] = None
    validate_response: Optional[callable] = None

    def copy(self) -> 'BenchmarkConfig':
        """Create a deep copy of the configuration"""
        return BenchmarkConfig(
            iterations=self.iterations,
            warmup_iterations=self.warmup_iterations,
            batch_size=self.batch_size,
            duration=self.duration,
            host=self.host,
            port=self.port,
            message_size=self.message_size,
            message_type=self.message_type,
            custom_config=deepcopy(self.custom_config) if self.custom_config else None,
            validate_response=self.validate_response
        )

@dataclass
class BenchmarkResult:
    """Standard benchmark result structure"""
    name: str
    throughput: float  # MB/s
    latency: float    # ms
    messages_per_sec: float
    message_size: int
    total_messages: int
    total_bytes: int
    errors: int
    successful_messages: int
    duration: float
    custom_metrics: Dict[str, Any] = None

class BaseBenchmark(Generic[T], ABC):
    """Abstract base class for all benchmarks"""
    
    def __init__(self, 
                 client_class: Type[T], 
                 benchmark_config: BenchmarkConfig, 
                 protocol_config: ProtocolConfig):
        self.client_class = client_class
        self.config = benchmark_config
        self.protocol_config = protocol_config
        self.client: Optional[T] = None
        self.max_retries = 3
        
    async def __aenter__(self):
        await self.setup()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.teardown()
        
    async def get_client(self) -> T:
        """Get or create a client connection with retry logic"""
        if self.client is None:
            self.client = self.client_class(self.protocol_config)
            await self.client.connect(self.config.host, self.config.port)
        return self.client
        
    async def send_message(self, message_type: Any, payload: Dict[str, Any]) -> bool:
        """Send a message with retry logic"""
        for retry in range(self.max_retries):
            try:
                client = await self.get_client()
                await client.send_message(message_type, payload)
                return True
            except Exception as e:
                if retry == self.max_retries - 1:
                    logger.error(f"Failed to send message after {self.max_retries} attempts: {str(e)}")
                    return False
                await asyncio.sleep(random.uniform(0.1, 0.5))
                self.client = None
                continue
        
    async def receive_message(self) -> tuple[Any, Dict[str, Any]]:
        """Receive a message using the client"""
        client = await self.get_client()
        return await client.receive_message()
        
    @abstractmethod
    async def create_message(self) -> Dict[str, Any]:
        """Create a message for the benchmark
        
        Returns:
            Dict containing the message payload. Should handle custom message formats
            defined in config.custom_config['message_format'] if present.
        """
        pass
        
    async def validate_response(self, response: tuple[Any, Dict[str, Any]]) -> bool:
        """Validate the response from the server"""
        if not await self._validate_base_response(response):
            return False
        
        # Use custom validation if provided
        if self.config.validate_response:
            try:
                return self.config.validate_response(response)
            except Exception as e:
                logger.error(f"Custom validation failed: {str(e)}")
                return False
            
        return True
        
    async def _validate_base_response(self, response: tuple[Any, Dict[str, Any]]) -> bool:
        """Base validation logic shared by all benchmarks"""
        msg_type, payload = response
        
        if not isinstance(payload, dict):
            logger.error(f"Invalid payload format: {payload}")
            return False
        
        return True
        
    async def setup(self) -> None:
        """Setup benchmark environment"""
        await self.get_client()
        
    async def teardown(self) -> None:
        """Cleanup benchmark environment"""
        if self.client:
            await self.client.disconnect()
            self.client = None
            
    async def warmup(self) -> None:
        """Perform warmup iterations"""
        if self.config.warmup_iterations <= 0:
            return
        
        message = await self.create_message()
        if message is None:
            logger.warning("Warmup skipped - no message created")
            return
        
        for _ in range(self.config.warmup_iterations):
            try:
                await self.client.send_message(self.config.message_type, message)
                await self.client.receive_message()
            except Exception as e:
                logger.warning(f"Warmup iteration failed: {str(e)}")
                continue
        
    async def run(self) -> BenchmarkResult:
        total_messages = 0
        successful_messages = 0
        errors = 0
        total_bytes = 0
        
        async with self:  # Use context manager for connection handling
            start_time = time.time()
            await self.warmup()
            
            for _ in range(self.config.iterations):
                try:
                    message = await self.create_message()
                    # Calculate actual wire size including protocol overhead
                    payload_size = len(message['data']) if isinstance(message.get('data'), (str, bytes)) else 8
                    wire_size = 2  # Header size
                    if hasattr(self, 'is_variable_length') and self.is_variable_length:
                        wire_size += 4  # Length prefix
                        wire_size += 4  # Field length prefix
                    wire_size += payload_size
                    
                    total_bytes += wire_size
                    
                    await self.client.send_message(self.config.message_type, message)
                    total_messages += 1
                    
                    response = await self.client.receive_message()
                    if await self.validate_response(response):
                        successful_messages += 1
                    else:
                        errors += 1
                except Exception as e:
                    errors += 1
                    logging.error(f"Error during benchmark: {str(e)}")
                    
        duration = time.time() - start_time
        
        return BenchmarkResult(
            name=self.__class__.__name__,
            throughput=(total_bytes / duration) / (1024 * 1024),
            latency=(duration / total_messages * 1000) if total_messages > 0 else 0,
            messages_per_sec=total_messages / duration,
            message_size=total_bytes // total_messages if total_messages > 0 else 0,
            total_messages=total_messages,
            total_bytes=total_bytes,
            errors=errors,
            successful_messages=successful_messages,
            duration=duration,
            custom_metrics={}
        )