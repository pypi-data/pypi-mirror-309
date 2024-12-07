from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
from collections import deque
import statistics
import logging
import threading
from time import monotonic, sleep

logger = logging.getLogger(__name__)

@dataclass
class PacketMetrics:
    """Base metrics for any packet"""
    id: int
    size_bytes: int
    timestamp: float
    source_ip: str
    destination_ip: str
    frame_type: Optional[str] = None
    is_frame: bool = False
    frame_number: Optional[int] = None
    resolution: Optional[Tuple[int, int]] = None
    quality: Optional[int] = None

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Network metrics
        self.throughput_samples = deque(maxlen=window_size)
        self.latency_samples = deque(maxlen=window_size)
        self.frame_timestamps = deque(maxlen=window_size)
        self.frame_sizes = deque(maxlen=window_size)
        
        # Video metrics
        self.frame_intervals = deque(maxlen=30)
        self.frame_latencies = deque(maxlen=30)
        
        # Counters
        self.total_bytes = 0
        self.frame_count = 0
        self.last_frame_time = None
        
        # Control flag
        self.running = True
        
        # Start background monitoring
        self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self._monitor_thread.start()
        
    def _monitor_network(self):
        """Monitor network conditions in background"""
        while self.running:
            try:
                with self.metrics_lock:
                    # Calculate throughput from recent frames
                    if len(self.frame_timestamps) >= 2:
                        time_diff = self.frame_timestamps[-1] - self.frame_timestamps[0]
                        bytes_diff = sum(self.frame_sizes)
                        if time_diff > 0:
                            mbps = (bytes_diff * 8) / (time_diff * 1_000_000)
                            self.throughput_samples.append(mbps)
                    
                    # Calculate frame timing statistics
                    if len(self.frame_timestamps) >= 2:
                        intervals = [j-i for i, j in zip(self.frame_timestamps, self.frame_timestamps[1:])]
                        if intervals:
                            avg_interval = statistics.mean(intervals)
                            self.latency_samples.append(avg_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring network: {e}")
            
            try:
                sleep(0.1)  # Check 10 times per second
            except Exception as e:
                logger.error(f"Error in sleep: {e}")
                break
            
    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record metrics for sent data"""
        with self.metrics_lock:
            is_frame = isinstance(data, bytes)
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            
            self.total_bytes += size
            
            if is_frame:
                self.frame_count += 1
                self.frame_timestamps.append(timestamp)
                self.frame_sizes.append(size)
                
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    self.frame_intervals.append(interval)
                
                self.last_frame_time = timestamp

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record metrics for received data"""
        with self.metrics_lock:
            if 'image' in content_type and self.last_frame_time is not None:
                latency = timestamp - self.last_frame_time
                self.frame_latencies.append(latency)

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all network metrics"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed = current_time - self.start_time
            
            # Calculate throughput
            recent_throughput = list(self.throughput_samples)
            current_mbps = statistics.mean(recent_throughput) if recent_throughput else 0
            
            # Calculate latency stats
            latencies = list(self.latency_samples)
            
            metrics = {
                "throughput": {
                    "total_mbps": current_mbps,
                    "peak_throughput_mbps": max(recent_throughput) if recent_throughput else 0
                },
                "latency": {
                    "min_ms": min(latencies) * 1000 if latencies else 0,
                    "max_ms": max(latencies) * 1000 if latencies else 0,
                    "avg_ms": statistics.mean(latencies) * 1000 if latencies else 0,
                    "jitter_ms": statistics.stdev(latencies) * 1000 if len(latencies) > 1 else 0
                },
                "frame_metrics": {
                    "frame_rate": {
                        "current_fps": self.frame_count / elapsed if elapsed > 0 else 0,
                        "frame_time_ms": (1000 / (self.frame_count / elapsed)) if self.frame_count > 0 and elapsed > 0 else 0
                    },
                    "frame_size": {
                        "avg_bytes": statistics.mean(self.frame_sizes) if self.frame_sizes else 0
                    }
                }
            }
            
            # Add frame latency if available
            if self.frame_latencies:
                metrics["frame_metrics"]["latency"] = {
                    "min_ms": min(self.frame_latencies) * 1000,
                    "max_ms": max(self.frame_latencies) * 1000,
                    "avg_ms": statistics.mean(self.frame_latencies) * 1000,
                    "jitter_ms": statistics.stdev(self.frame_latencies) * 1000 if len(self.frame_latencies) > 1 else 0
                }
            
            return metrics

    def get_frame_metrics(self) -> Optional[Dict[str, Any]]:
        """Get frame-specific metrics if available"""
        with self.metrics_lock:
            if self.frame_count == 0:
                return None
                
            return self.calculate_metrics().get("frame_metrics")

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.throughput_samples.clear()
            self.latency_samples.clear()
            self.frame_timestamps.clear()
            self.frame_sizes.clear()
            self.frame_intervals.clear()
            self.frame_latencies.clear()
            self.total_bytes = 0
            self.frame_count = 0
            self.last_frame_time = None

    def __del__(self):
        """Cleanup when object is destroyed"""
        self.running = False
        if hasattr(self, '_monitor_thread'):
            self._monitor_thread.join(timeout=1.0)