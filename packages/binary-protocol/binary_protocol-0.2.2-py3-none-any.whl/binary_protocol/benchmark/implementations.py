# benchmark/implementations.py
from typing import Dict, Any, Optional, Type, List, Tuple
import random
import time
import asyncio
import logging
from .base import BaseBenchmark, BenchmarkConfig, BenchmarkResult, T
from ..protocol.config import ProtocolConfig

logger = logging.getLogger(__name__)

class FixedSizeBenchmark(BaseBenchmark[T]):
    """Benchmark with fixed-size messages"""
    
    def __init__(self, client_class: Type[T], config: BenchmarkConfig, protocol_config: ProtocolConfig):
        super().__init__(client_class, config, protocol_config)
        self.default_message = config.custom_config.get('default_message', {}) if config.custom_config else {}
        
    async def create_message(self) -> Dict[str, Any]:
        if self.config.custom_config and 'message_format' in self.config.custom_config:
            # Use user-provided message format
            message = self.config.custom_config['message_format'].copy()
            # Allow for dynamic field updates if specified
            if 'dynamic_fields' in self.config.custom_config:
                for field, generator in self.config.custom_config['dynamic_fields'].items():
                    if field in message:
                        message[field] = generator()
            return message
        return self.default_message.copy()

class VariableSizeBenchmark(BaseBenchmark[T]):
    """Benchmark with variable size messages"""
    
    def __init__(self, client_class: Type[T], config: BenchmarkConfig, protocol_config: ProtocolConfig):
        super().__init__(client_class, config, protocol_config)
        self.default_message = config.custom_config.get('default_message', {}) if config.custom_config else {}
        
    async def create_message(self) -> Dict[str, Any]:
        if self.config.custom_config and 'message_format' in self.config.custom_config:
            base_message = self.config.custom_config['message_format'].copy()
            # Add variable size data field if not present
            if 'data' not in base_message:
                base_message['data'] = b'x' * self.config.message_size
            return base_message
            
        return {
            "data": b'x' * self.config.message_size,
        }

class RealisticBenchmark(BaseBenchmark[T]):
    """Multi-client realistic usage benchmark"""
    
    def __init__(self, client_class: Type[T], config: BenchmarkConfig, protocol_config: ProtocolConfig):
        super().__init__(client_class, config, protocol_config)
        logger.info("Initializing RealisticBenchmark")
        self.num_clients = config.custom_config.get('num_clients', 100)
        self.ramp_up_time = config.custom_config.get('ramp_up_time', 2.0)
        self.max_retries = config.custom_config.get('max_retries', 3)
        self.min_size = config.custom_config.get('min_size', 10)
        self.max_size = config.custom_config.get('max_size', 30)
        
        # Ensure duration is set
        if not config.duration:
            config.duration = 10.0
        self.duration = config.duration
        
        logger.debug(f"Configured with {self.num_clients} clients, duration={self.duration}s")
        
        # Ensure we have a default message format
        self.default_message = {
            "data": b'x' * self.min_size,
        }
        if config.custom_config and 'default_message' in config.custom_config:
            self.default_message.update(config.custom_config['default_message'])
    
    async def create_message(self) -> Dict[str, Any]:
        """Create a random message for realistic testing"""
        # Use default message as base
        message = self.default_message.copy()
        
        # Generate random data size between min and max
        size = random.randint(self.min_size, self.max_size)
        message['data'] = b'x' * size
        message['timestamp'] = time.time()
        
        # Apply any custom updates from config
        if self.config.custom_config and 'default_message' in self.config.custom_config:
            message.update(self.config.custom_config['default_message'])
        
        return message
        
    async def simulate_client(self, client_id: int) -> Dict[str, Any]:
        start_delay = (client_id / self.num_clients) * self.ramp_up_time
        await asyncio.sleep(start_delay)
        
        messages_sent = 0
        messages_received = 0
        errors = 0
        client = None
        
        logger.debug(f"Client {client_id} starting with delay {start_delay:.2f}s")
        
        try:
            # Create a new client instance for each simulated client
            client = self.client_class(self.protocol_config)
            await client.connect(self.config.host, self.config.port)
            start_time = time.time()
            logger.debug(f"Client {client_id} connected")
            
            while time.time() - start_time < self.duration:
                try:
                    message = await self.create_message()
                    message['client_id'] = client_id  # Add client ID to message
                    await client.send_message(self.config.message_type, message)
                    messages_sent += 1
                    
                    response = await asyncio.wait_for(
                        client.receive_message(), 
                        timeout=1.0
                    )
                    if await self.validate_response(response):
                        messages_received += 1
                        if messages_received % 100 == 0:
                            logger.debug(f"Client {client_id}: {messages_received} messages processed")
                except Exception as e:
                    errors += 1
                    logger.error(f"Client {client_id} message error: {str(e)}")
        except Exception as e:
            logger.error(f"Client {client_id} connection error: {str(e)}")
        finally:
            if client:
                try:
                    await client.disconnect()
                except:
                    pass
        
        logger.debug(f"Client {client_id} finished: sent={messages_sent}, received={messages_received}, errors={errors}")
        return {
            "sent": messages_sent,
            "received": messages_received,
            "errors": errors,
            "client_id": client_id
        }
        
    async def run(self) -> BenchmarkResult:
        """Run the multi-client benchmark"""
        logger.debug(f"Starting realistic benchmark with {self.num_clients} clients")
        
        start_time = time.time()
        
        # Create and run client simulation tasks
        tasks = [self.simulate_client(i) for i in range(self.num_clients)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        valid_results = [r for r in results if isinstance(r, dict)]
        failed_clients = len(results) - len(valid_results)
        if failed_clients > 0:
            logger.warning(f"{failed_clients} clients failed to complete")
        
        total_sent = sum(r['sent'] for r in valid_results)
        total_received = sum(r['received'] for r in valid_results)
        total_errors = sum(r['errors'] for r in valid_results)
        
        # Calculate average message size
        messages = [await self.create_message() for _ in range(min(10, total_sent))]
        total_size = sum(len(message['data']) for message in messages)
        avg_message_size = total_size // len(messages) if messages else 0
        
        logger.debug(f"Benchmark completed: {total_sent} messages sent, {total_received} received")
        
        duration = time.time() - start_time
        
        return BenchmarkResult(
            name="Realistic Multi-Client",
            throughput=(total_sent * avg_message_size / duration) / (1024 * 1024),
            latency=(duration / total_received * 1000) if total_received > 0 else 0,
            messages_per_sec=total_sent / duration,
            message_size=avg_message_size,
            total_messages=total_sent,
            total_bytes=total_sent * avg_message_size,
            errors=total_errors,
            successful_messages=total_received,
            duration=duration,
            custom_metrics={
                'successful_clients': len(valid_results),
                'success_rate': (total_received / total_sent * 100) if total_sent > 0 else 0,
                'avg_messages_per_client': total_sent / len(valid_results) if valid_results else 0,
                'avg_message_size': avg_message_size
            }
        )