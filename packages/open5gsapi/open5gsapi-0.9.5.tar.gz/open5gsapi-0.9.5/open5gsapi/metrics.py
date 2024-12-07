import subprocess
from dataclasses import dataclass
from typing import Dict, Any, Optional, Deque, Union, Tuple
from time import time, monotonic
import threading
from collections import deque
import statistics
import logging
import re
import psutil

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

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Packet metrics
        self.packet_sizes = deque(maxlen=window_size)
        self.packet_latencies = deque(maxlen=window_size)
        self.total_packets = 0
        self.total_bytes = 0
        
        # Frame metrics
        self.frame_sizes = deque(maxlen=30)
        self.frame_intervals = deque(maxlen=30)
        self.frame_latencies = deque(maxlen=30)
        self.total_frames = 0
        self.frame_bytes = 0
        self.last_frame_time = None
        
        # Network monitoring
        self._prev_bytes = self._get_interface_bytes()
        self._prev_time = monotonic()
        self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self._monitor_thread.start()
        
        # Network metrics
        self.throughput_samples = deque(maxlen=window_size)
        self.latency_samples = deque(maxlen=window_size)
        self.frame_timestamps = deque(maxlen=window_size)
        self.frame_sizes = deque(maxlen=window_size)


    def _get_interface_bytes(self) -> Dict[str, Tuple[int, int]]:
        """Get bytes sent/received for relevant interfaces"""
        stats = {}
        try:
            for iface, counters in psutil.net_io_counters(pernic=True).items():
                if iface.startswith(('uesimtun', 'ogstun')):
                    stats[iface] = (counters.bytes_sent, counters.bytes_recv)
        except Exception as e:
            logger.error(f"Error getting interface stats: {e}")
        return stats

    def _measure_latency(self) -> float:
        """Measure latency using ping"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', '10.45.0.1'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                match = re.search(r'time=([\d.]+)', result.stdout)
                if match:
                    return float(match.group(1)) / 1000  # Convert ms to seconds
        except Exception as e:
            logger.error(f"Error measuring latency: {e}")
        return 0

    def _monitor_network(self):
        """Monitor network conditions in background"""
        while True:
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
            
            time.sleep(0.1)  # Check 10 times per second
            
    def record_data_sent(self, data: bytes, timestamp: float) -> None:
        with self.metrics_lock:
            size = len(data)
            self.total_bytes += size
            self.frame_count += 1
            
            self.frame_timestamps.append(timestamp)
            self.frame_sizes.append(size)
            
            self.last_frame_time = timestamp
            
    def calculate_metrics(self) -> Dict[str, Any]:
        with self.metrics_lock:
            current_time = time.monotonic()
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
            
            return metrics
        
    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            if 'image' in content_type:
                self.frame_latencies.append(timestamp - self.start_time)

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.packet_sizes.clear()
            self.packet_latencies.clear()
            self.total_packets = 0
            self.total_bytes = 0
            self.frame_sizes.clear()
            self.frame_intervals.clear()
            self.frame_latencies.clear()
            self.total_frames = 0
            self.frame_bytes = 0
            self.last_frame_time = None
            self._prev_bytes = self._get_interface_bytes()
            self._prev_time = monotonic()