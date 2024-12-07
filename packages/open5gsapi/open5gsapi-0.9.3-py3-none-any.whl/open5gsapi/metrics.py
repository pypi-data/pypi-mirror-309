import socket
import struct
import fcntl
import array
from dataclasses import dataclass
from typing import Dict, Any, Optional, Deque, Union, Tuple
from time import time, monotonic
import threading
from collections import deque
import statistics
import logging
import subprocess
from scapy.all import sniff, IP

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
        
        # Packet metrics between UE and UPF
        self.packet_metrics = deque(maxlen=window_size)
        self.ue_upf_latencies = deque(maxlen=window_size)
        self.total_packets = 0
        self.total_bytes = 0
        
        # Frame-specific metrics
        self.frame_sizes = deque(maxlen=30)
        self.frame_intervals = deque(maxlen=30)
        self.frame_latencies = deque(maxlen=30)
        self.total_frames = 0
        self.frame_bytes = 0
        self.last_frame_time = None
        
        # Initialize packet capture
        self._setup_packet_capture()
        
    def _setup_packet_capture(self):
        """Setup packet capture on UE and UPF interfaces"""
        self.capture_thread = threading.Thread(
            target=self._capture_packets,
            daemon=True
        )
        self.capture_thread.start()
        
    def _capture_packets(self):
        """Capture packets between UE and UPF interfaces"""
        def packet_callback(pkt):
            if IP in pkt:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
                
                # Only track packets between UE (10.45.0.X) and UPF (10.45.0.1)
                if (src_ip.startswith("10.45.0.") and dst_ip == "10.45.0.1") or \
                   (src_ip == "10.45.0.1" and dst_ip.startswith("10.45.0.")):
                    with self.metrics_lock:
                        timestamp = monotonic()
                        size = len(pkt)
                        
                        metric = PacketMetrics(
                            id=self.total_packets,
                            size_bytes=size,
                            timestamp=timestamp,
                            source_ip=src_ip,
                            destination_ip=dst_ip
                        )
                        
                        self.packet_metrics.append(metric)
                        self.total_packets += 1
                        self.total_bytes += size
                        
                        # Calculate latency if we have a packet pair
                        if len(self.packet_metrics) >= 2:
                            prev_pkt = self.packet_metrics[-2]
                            if prev_pkt.source_ip == dst_ip and prev_pkt.destination_ip == src_ip:
                                latency = (timestamp - prev_pkt.timestamp) / 2  # RTT/2
                                self.ue_upf_latencies.append(latency)

        try:
            # Capture on all interfaces
            sniff(
                filter="host 10.45.0.1",  # Capture UPF traffic
                prn=packet_callback,
                store=0
            )
        except Exception as e:
            logger.error(f"Packet capture error: {e}")

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

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        with self.metrics_lock:
            if 'image' in content_type:
                self.frame_latencies.append(timestamp - self.start_time)

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all network metrics"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed_time = current_time - self.start_time
            
            # Calculate network metrics from actual UE-UPF packets
            recent_packets = list(self.packet_metrics)[-self.window_size:]
            recent_time = (recent_packets[-1].timestamp - recent_packets[0].timestamp) \
                         if len(recent_packets) > 1 else elapsed_time
            
            # Calculate throughput from recent packets
            recent_bytes = sum(pkt.size_bytes for pkt in recent_packets)
            current_throughput = (recent_bytes * 8) / (recent_time * 1_000_000) if recent_time > 0 else 0
            
            # Calculate latency statistics
            latencies = list(self.ue_upf_latencies)
            
            metrics = {
                "throughput": {
                    "total_mbps": current_throughput,
                    "peak_throughput_mbps": max(current_throughput, 0)
                },
                "latency": {
                    "min_ms": min(latencies) * 1000 if latencies else 0,
                    "max_ms": max(latencies) * 1000 if latencies else 0,
                    "avg_ms": statistics.mean(latencies) * 1000 if latencies else 0,
                    "jitter_ms": statistics.stdev(latencies) * 1000 if len(latencies) > 1 else 0
                },
                "packets": {
                    "total": self.total_packets,
                    "avg_size_bytes": statistics.mean([pkt.size_bytes for pkt in recent_packets]) if recent_packets else 0
                },
                "data_volume_mb": self.total_bytes / 1_000_000,
                "elapsed_time": elapsed_time
            }

            # Add frame-specific metrics if we have processed any frames
            if self.total_frames > 0:
                if self.frame_intervals:
                    avg_interval = statistics.mean(self.frame_intervals)
                    current_fps = 1 / avg_interval if avg_interval > 0 else 0
                else:
                    current_fps = 0

                metrics["frame_metrics"] = {
                    "frame_rate": {
                        "current_fps": current_fps,
                        "frame_time_ms": (avg_interval * 1000) if self.frame_intervals else 0
                    },
                    "frame_size": {
                        "avg_bytes": statistics.mean(self.frame_sizes) if self.frame_sizes else 0
                    }
                }

                if self.frame_latencies:
                    metrics["frame_metrics"]["latency"] = {
                        "avg_ms": statistics.mean(self.frame_latencies) * 1000
                    }

            return metrics

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.packet_metrics.clear()
            self.ue_upf_latencies.clear()
            self.total_packets = 0
            self.total_bytes = 0
            self.frame_sizes.clear()
            self.frame_intervals.clear()
            self.frame_latencies.clear()
            self.total_frames = 0
            self.frame_bytes = 0
            self.last_frame_time = None