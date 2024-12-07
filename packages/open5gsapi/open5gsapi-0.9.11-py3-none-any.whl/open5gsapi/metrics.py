from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Union, Tuple
from collections import deque
import threading
import statistics
import logging
import psutil
import socket
import subprocess
import time
from time import monotonic
import netifaces
import re
import shutil

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

class LatencyMeasurer:
    """Handles different methods of latency measurement"""
    def __init__(self):
        self.method = self._determine_measurement_method()
        logger.info(f"Using latency measurement method: {self.method}")

    def _determine_measurement_method(self) -> str:
        """Determine the best available method for latency measurement"""
        # Try ping
        if self._check_ping_available():
            return 'ping'
        # Try tc
        elif self._check_tc_available():
            return 'tc'
        # Fallback to timestamp
        else:
            return 'timestamp'

    def _check_ping_available(self) -> bool:
        """Check if ping command is available and has necessary permissions"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', '127.0.0.1'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=1
            )
            return result.returncode == 0
        except:
            return False

    def _check_tc_available(self) -> bool:
        """Check if tc command is available"""
        return shutil.which('tc') is not None

    def measure_latency(self, source_ip: str, dest_ip: str = '10.45.0.1') -> float:
        """Measure latency using the best available method"""
        if self.method == 'ping':
            return self._measure_with_ping(dest_ip)
        elif self.method == 'tc':
            return self._measure_with_tc(source_ip, dest_ip)
        else:
            return self._measure_with_timestamp()

    def _measure_with_ping(self, dest_ip: str) -> float:
        """Measure latency using ping command"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', dest_ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=1
            )
            if result.returncode == 0:
                match = re.search(r'time=([\d.]+)', result.stdout)
                if match:
                    return float(match.group(1)) / 1000  # Convert ms to seconds
        except:
            pass
        return 0.0

    def _measure_with_tc(self, source_ip: str, dest_ip: str) -> float:
        """Measure latency using tc command"""
        try:
            interface = self._get_interface_for_ip(source_ip)
            if interface:
                result = subprocess.run(
                    ['tc', '-s', 'qdisc', 'show', 'dev', interface],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    match = re.search(r'delay ([\d.]+)ms', result.stdout)
                    if match:
                        return float(match.group(1)) / 1000
        except:
            pass
        return 0.0

    def _measure_with_timestamp(self) -> float:
        """Measure latency using timestamps"""
        return 0.001  # Return a nominal 1ms latency as fallback

    def _get_interface_for_ip(self, ip: str) -> Optional[str]:
        """Get network interface name for given IP"""
        try:
            for interface in netifaces.interfaces():
                addresses = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addresses:
                    for addr in addresses[netifaces.AF_INET]:
                        if addr['addr'] == ip:
                            return interface
        except:
            pass
        return None

class NetworkMetricsCalculator:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.metrics_lock = threading.Lock()
        self.start_time = monotonic()
        
        # Initialize latency measurer
        self.latency_measurer = LatencyMeasurer()
        
        # Track metrics per UE
        self.ue_metrics: Dict[str, UEMetrics] = {}
        
        # UPF interface metrics
        self.upf_metrics = UEMetrics('ogstun', '10.45.0.1', window_size)
        
        # Interface monitoring
        self._monitor_thread = threading.Thread(target=self._monitor_interfaces, daemon=True)
        self._monitor_thread.start()
        
        # Initial interface scan
        self._scan_interfaces()

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
                # Scan for new interfaces periodically
                self._scan_interfaces()
                
                # Get current stats
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
            
            time.sleep(1)  # Sample every second

    def _calculate_jitter(self, ue_metrics: UEMetrics, current_latency: float):
        """Calculate jitter using RFC 3550 method"""
        if ue_metrics.latencies:
            last_latency = ue_metrics.latencies[-1]
            jitter = abs(current_latency - last_latency)
            
            if ue_metrics.jitter_values:
                # Moving average jitter calculation
                last_jitter = ue_metrics.jitter_values[-1]
                new_jitter = last_jitter + (jitter - last_jitter) / 16
            else:
                new_jitter = jitter
                
            ue_metrics.jitter_values.append(new_jitter)

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
            latency = self.latency_measurer.measure_latency(ue.ip)
            if latency > 0:
                ue.latencies.append(latency)
                self._calculate_jitter(ue, latency)
            
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

    def reset(self):
        """Reset all metrics"""
        with self.metrics_lock:
            self.start_time = monotonic()
            self.ue_metrics.clear()
            self.upf_metrics = UEMetrics('ogstun', '10.45.0.1', self.window_size)
            # Rescan interfaces to rebuild UE metrics
            self._scan_interfaces()

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