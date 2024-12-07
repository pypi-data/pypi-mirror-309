import subprocess
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Deque
from collections import deque
import threading
import statistics
import logging
import time
from time import monotonic
import json

logger = logging.getLogger(__name__)

@dataclass
class Packet:
    """Represents a network packet with timing information"""
    size: int
    send_time: float
    receive_time: Optional[float] = None
    source_ip: str = ""
    dest_ip: str = ""
    is_frame: bool = False

class InterfaceMonitor:
    """Monitors network interfaces inside Docker containers"""
    def __init__(self, container_name: str):
        self.container = container_name
        self.interfaces: Dict[str, str] = {}  # interface name -> IP address
        self.update_interfaces()

    def update_interfaces(self) -> None:
        """Update interface list from Docker container"""
        try:
            # Get interfaces from container
            cmd = ['docker', 'exec', self.container, 'ip', 'addr', 'show']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.interfaces.clear()
                current_iface = None
                
                for line in result.stdout.splitlines():
                    if ': ' in line:  # Interface line
                        current_iface = line.split(': ')[1].split('@')[0]
                    elif 'inet ' in line and current_iface:  # IP address line
                        ip = line.strip().split()[1].split('/')[0]
                        if current_iface.startswith(('uesimtun', 'ogstun')):
                            self.interfaces[current_iface] = ip
                            logger.info(f"Found interface {current_iface} with IP {ip} in {self.container}")
        except Exception as e:
            logger.error(f"Error updating interfaces for {self.container}: {e}")

    def get_interface_stats(self, interface: str) -> Optional[Dict[str, int]]:
        """Get network statistics for an interface"""
        try:
            cmd = ['docker', 'exec', self.container, 'cat', f'/sys/class/net/{interface}/statistics/rx_bytes', 
                  f'/sys/class/net/{interface}/statistics/tx_bytes']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                rx_bytes, tx_bytes = map(int, result.stdout.strip().split())
                return {'rx_bytes': rx_bytes, 'tx_bytes': tx_bytes}
        except Exception as e:
            logger.error(f"Error getting stats for {interface} in {self.container}: {e}")
        return None

class MetricsCollector:
    """Collects and calculates network metrics"""
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.packets: Deque[Packet] = deque(maxlen=window_size)
        self.throughput_samples: Deque[float] = deque(maxlen=window_size)
        self.latency_samples: Deque[float] = deque(maxlen=window_size)
        self.jitter_samples: Deque[float] = deque(maxlen=window_size)
        self.last_packet_time = None
        self.total_bytes = 0
        self.total_packets = 0

    def add_packet(self, packet: Packet) -> None:
        """Add a packet and update metrics"""
        self.packets.append(packet)
        self.total_bytes += packet.size
        self.total_packets += 1
        
        if packet.receive_time is not None:
            latency = packet.receive_time - packet.send_time
            self.latency_samples.append(latency)
            
            # Calculate jitter (RFC 3550)
            if len(self.latency_samples) >= 2:
                jitter = abs(self.latency_samples[-1] - self.latency_samples[-2])
                if self.jitter_samples:
                    new_jitter = self.jitter_samples[-1] + (jitter - self.jitter_samples[-1]) / 16
                else:
                    new_jitter = jitter
                self.jitter_samples.append(new_jitter)
        
        # Update throughput
        current_time = monotonic()
        if self.last_packet_time is not None:
            interval = current_time - self.last_packet_time
            if interval > 0:
                throughput = packet.size / interval
                self.throughput_samples.append(throughput)
        self.last_packet_time = current_time

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Initialize Docker monitors
        self.ue_monitor = InterfaceMonitor('ue')
        self.upf_monitor = InterfaceMonitor('upf')
        
        # Metrics collectors
        self.collectors: Dict[str, MetricsCollector] = {}  # IP -> collector
        
        # Packet tracking
        self.pending_packets: Dict[int, Packet] = {}  # packet_id -> Packet
        self._packet_counter = 0
        self._packet_lock = threading.Lock()
        
        # Start monitoring thread
        self._monitor_thread = threading.Thread(target=self._monitor_network, daemon=True)
        self._monitor_thread.start()
        
    def _get_next_packet_id(self) -> int:
        with self._packet_lock:
            self._packet_counter += 1
            return self._packet_counter

    def _monitor_network(self):
        """Monitor network interfaces in containers"""
        while True:
            try:
                # Update interface lists
                self.ue_monitor.update_interfaces()
                self.upf_monitor.update_interfaces()
                
                # Initialize collectors for any new interfaces
                for iface, ip in self.ue_monitor.interfaces.items():
                    if ip not in self.collectors:
                        self.collectors[ip] = MetricsCollector(self.window_size)
                
                if '10.45.0.1' not in self.collectors:  # UPF
                    self.collectors['10.45.0.1'] = MetricsCollector(self.window_size)
                
                # Update throughput measurements
                current_time = monotonic()
                for monitor in [self.ue_monitor, self.upf_monitor]:
                    for iface, ip in monitor.interfaces.items():
                        stats = monitor.get_interface_stats(iface)
                        if stats and ip in self.collectors:
                            collector = self.collectors[ip]
                            if hasattr(collector, 'last_stats'):
                                last_stats = collector.last_stats
                                last_time = collector.last_stats_time
                                
                                bytes_delta = (stats['rx_bytes'] + stats['tx_bytes'] - 
                                             last_stats['rx_bytes'] - last_stats['tx_bytes'])
                                time_delta = current_time - last_time
                                
                                if time_delta > 0:
                                    throughput = bytes_delta / time_delta
                                    collector.throughput_samples.append(throughput)
                            
                            collector.last_stats = stats
                            collector.last_stats_time = current_time
                            
            except Exception as e:
                logger.error(f"Error in network monitor: {e}")
            
            time.sleep(1)  # Update every second

    def record_data_sent(self, data: Any, timestamp: float, port_offset: int = 0) -> None:
        """Record metrics for sent data"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            source_ip = f"10.45.0.{2 + port_offset}"
            dest_ip = "10.45.0.1"
            
            # Create new packet record
            packet = Packet(
                size=size,
                send_time=timestamp,
                source_ip=source_ip,
                dest_ip=dest_ip,
                is_frame=isinstance(data, bytes)
            )
            
            # Get or create collector for this UE
            if source_ip not in self.collectors:
                self.collectors[source_ip] = MetricsCollector(self.window_size)
            
            # Add packet to collector
            self.collectors[source_ip].add_packet(packet)
            
            # Store packet for matching with receive
            packet_id = self._get_next_packet_id()
            self.pending_packets[packet_id] = packet

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record metrics for received data"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            
            # Match with pending packet if possible
            matched_id = None
            for packet_id, packet in self.pending_packets.items():
                if packet.size == size:
                    packet.receive_time = timestamp
                    if '10.45.0.1' not in self.collectors:
                        self.collectors['10.45.0.1'] = MetricsCollector(self.window_size)
                    self.collectors['10.45.0.1'].add_packet(packet)
                    matched_id = packet_id
                    break
            
            if matched_id:
                del self.pending_packets[matched_id]

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate network metrics"""
        with self.metrics_lock:
            # Aggregate metrics across all collectors
            all_latencies = []
            all_jitter = []
            total_throughput = 0
            frame_metrics = []
            
            for ip, collector in self.collectors.items():
                if collector.latency_samples:
                    all_latencies.extend(collector.latency_samples)
                if collector.jitter_samples:
                    all_jitter.extend(collector.jitter_samples)
                if collector.throughput_samples:
                    total_throughput += collector.throughput_samples[-1]
                
                # Collect frame metrics
                frame_packets = [p for p in collector.packets if p.is_frame]
                if frame_packets:
                    frame_metrics.extend(frame_packets)
            
            metrics = {
                'throughput': {
                    'total_mbps': (total_throughput * 8) / 1_000_000 if total_throughput > 0 else 0,
                },
                'latency': {
                    'min_ms': min(all_latencies) * 1000 if all_latencies else 0,
                    'max_ms': max(all_latencies) * 1000 if all_latencies else 0,
                    'avg_ms': statistics.mean(all_latencies) * 1000 if all_latencies else 0,
                    'jitter_ms': statistics.mean(all_jitter) * 1000 if all_jitter else 0
                }
            }
            
            # Add frame metrics if available
            if frame_metrics:
                frame_intervals = []
                prev_time = None
                for packet in sorted(frame_metrics, key=lambda p: p.send_time):
                    if prev_time is not None:
                        frame_intervals.append(packet.send_time - prev_time)
                    prev_time = packet.send_time
                
                if frame_intervals:
                    avg_interval = statistics.mean(frame_intervals)
                    metrics['frame_metrics'] = {
                        'frame_rate': {
                            'current_fps': 1 / avg_interval if avg_interval > 0 else 0,
                            'frame_time_ms': avg_interval * 1000
                        },
                        'frame_size': {
                            'avg_bytes': statistics.mean([p.size for p in frame_metrics]),
                            'max_bytes': max([p.size for p in frame_metrics]),
                            'min_bytes': min([p.size for p in frame_metrics])
                        }
                    }
            
            return metrics

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.collectors.clear()
            self.pending_packets.clear()
            self._packet_counter = 0
            
            # Re-initialize monitors
            self.ue_monitor.update_interfaces()
            self.upf_monitor.update_interfaces()