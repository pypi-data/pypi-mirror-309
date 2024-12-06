# benchmark/reporter.py
from typing import List, Dict, Any, Optional
from .base import BenchmarkResult
import json
import logging
from datetime import datetime
import os
import statistics
from dataclasses import asdict
import matplotlib.pyplot as plt
import seaborn as sns

class BenchmarkReporter:
    """Enhanced reporter with visualization and statistical analysis"""
    
    # Global table configuration
    TABLE_CONFIG = {
        'width': 150,
        'column_widths': {
            'benchmark': 40,
            'size': 12,
            'throughput': 15,
            'latency': 12,
            'msgs_per_sec': 12,
            'success': 12,
            'duration': 15,
            # Resource table columns
            'resource_benchmark': 35,
            'cpu_usage': 12,
            'memory_delta': 12,
            'network_io': 40,
            # Comparison table columns
            'comparison_benchmark': 25,
            'current': 12,
            'baseline': 12,
            'change': 12
        }
    }
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or "benchmark_results"
        self._logger = logging.getLogger(__name__)
        self._setup_output_dir()
        
    def _setup_output_dir(self) -> None:
        """Setup output directory structure"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.plots_dir = os.path.join(self.output_dir, "plots")
        if not os.path.exists(self.plots_dir):
            os.makedirs(self.plots_dir)
            
    def _calculate_statistics(self, results: List[BenchmarkResult]) -> Dict[str, Dict[str, float]]:
        """Calculate statistical metrics from benchmark results"""
        if not results:
            return {}
        
        throughputs = [r.throughput for r in results]  # Use existing throughput values
        latencies = [r.latency for r in results]       # Use existing latency values
        
        # Add logging for debugging
        logging.debug(f"Processing statistics for {len(results)} results")
        for r in results:
            logging.debug(f"Result: {r.name} - Throughput: {r.throughput} MB/s, Latency: {r.latency} ms")
        
        stats = {
            "throughput": {
                "mean": statistics.mean(throughputs) if throughputs else 0,
                "min": min(throughputs) if throughputs else 0,
                "max": max(throughputs) if throughputs else 0
            },
            "latency": {
                "mean": statistics.mean(latencies) if latencies else 0,
                "min": min(latencies) if latencies else 0,
                "max": max(latencies) if latencies else 0
            }
        }
        
        # Only add advanced statistics if we have enough data points
        if len(throughputs) >= 2:
            stats["throughput"].update({
                "std_dev": statistics.stdev(throughputs),
                "median": statistics.median(throughputs),
                "percentile_95": statistics.quantiles(throughputs, n=20)[18]
            })
            stats["latency"].update({
                "std_dev": statistics.stdev(latencies),
                "median": statistics.median(latencies),
                "percentile_95": statistics.quantiles(latencies, n=20)[18]
            })
        
        return stats
        
    def generate_plots(self, results: List[BenchmarkResult]) -> None:
        """Generate visualization plots"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Throughput comparison
        plt.figure(figsize=(10, 6))
        sns.barplot(x=[r.name for r in results], y=[r.throughput for r in results])
        plt.title("Throughput Comparison")
        plt.xticks(rotation=45)
        plt.ylabel("MB/s")
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, f"throughput_{timestamp}.png"))
        plt.close()
        
        # Latency comparison
        plt.figure(figsize=(10, 6))
        sns.barplot(x=[r.name for r in results], y=[r.latency for r in results])
        plt.title("Latency Comparison")
        plt.xticks(rotation=45)
        plt.ylabel("ms")
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, f"latency_{timestamp}.png"))
        plt.close()
        
    def _format_size(self, size: int) -> str:
        """Format byte sizes in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}TB"
        
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 0.001:
            return f"{seconds*1000000:.2f}µs"
        elif seconds < 1:
            return f"{seconds*1000:.2f}ms"
        else:
            return f"{seconds:.2f}s"
            
    def print_result(self, result: BenchmarkResult) -> None:
        """Print a single benchmark result"""
        print(f"\n{result.name} Results:")
        print("-" * 60)
        print(f"Throughput: {result.throughput:.2f} MB/s")
        print(f"Latency: {result.latency:.2f} ms")
        print(f"Messages/sec: {result.messages_per_sec:.2f}")
        print(f"Total Messages: {result.total_messages:,}")
        print(f"Errors: {result.errors}")
        print(f"Duration: {self._format_duration(result.duration)}")
        
        if result.custom_metrics:
            print("\nCustom Metrics:")
            for key, value in result.custom_metrics.items():
                print(f"{key}: {value}")
                
    def print_summary(self, results: List[BenchmarkResult]) -> None:
        """Print a detailed summary of all benchmark results"""
        TABLE_WIDTH = self.TABLE_CONFIG['width']
        SEPARATOR = "=" * TABLE_WIDTH
        SUB_SEPARATOR = "-" * TABLE_WIDTH
        
        # Enhanced column configurations with size information
        headers = [
            ("Benchmark", self.TABLE_CONFIG['column_widths']['benchmark']),
            ("Payload", 12),  # New column for payload size
            ("Wire Size", 12),  # Total size including protocol overhead
            ("Throughput", self.TABLE_CONFIG['column_widths']['throughput']),
            ("Latency", self.TABLE_CONFIG['column_widths']['latency']),
            ("Msgs/sec", self.TABLE_CONFIG['column_widths']['msgs_per_sec']),
            ("Success", self.TABLE_CONFIG['column_widths']['success']),
            ("Duration", self.TABLE_CONFIG['column_widths']['duration'])
        ]
        
        title = "Detailed Benchmark Summary"
        title_padding = (TABLE_WIDTH - len(title)) // 2
        
        print(f"\n{' ' * title_padding}{title}")
        print(SEPARATOR)
        
        # Create header line
        header_parts = []
        for name, width in headers:
            header_parts.append(f"{name:<{width}}")
        header_line = " | ".join(header_parts)
        print(header_line)
        print(SUB_SEPARATOR)
        
        # Print results with enhanced information
        for result in results:
            if "FixedSizeBenchmark" in result.name:
                payload_size = 8  # Fixed 8-byte payload
                wire_size = 10    # 8 bytes + 2 byte header
                benchmark_name = "Fixed Size"
            elif "VariableSizeBenchmark" in result.name:
                wire_size = result.message_size
                payload_size = wire_size - 6  # Subtract header (2) and length prefix (4)
                benchmark_name = f"Variable Size"
            elif "RealisticBenchmark" in result.name:
                wire_size = result.message_size
                payload_size = wire_size - 6  # Same overhead calculation
                benchmark_name = "Realistic Multi-Client"
            else:
                payload_size = result.message_size
                wire_size = result.message_size
                benchmark_name = result.name
                
            success_rate = (result.successful_messages / result.total_messages * 100) \
                if result.total_messages > 0 else 0
            
            columns = [
                f"{benchmark_name:<{headers[0][1]}}",
                f"{self._format_size(payload_size):<{headers[1][1]}}",
                f"{self._format_size(wire_size):<{headers[2][1]}}",
                f"{result.throughput:>{headers[3][1]-3}.2f}MB/s",
                f"{result.latency:>{headers[4][1]-3}.2f}ms",
                f"{result.messages_per_sec:>{headers[5][1]-1}.1f}",
                f"{success_rate:>{headers[6][1]-2}.1f}%",
                f"{self._format_duration(result.duration):>{headers[7][1]-1}}"
            ]
            print(" | ".join(columns))
        
        # Print resource utilization in table format
        if any(result.custom_metrics for result in results):
            print(f"\n{' ' * (title_padding)}Resource Utilization")
            print(SEPARATOR)
            
            # Resource table headers
            resource_headers = [
                ("Benchmark", self.TABLE_CONFIG['column_widths']['resource_benchmark']),
                ("CPU Usage", self.TABLE_CONFIG['column_widths']['cpu_usage']),
                ("Memory Δ", self.TABLE_CONFIG['column_widths']['memory_delta']),
                ("Network I/O", self.TABLE_CONFIG['column_widths']['network_io'])
            ]
            
            # Print resource headers
            resource_header = " | ".join(f"{name:<{width}}" for name, width in resource_headers)
            print(resource_header)
            print(SUB_SEPARATOR)
            
            # Print resource data
            for result in results:
                if result.custom_metrics:
                    cpu = result.custom_metrics.get('cpu_percent')
                    mem = result.custom_metrics.get('memory_delta_mb')
                    net_sent = self._format_size(result.custom_metrics.get('network_bytes_sent', 0))
                    net_recv = self._format_size(result.custom_metrics.get('network_bytes_recv', 0))
                    
                    columns = [
                        f"{result.name:<{resource_headers[0][1]}}",
                        f"{cpu:>{resource_headers[1][1]-2}.1f}%" if isinstance(cpu, (int, float)) else "N/A".center(resource_headers[1][1]),
                        f"{mem:>{resource_headers[2][1]-3}.1f}MB" if isinstance(mem, (int, float)) else "N/A".center(resource_headers[2][1]),
                        f"{net_sent} sent / {net_recv} recv".center(resource_headers[3][1])
                    ]
                    print(" | ".join(columns))
            
    def save_results(self, results: List[BenchmarkResult]) -> str:
        """Save results to a JSON file"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_results_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert results to serializable format
        serializable_results = []
        for result in results:
            result_dict = {
                'name': result.name,
                'throughput': result.throughput,
                'latency': result.latency,
                'messages_per_sec': result.messages_per_sec,
                'message_size': result.message_size,
                'total_messages': result.total_messages,
                'errors': result.errors,
                'duration': result.duration
            }
            if result.custom_metrics:
                result_dict['custom_metrics'] = result.custom_metrics
            serializable_results.append(result_dict)
            
        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'results': serializable_results
            }, f, indent=2)
            
        self._logger.info(f"Results saved to {filepath}")
        return filepath
        
    def generate_comparison(self, results: List[BenchmarkResult], baseline_results: List[BenchmarkResult]) -> None:
        """Compare current results with baseline results"""
        print("\nPerformance Comparison")
        print("=" * self.TABLE_CONFIG['width'])
        print(f"{'Benchmark':{self.TABLE_CONFIG['column_widths']['comparison_benchmark']}} | {'Current':>{self.TABLE_CONFIG['column_widths']['current']}} | {'Baseline':>{self.TABLE_CONFIG['column_widths']['baseline']}} | {'Change':>{self.TABLE_CONFIG['column_widths']['change']}}")
        print("-" * self.TABLE_CONFIG['width'])
        
        for current, baseline in zip(results, baseline_results):
            if current.name != baseline.name:
                continue
                
            throughput_change = ((current.throughput - baseline.throughput) / baseline.throughput) * 100
            latency_change = ((current.latency - baseline.latency) / baseline.latency) * 100
            
    def print_statistics(self, results: List[BenchmarkResult]) -> None:
        """Print statistical analysis of benchmark results"""
        print("\nStatistical Analysis")
        print("=" * self.TABLE_CONFIG['width'])
        
        for result in results:
            stats = self._calculate_statistics([result])
            print(f"\n{result.name} Statistics:")
            print("-" * 50)
            
            if "throughput" in stats:
                print("\nThroughput:")
                for metric, value in stats["throughput"].items():
                    print(f"  {metric.replace('_', ' ').title()}: {value:.2f} MB/s")
            
            if "latency" in stats:
                print("\nLatency:")
                for metric, value in stats["latency"].items():
                    print(f"  {metric.replace('_', ' ').title()}: {value:.2f} ms")
            