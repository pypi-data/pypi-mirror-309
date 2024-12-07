from dataclasses import dataclass
from typing import Dict, Any, Optional, Deque, Union, Tuple
from time import time, monotonic
import threading
from collections import deque
import statistics
import logging

logger = logging.getLogger(__name__)

@dataclass
class PacketMetrics:
    """Base metrics for any packet"""
    id: int
    size_bytes: int
    send_timestamp: float
    receive_timestamp: float
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
        
        # Regular packet metrics
        self.packet_sizes = deque(maxlen=window_size)
        self.packet_latencies = deque(maxlen=window_size)
        self.total_packets = 0
        self.total_bytes = 0
        
        self.frame_sizes = deque(maxlen=30)
        self.frame_intervals = deque(maxlen=30)
        self.frame_latencies = deque(maxlen=30)
        self.total_frames = 0
        self.frame_bytes = 0
        self.last_frame_time = None

    def record_data_sent(self, data: Any, timestamp: float) -> None:
        """Record metrics for sent data"""
        with self.metrics_lock:
            is_frame = isinstance(data, bytes)
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            
            if is_frame:
                self.total_frames += 1
                self.frame_bytes += size
                self.frame_sizes.append(size)
                
                if self.last_frame_time is not None:
                    interval = timestamp - self.last_frame_time
                    self.frame_intervals.append(interval)
                self.last_frame_time = timestamp
            
            self.total_packets += 1
            self.total_bytes += size
            self.packet_sizes.append(size)

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            size = len(data) if data else 0
            is_frame = 'image' in content_type
            
            latency = timestamp - self.start_time
            self.packet_latencies.append(latency)
            
            if is_frame:
                self.frame_latencies.append(latency)

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all network metrics"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed_time = current_time - self.start_time
            
            # Basic network metrics
            metrics = {
                "throughput": {
                    "total_mbps": (self.total_bytes * 8) / (elapsed_time * 1_000_000) if elapsed_time > 0 else 0,
                    "peak_throughput_mbps": 0
                },
                "latency": {
                    "min_ms": min(self.packet_latencies) * 1000 if self.packet_latencies else 0,
                    "max_ms": max(self.packet_latencies) * 1000 if self.packet_latencies else 0,
                    "avg_ms": statistics.mean(self.packet_latencies) * 1000 if self.packet_latencies else 0,
                    "jitter_ms": statistics.stdev(self.packet_latencies) * 1000 if len(self.packet_latencies) > 1 else 0
                },
                "packets": {
                    "total": self.total_packets,
                    "avg_size_bytes": statistics.mean(self.packet_sizes) if self.packet_sizes else 0
                },
                "data_volume_mb": self.total_bytes / 1_000_000,
                "elapsed_time": elapsed_time
            }

            # Calculate packet loss
            try:
                expected_packets = int(elapsed_time * 30)  # Assuming 30 fps
                packet_loss = ((expected_packets - self.total_packets) / expected_packets) * 100
                metrics["packet_loss_percent"] = max(0, min(100, packet_loss))
            except:
                metrics["packet_loss_percent"] = 0

            # Add frame-specific metrics if we have processed any frames
            if self.total_frames > 0:
                # Calculate FPS from frame intervals
                if self.frame_intervals:
                    avg_interval = statistics.mean(self.frame_intervals)
                    current_fps = 1 / avg_interval if avg_interval > 0 else 0
                    fps_variation = statistics.stdev(self.frame_intervals) if len(self.frame_intervals) > 1 else 0
                else:
                    current_fps = 0
                    fps_variation = 0

                # Calculate peak throughput from recent frames
                if self.frame_sizes and self.frame_intervals:
                    recent_frames = min(5, len(self.frame_sizes))
                    recent_size = sum(list(self.frame_sizes)[-recent_frames:])
                    recent_time = sum(list(self.frame_intervals)[-recent_frames:])
                    if recent_time > 0:
                        metrics["throughput"]["peak_throughput_mbps"] = (recent_size * 8) / (recent_time * 1_000_000)

                metrics["frame_metrics"] = {
                    "total_frames": self.total_frames,
                    "frame_rate": {
                        "current_fps": current_fps,
                        "fps_variation": fps_variation,
                        "frame_time_ms": (avg_interval * 1000) if self.frame_intervals else 0
                    },
                    "frame_size": {
                        "avg_bytes": statistics.mean(self.frame_sizes) if self.frame_sizes else 0,
                        "max_bytes": max(self.frame_sizes) if self.frame_sizes else 0,
                        "min_bytes": min(self.frame_sizes) if self.frame_sizes else 0
                    }
                }

                if self.frame_latencies:
                    metrics["frame_metrics"]["latency"] = {
                        "min_ms": min(self.frame_latencies) * 1000,
                        "max_ms": max(self.frame_latencies) * 1000,
                        "avg_ms": statistics.mean(self.frame_latencies) * 1000,
                        "jitter_ms": statistics.stdev(self.frame_latencies) * 1000 if len(self.frame_latencies) > 1 else 0
                    }

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