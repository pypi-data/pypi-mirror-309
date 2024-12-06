import socket
import json
import threading
import queue
import time
from typing import Optional, Tuple, Dict, Any, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class FrameData:
    chunks: list
    expected_chunks: int
    received_chunks: int

class TunnelHandler:
    def __init__(self, upf_ip: str = "10.45.0.1", upf_port: int = 5005):
        self.message_queues = {
            'default': queue.Queue(),
            'sensor': queue.Queue(),
            'stream': queue.Queue()
        }
        self.frame_data = {}
        self.chunk_size = 65000
        self.udp_socket = None
        self.running = False
        self.upf_ip = upf_ip
        self.upf_port = upf_port
        self.retry_count = 0
        self.max_retries = 5
        self.retry_delay = 2  # seconds
        
    def _setup_udp_socket(self) -> bool:
        """Setup UDP socket with retry mechanism"""
        while self.retry_count < self.max_retries:
            try:
                if self.udp_socket:
                    self.udp_socket.close()
                    
                self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # Set socket option for reuse
                self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.udp_socket.bind((self.upf_ip, self.upf_port))
                self.retry_count = 0  # Reset counter on successful bind
                return True
                
            except OSError as e:
                self.retry_count += 1
                logger.warning(f"Attempt {self.retry_count}/{self.max_retries} to bind socket failed: {e}")
                if self.retry_count < self.max_retries:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Failed to bind socket after {self.max_retries} attempts")
                    return False
                    
        return False
        
    def start(self) -> bool:
        """Start the tunnel handler with error handling"""
        if not self.running:
            if self._setup_udp_socket():
                self.running = True
                self.listener_thread = threading.Thread(target=self._udp_listener)
                self.listener_thread.daemon = True
                self.listener_thread.start()
                logger.info(f"TunnelHandler started on {self.upf_ip}:{self.upf_port}")
                return True
            else:
                logger.error("Failed to start TunnelHandler - socket binding failed")
                return False
        return True  # Already running

    def stop(self):
        """Stop the tunnel handler and cleanup"""
        self.running = False
        if self.udp_socket:
            try:
                self.udp_socket.close()
            except Exception as e:
                logger.error(f"Error closing UDP socket: {e}")
        logger.info("TunnelHandler stopped")
            
    def _udp_listener(self):
        while self.running:
            try:
                data, addr = self.udp_socket.recvfrom(65507)
                self._handle_received_data(data, addr[0])
            except Exception as e:
                if self.running:  # Only log if we're still meant to be running
                    logger.error(f"Error in UDP listener: {e}")
                
    def _handle_received_data(self, data: bytes, source_ip: str):
        try:
            # Try to decode as JSON first
            message = json.loads(data.decode())
            
            # Handle chunked data
            if isinstance(message, dict) and 'type' in message:
                if message['type'] == 'frame_header':
                    self.frame_data[source_ip] = FrameData([], message['chunks'], 0)
                    return
                elif message['type'] == 'frame_chunk':
                    chunk_data, _ = self.udp_socket.recvfrom(65507)
                    if source_ip in self.frame_data:
                        frame = self.frame_data[source_ip]
                        frame.chunks.append(chunk_data)
                        frame.received_chunks += 1
                        
                        if frame.received_chunks == frame.expected_chunks:
                            complete_data = b''.join(frame.chunks)
                            self._route_data(complete_data, source_ip)
                            del self.frame_data[source_ip]
                    return
            
            # If it's a regular JSON message, route it
            self._route_data(data, source_ip)
            
        except json.JSONDecodeError:
            # If it's not JSON, it might be binary data (like video stream)
            self._route_data(data, source_ip)
            
    def _route_data(self, data: bytes, source_ip: str):
        try:
            # Try to decode as JSON to check data type
            message = json.loads(data.decode())
            
            # Route based on message type
            if isinstance(message, dict):
                if 'type' in message:
                    if message['type'] == 'sensor':
                        self.message_queues['sensor'].put((data, source_ip))
                        return
                    elif message['type'] == 'stream':
                        self.message_queues['stream'].put((data, source_ip))
                        return
            
            # Default queue for regular JSON messages
            self.message_queues['default'].put((data, source_ip))
            
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Binary data goes to stream queue
            self.message_queues['stream'].put((data, source_ip))
            
    def send_data(self, data: Union[bytes, Dict, str], target_ip: str, target_port: int) -> bool:
        try:
            # Convert input to bytes if needed
            if isinstance(data, dict):
                data = json.dumps(data).encode()
            elif isinstance(data, str):
                data = data.encode()
                
            # Handle large data with chunking
            if len(data) > self.chunk_size:
                return self._send_chunked_data(data, target_ip, target_port)
            
            # Direct send for small data
            self.udp_socket.sendto(data, (target_ip, target_port))
            return True
            
        except Exception as e:
            logger.error(f"Error sending data: {e}")
            return False
            
    def _send_chunked_data(self, data: bytes, target_ip: str, target_port: int) -> bool:
        try:
            chunks = [data[i:i + self.chunk_size] 
                     for i in range(0, len(data), self.chunk_size)]
            
            # Send header
            header = json.dumps({
                "type": "frame_header",
                "chunks": len(chunks)
            }).encode()
            self.udp_socket.sendto(header, (target_ip, target_port))
            
            # Send chunks
            for i, chunk in enumerate(chunks):
                chunk_header = json.dumps({
                    "type": "frame_chunk",
                    "chunk_number": i,
                    "total_chunks": len(chunks)
                }).encode()
                
                self.udp_socket.sendto(chunk_header, (target_ip, target_port))
                self.udp_socket.sendto(chunk, (target_ip, target_port))
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending chunked data: {e}")
            return False
            
    def receive_data(self, queue_type: str = 'default', 
                    timeout: float = 0.1) -> Optional[Tuple[bytes, str]]:
        """
        Receive data from specified queue type
        Args:
            queue_type: 'default', 'sensor', or 'stream'
            timeout: How long to wait for data
        Returns:
            Tuple of (data, source_ip) or None if queue is empty
        """
        try:
            if queue_type not in self.message_queues:
                raise ValueError(f"Invalid queue type: {queue_type}")
                
            return self.message_queues[queue_type].get(timeout=timeout)
        except queue.Empty:
            return None