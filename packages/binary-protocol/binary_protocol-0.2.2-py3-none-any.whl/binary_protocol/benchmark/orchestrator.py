from typing import List, Type, Dict, Any, Generic
from .base import BaseBenchmark, BenchmarkConfig, BenchmarkResult, T
from .runner import BenchmarkRunner
from .reporter import BenchmarkReporter
from ..protocol.config import ProtocolConfig
import logging

logger = logging.getLogger(__name__)

class BenchmarkOrchestrator(Generic[T]):
    """Coordinates benchmark execution and result collection"""
    
    def __init__(self, client_class: Type[T], config: ProtocolConfig):
        self.client_class = client_class
        self.config = config
        self.runner = BenchmarkRunner[T]()
        self.reporter = BenchmarkReporter()
        self.configs: Dict[str, BenchmarkConfig] = {}
        
    def add_config(self, name: str, config: BenchmarkConfig) -> None:
        """Add a named configuration"""
        self.configs[name] = config
        
    def create_benchmark(self, benchmark_class: Type[BaseBenchmark[T]], config_name: str) -> None:
        """Create and register a benchmark with specified configuration"""
        if config_name not in self.configs:
            raise ValueError(f"Configuration '{config_name}' not found")
            
        benchmark = benchmark_class(
            self.client_class, 
            self.configs[config_name],
            self.config
        )
        self.runner.add_benchmark(benchmark)
        
    async def run_all(self, save_results: bool = True) -> List[BenchmarkResult]:
        """Run all registered benchmarks with enhanced reporting"""
        results = await self.runner.run_all()
        
        # Print detailed summary
        print("\nBenchmark Results")
        print("=" * 100)
        self.reporter.print_summary(results)
        
        # Print statistical analysis
        self.reporter.print_statistics(results)
        
        # Generate plots if output is enabled
        if save_results:
            self.reporter.save_results(results)
            self.reporter.generate_plots(results)
            
        return results