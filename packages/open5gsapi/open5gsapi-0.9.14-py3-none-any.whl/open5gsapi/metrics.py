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

        # Debug counters
        self.debug_sent_count = 0
        self.debug_received_count = 0
        
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
        """Monitor network metrics in background"""
        while True:
            try:
                current_time = monotonic()
                current_bytes = self._get_interface_bytes()
                
                with self.metrics_lock:
                    # Calculate throughput
                    elapsed = current_time - self._prev_time
                    for iface in current_bytes:
                        if iface in self._prev_bytes:
                            prev_sent, prev_recv = self._prev_bytes[iface]
                            curr_sent, curr_recv = current_bytes[iface]
                            
                            total_bytes = (curr_sent + curr_recv - prev_sent - prev_recv)
                            if elapsed > 0:
                                throughput = total_bytes / elapsed
                                self.packet_sizes.append(throughput)
                    
                    # Measure latency
                    latency = self._measure_latency()
                    if latency > 0:
                        self.packet_latencies.append(latency)
                    
                    self._prev_bytes = current_bytes
                    self._prev_time = current_time
                
                threading.Event().wait(1)  # Sample every second
                
            except Exception as e:
                logger.error(f"Error in network monitor: {e}")
                threading.Event().wait(5)  # Wait longer on error

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record metrics for sent data"""
        with self.metrics_lock:
            self.debug_sent_count += 1
            is_frame = isinstance(data, bytes)
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            
            logger.debug(f"Recording sent data - Size: {size}, Is frame: {is_frame}")
            
            if is_frame:
                self.total_frames += 1
                self.frame_bytes += size
                self.frame_sizes.append(size)
                
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    self.frame_intervals.append(interval)
                    logger.debug(f"Frame interval: {interval:.3f}s")
                self.last_frame_time = timestamp
            
            self.total_packets += 1
            self.total_bytes += size
            self.packet_sizes.append(size)

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            self.debug_received_count += 1
            size = len(data) if isinstance(data, (bytes, str)) else 0
            
            logger.debug(f"Recording received data - Size: {size}, Content type: {content_type}")
            
            is_frame = 'image' in content_type
            
            latency = timestamp - self.start_time
            self.packet_latencies.append(latency)
            
            if is_frame:
                self.frame_latencies.append(latency)
                logger.debug(f"Frame latency: {latency:.3f}s")

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all network metrics"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed_time = current_time - self.start_time
            
            logger.debug(f"Calculating metrics after {elapsed_time:.1f}s")
            logger.debug(f"Total data sent count: {self.debug_sent_count}")
            logger.debug(f"Total data received count: {self.debug_received_count}")
            logger.debug(f"Packet latencies count: {len(self.packet_latencies)}")
            logger.debug(f"Frame latencies count: {len(self.frame_latencies)}")
            
            metrics = {
                "throughput": {
                    "total_mbps": (self.total_bytes * 8) / (elapsed_time * 1_000_000) if elapsed_time > 0 else 0,
                },
                "latency": {
                    "min_ms": min(self.packet_latencies) * 1000 if self.packet_latencies else 0,
                    "max_ms": max(self.packet_latencies) * 1000 if self.packet_latencies else 0,
                    "avg_ms": statistics.mean(self.packet_latencies) * 1000 if self.packet_latencies else 0,
                    "jitter_ms": statistics.stdev(self.packet_latencies) * 1000 if len(self.packet_latencies) > 1 else 0
                }
            }
            
            logger.debug(f"Calculated metrics: {metrics}")
            return metrics

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