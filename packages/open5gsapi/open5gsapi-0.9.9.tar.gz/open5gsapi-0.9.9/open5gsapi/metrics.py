import subprocess
from dataclasses import dataclass
from typing import Dict, Any, Optional, Deque, Union, Tuple, List
from time import time, monotonic
import threading
from collections import deque, defaultdict
import statistics
import logging
import re
import psutil
import socket
import struct
import fcntl
import netifaces

logger = logging.getLogger(__name__)

@dataclass
class PacketMetrics:
    """Metrics for a single packet"""
    id: int
    size_bytes: int
    timestamp: float
    latency: float
    source_ip: str
    destination_ip: str
    interface: str
    ue_index: Optional[int] = None
    frame_type: Optional[str] = None
    is_frame: bool = False

class UEMetrics:
    """Metrics tracker for a single UE"""
    def __init__(self, interface: str, ip: str, window_size: int = 100):
        self.interface = interface
        self.ip = ip
        self.packet_metrics = deque(maxlen=window_size)
        self.latencies = deque(maxlen=window_size)
        self.jitter_values = deque(maxlen=window_size)
        self.throughput_samples = deque(maxlen=window_size)
        self.total_bytes = 0
        self.total_packets = 0
        self.last_packet_time = None
        self._last_bytes = 0
        self._last_time = monotonic()

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Track metrics per UE
        self.ue_metrics: Dict[str, UEMetrics] = {}  # Key: interface name
        
        # UPF interface metrics
        self.upf_metrics = UEMetrics('ogstun', '10.45.0.1', window_size)
        
        # Interface monitoring
        self._monitor_thread = threading.Thread(target=self._monitor_interfaces, daemon=True)
        self._monitor_thread.start()
        
        # Socket for ICMP measurements
        self.icmp_socket = self._create_icmp_socket()
        
        # Initial interface scan
        self._scan_interfaces()
        
    def _create_icmp_socket(self) -> Optional[socket.socket]:
        """Create raw socket for ICMP measurements"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s.setblocking(False)
            return s
        except (socket.error, PermissionError) as e:
            logger.warning(f"Could not create ICMP socket: {e}")
            return None

    def _scan_interfaces(self):
        """Scan and initialize metrics for all UE TUN interfaces"""
        try:
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                if iface.startswith('uesimtun'):
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_INET in addrs:
                        ip = addrs[netifaces.AF_INET][0]['addr']
                        if ip.startswith('10.45.0.'):
                            self.ue_metrics[iface] = UEMetrics(iface, ip, self.window_size)
                            logger.info(f"Found UE interface: {iface} with IP: {ip}")
        except Exception as e:
            logger.error(f"Error scanning interfaces: {e}")

    def _get_ue_for_ip(self, ip: str) -> Optional[UEMetrics]:
        """Get UE metrics object for a given IP"""
        for ue in self.ue_metrics.values():
            if ue.ip == ip:
                return ue
        return None

    def _monitor_interfaces(self):
        """Monitor all network interfaces for throughput calculation"""
        while True:
            try:
                # Scan for new interfaces
                self._scan_interfaces()
                
                # Monitor all interfaces
                stats = psutil.net_io_counters(pernic=True)
                current_time = monotonic()
                
                # Monitor UE interfaces
                for ue in self.ue_metrics.values():
                    if ue.interface in stats:
                        interface_stats = stats[ue.interface]
                        bytes_total = interface_stats.bytes_sent + interface_stats.bytes_recv
                        
                        if current_time > ue._last_time:
                            throughput = (bytes_total - ue._last_bytes) / (current_time - ue._last_time)
                            ue.throughput_samples.append(throughput)
                        
                        ue._last_bytes = bytes_total
                        ue._last_time = current_time
                
                # Monitor UPF interface
                if 'ogstun' in stats:
                    upf_stats = stats['ogstun']
                    bytes_total = upf_stats.bytes_sent + upf_stats.bytes_recv
                    
                    if current_time > self.upf_metrics._last_time:
                        throughput = (bytes_total - self.upf_metrics._last_bytes) / (current_time - self.upf_metrics._last_time)
                        self.upf_metrics.throughput_samples.append(throughput)
                    
                    self.upf_metrics._last_bytes = bytes_total
                    self.upf_metrics._last_time = current_time
                
            except Exception as e:
                logger.error(f"Error monitoring interfaces: {e}")
            
            threading.Event().wait(1)

    def _measure_latency(self, source_ip: str, dest_ip: str = '10.45.0.1') -> float:
        """Measure latency between source and destination IPs"""
        if not self.icmp_socket:
            return 0.0
            
        try:
            # Bind socket to source IP
            self.icmp_socket.bind((source_ip, 0))
            
            # Create and send ICMP packet
            icmp_packet = self._create_icmp_packet()
            
            start_time = monotonic()
            self.icmp_socket.sendto(icmp_packet, (dest_ip, 0))
            
            # Wait for reply with timeout
            while monotonic() - start_time < 1.0:
                try:
                    data, addr = self.icmp_socket.recvfrom(1024)
                    if addr[0] == dest_ip:
                        return monotonic() - start_time
                except (socket.error, BlockingIOError):
                    continue
                    
        except Exception as e:
            logger.debug(f"Error measuring latency: {e}")
            
        return 0.0

    def _create_icmp_packet(self) -> bytes:
        """Create an ICMP echo request packet"""
        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = id(self) & 0xFFFF
        icmp_seq = 1
        
        header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        
        # Calculate checksum
        my_checksum = 0
        for i in range(0, len(header), 2):
            my_checksum += (header[i] << 8) + header[i+1]
        my_checksum = (my_checksum >> 16) + (my_checksum & 0xFFFF)
        my_checksum = ~my_checksum & 0xFFFF
        
        return struct.pack('!BBHHH', icmp_type, icmp_code, my_checksum, icmp_id, icmp_seq)

    def record_data_sent(self, data: Any, timestamp: float, port_offset: int = 0) -> None:
        """Record metrics for sent data"""
        with self.metrics_lock:
            # Determine UE based on port offset
            ue_ip = f"10.45.0.{2 + port_offset}"
            ue = self._get_ue_for_ip(ue_ip)
            
            if not ue:
                logger.warning(f"No UE found for IP {ue_ip}")
                return
                
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            
            # Update UE metrics
            ue.total_bytes += size
            ue.total_packets += 1
            
            # Measure latency
            latency = self._measure_latency(ue.ip)
            if latency > 0:
                ue.latencies.append(latency)
                if ue.latencies:
                    jitter = abs(latency - ue.latencies[-1])
                    if ue.jitter_values:
                        new_jitter = ue.jitter_values[-1] + (jitter - ue.jitter_values[-1]) / 16
                    else:
                        new_jitter = jitter
                    ue.jitter_values.append(new_jitter)
            
            # Record packet metrics
            metrics = PacketMetrics(
                id=ue.total_packets,
                size_bytes=size,
                timestamp=timestamp,
                latency=latency,
                source_ip=ue.ip,
                destination_ip=self.upf_metrics.ip,
                interface=ue.interface,
                ue_index=port_offset,
                is_frame=isinstance(data, bytes)
            )
            ue.packet_metrics.append(metrics)
            ue.last_packet_time = timestamp

    def record_data_received(self, data: Any, timestamp: float, content_type: str) -> None:
        """Record metrics for received data"""
        with self.metrics_lock:
            size = len(data) if isinstance(data, (bytes, str)) else len(str(data))
            
            # Update UPF metrics
            self.upf_metrics.total_bytes += size
            self.upf_metrics.total_packets += 1
            
            metrics = PacketMetrics(
                id=self.upf_metrics.total_packets,
                size_bytes=size,
                timestamp=timestamp,
                latency=0.0,  # Latency measured on send
                source_ip=self.upf_metrics.ip,
                destination_ip="",  # Will be set when matched with send
                interface='ogstun',
                is_frame='image' in content_type,
                frame_type=content_type if 'image' in content_type else None
            )
            self.upf_metrics.packet_metrics.append(metrics)
            self.upf_metrics.last_packet_time = timestamp

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate network metrics across all UEs"""
        with self.metrics_lock:
            current_time = monotonic()
            elapsed_time = current_time - self.start_time
            
            # Aggregate metrics from all UEs
            all_latencies = []
            all_jitter_values = []
            total_throughput = 0
            
            for ue in self.ue_metrics.values():
                if ue.latencies:
                    all_latencies.extend(ue.latencies)
                if ue.jitter_values:
                    all_jitter_values.extend(ue.jitter_values)
                if ue.throughput_samples:
                    total_throughput += ue.throughput_samples[-1]
            
            # Calculate aggregate metrics
            metrics = {
                'throughput': {
                    'total_mbps': (total_throughput * 8) / 1_000_000 if total_throughput > 0 else 0,
                },
                'latency': {
                    'min_ms': min(all_latencies) * 1000 if all_latencies else 0,
                    'max_ms': max(all_latencies) * 1000 if all_latencies else 0,
                    'avg_ms': statistics.mean(all_latencies) * 1000 if all_latencies else 0,
                    'jitter_ms': statistics.mean(all_jitter_values) * 1000 if all_jitter_values else 0
                }
            }
            
            # Calculate frame metrics if we have frame data
            frame_packets = []
            for ue in self.ue_metrics.values():
                frame_packets.extend([p for p in ue.packet_metrics if p.is_frame])
                
            if frame_packets:
                frame_intervals = []
                prev_time = None
                for packet in sorted(frame_packets, key=lambda p: p.timestamp):
                    if prev_time:
                        frame_intervals.append(packet.timestamp - prev_time)
                    prev_time = packet.timestamp
                
                if frame_intervals:
                    avg_interval = statistics.mean(frame_intervals)
                    metrics['frame_metrics'] = {
                        'frame_rate': {
                            'current_fps': 1 / avg_interval if avg_interval > 0 else 0,
                            'frame_time_ms': avg_interval * 1000
                        },
                        'frame_size': {
                            'avg_bytes': statistics.mean([p.size_bytes for p in frame_packets]),
                            'max_bytes': max([p.size_bytes for p in frame_packets]),
                            'min_bytes': min([p.size_bytes for p in frame_packets])
                        },
                        'latency': {
                            'min_ms': min([p.latency * 1000 for p in frame_packets]),
                            'max_ms': max([p.latency * 1000 for p in frame_packets]),
                            'avg_ms': statistics.mean([p.latency * 1000 for p in frame_packets])
                        }
                    }
            
            return metrics

    def get_ue_specific_metrics(self, ue_index: int) -> Optional[Dict[str, Any]]:
        """Get metrics for a specific UE"""
        ue_ip = f"10.45.0.{2 + ue_index}"
        ue = self._get_ue_for_ip(ue_ip)
        
        if not ue:
            return None
            
        return {
            'interface': ue.interface,
            'ip': ue.ip,
            'throughput_mbps': (ue.throughput_samples[-1] * 8 / 1_000_000) if ue.throughput_samples else 0,
            'latency_ms': statistics.mean(ue.latencies) * 1000 if ue.latencies else 0,
            'jitter_ms': statistics.mean(ue.jitter_values) * 1000 if ue.jitter_values else 0,
            'total_bytes': ue.total_bytes,
            'total_packets': ue.total_packets
        }

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.ue_metrics.clear()
            self.upf_metrics = UEMetrics('ogstun', '10.45.0.1', self.window_size)
            self._scan_interfaces()