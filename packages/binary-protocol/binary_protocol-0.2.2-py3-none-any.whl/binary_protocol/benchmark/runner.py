# benchmark/runner.py
import asyncio
import time
from typing import Generic, TypeVar, List, Dict, Any
from .base import BaseBenchmark, BenchmarkResult, MessageProtocol
import psutil
import resource
from dataclasses import dataclass
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=MessageProtocol)

@dataclass
class ResourceMetrics:
    cpu_percent: float
    memory_usage: int
    open_files: int
    network_bytes_sent: int
    network_bytes_recv: int
    
class ResourceMonitor:
    """Monitors system resource usage during benchmarks"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.initial_metrics: Optional[ResourceMetrics] = None
        self.final_metrics: Optional[ResourceMetrics] = None
        
    def start(self) -> None:
        """Start monitoring resources"""
        self.process.cpu_percent()  # First call to initialize CPU monitoring
        net_io = psutil.net_io_counters()
        self.initial_metrics = ResourceMetrics(
            cpu_percent=0,  # Will be calculated on stop
            memory_usage=self.process.memory_info().rss,
            open_files=len(self.process.open_files()),
            network_bytes_sent=net_io.bytes_sent,
            network_bytes_recv=net_io.bytes_recv
        )
        
    def stop(self) -> Dict[str, Any]:
        """Stop monitoring and return metrics"""
        net_io = psutil.net_io_counters()
        cpu_percent = self.process.cpu_percent()
        memory_current = self.process.memory_info().rss
        
        return {
            "cpu_percent": cpu_percent,
            "memory_delta_mb": (memory_current - self.initial_metrics.memory_usage) / (1024 * 1024),
            "max_open_files": len(self.process.open_files()),
            "network_bytes_sent": net_io.bytes_sent - self.initial_metrics.network_bytes_sent,
            "network_bytes_recv": net_io.bytes_recv - self.initial_metrics.network_bytes_recv
        }

class BenchmarkRunner(Generic[T]):
    """Enhanced runner with batch processing capabilities"""
    
    def __init__(self):
        self.benchmarks: List[BaseBenchmark[T]] = []
        self.resource_monitor = ResourceMonitor()
        
    def add_benchmark(self, benchmark: BaseBenchmark[T]) -> None:
        """Add a benchmark to the runner"""
        self.benchmarks.append(benchmark)
        
    async def run_single_benchmark(self, benchmark: BaseBenchmark[T]) -> BenchmarkResult:
        """Run a single benchmark and collect results"""
        try:
            await benchmark.setup()
            await benchmark.warmup()
            
            self.resource_monitor.start()
            result = await benchmark.run()
            resource_metrics = self.resource_monitor.stop()
            
            # Add resource metrics to the result
            result.custom_metrics.update(resource_metrics)
            return result
            
        finally:
            await benchmark.teardown()
            
    async def run_all(self) -> List[BenchmarkResult]:
        """Run all registered benchmarks"""
        results = []
        for benchmark in self.benchmarks:
            logger.info(f"Running benchmark: {benchmark.__class__.__name__}")
            result = await self.run_single_benchmark(benchmark)
            results.append(result)
        return results
        
    async def run_batch(self, benchmark: BaseBenchmark[T], batch_size: int) -> BenchmarkResult:
        """Run benchmark with batch processing"""
        try:
            await benchmark.setup()
            await benchmark.warmup()
            
            start_time = time.perf_counter()
            total_bytes = 0
            messages_sent = 0
            errors = 0
            
            # Process in batches
            for _ in range(benchmark.config.iterations // batch_size):
                try:
                    # Create batch of messages
                    messages = [
                        await benchmark.create_message()
                        for _ in range(batch_size)
                    ]
                    
                    # Calculate actual wire size including protocol overhead
                    batch_bytes = 0
                    for message in messages:
                        payload_size = len(str(message).encode())
                        wire_size = 2  # Header size
                        if hasattr(benchmark, 'is_variable_length') and benchmark.is_variable_length:
                            wire_size += 4  # Add length prefix for variable length messages
                        wire_size += payload_size
                        batch_bytes += wire_size
                    
                    total_bytes += batch_bytes
                    
                    # Send batch
                    tasks = [
                        benchmark.client.send_message(
                            benchmark.config.message_type,
                            message
                        )
                        for message in messages
                    ]
                    await asyncio.gather(*tasks)
                    
                    # Receive responses
                    response_tasks = [
                        benchmark.client.receive_message()
                        for _ in range(batch_size)
                    ]
                    responses = await asyncio.gather(*response_tasks)
                    
                    # Validate responses
                    for response in responses:
                        if not await benchmark.validate_response(response):
                            errors += 1
                            
                    messages_sent += batch_size
                    
                except Exception as e:
                    errors += batch_size
                    self._logger.error(f"Batch error: {str(e)}")
                    
            end_time = time.perf_counter()
            duration = end_time - start_time
            
            return BenchmarkResult(
                name=f"{benchmark.__class__.__name__}_batch{batch_size}",
                throughput=(total_bytes / duration) / (1024 * 1024),
                latency=(duration / messages_sent) * 1000 if messages_sent > 0 else 0,
                messages_per_sec=messages_sent / duration,
                message_size=benchmark.config.message_size,
                total_messages=messages_sent,
                errors=errors,
                successful_messages=messages_sent - errors,
                duration=duration,
                custom_metrics={"batch_size": batch_size}
            )
            
        finally:
            await benchmark.teardown()