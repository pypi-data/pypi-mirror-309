import json
import yaml
import requests
import subprocess
import logging
from ruamel.yaml import YAML
import os
from urllib.parse import urljoin, urlparse
import shutil
from typing import Dict, Any, Optional, List, Union, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import time
from requests.exceptions import RequestException
from .exceptions import ConfigurationError, CommunicationError, ValidationError
from .tunnel_handler import TunnelHandler  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(value: Any, allowed_values: List[Any], field: str):
    if value not in allowed_values:
        raise ValidationError(f"Invalid value for {field}", field, value, allowed_values)

class AMBRDirection:
    def __init__(self, parent, direction: str):
        self.parent = parent
        self.direction = direction
        self.value: Optional[int] = None
        self.unit: Optional[int] = None

    def __call__(self, value: int, unit: int):
        validate_input(unit, [0, 1, 2, 3, 4], f"{self.direction} AMBR unit")
        self.value = value
        self.unit = unit
        return self

class AMBR:
    def __init__(self, parent):
        self.parent = parent
        self.downlink = AMBRDirection(self, 'downlink')
        self.uplink = AMBRDirection(self, 'uplink')

class QoS:
    def __init__(self, parent):
        self.parent = parent
        self.index: Optional[int] = None
        self.arp = ARP(self)

    def __call__(self, index: int):
        allowed_indices = [1, 2, 3, 4, 65, 66, 67, 75, 71, 72, 73, 74, 76, 5, 6, 7, 8, 9, 69, 70, 79, 80, 82, 83, 84, 85, 86]
        validate_input(index, allowed_indices, "QoS index")
        self.index = index
        return self

class ARP:
    def __init__(self, parent):
        self.parent = parent
        self.priority_level: Optional[int] = None
        self.pre_emption_vulnerability: Optional[int] = None
        self.pre_emption_capability: Optional[int] = None

    def __call__(self, priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int):
        validate_input(priority_level, range(1, 16), "ARP priority level")
        validate_input(pre_emption_vulnerability, [1, 2], "ARP pre-emption vulnerability")
        validate_input(pre_emption_capability, [1, 2], "ARP pre-emption capability")
        self.priority_level = priority_level
        self.pre_emption_vulnerability = pre_emption_vulnerability
        self.pre_emption_capability = pre_emption_capability
        return self

class PccRule:
    def __init__(self, parent):
        self.parent = parent
        self.qos = QoS(self)
        self.mbr = AMBR(self)
        self.gbr = AMBR(self)
        self.flow: List[Dict[str, Union[int, str]]] = []

    def add_flow(self, direction: int, description: str):
        validate_input(direction, [1, 2], "Flow direction")
        self.flow.append({"direction": direction, "description": description})

class Session:
    def __init__(self, parent, name: str):
        self.parent = parent
        self.name = name
        self.type: int = 1
        self.ambr = AMBR(self)
        self.qos = QoS(self)
        self.arp = ARP(self)
        self.pcc_rule: List[PccRule] = [PccRule(self), PccRule(self)]

    def set_type(self, session_type: int):
        validate_input(session_type, [1, 2, 3], "Session type")
        self.type = session_type

class Policy:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.config: Optional[Dict[str, Any]] = None
        self.sessions: Dict[str, Session] = {}
        self._last_modified_time: Optional[float] = None

    def _ensure_config_loaded(self, force_reload: bool = False):
        if not self.config_path:
            raise ConfigurationError("Configuration path not set")
        if not os.path.exists(self.config_path):
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")
        
        current_modified_time = os.path.getmtime(self.config_path)
        if force_reload or self.config is None or current_modified_time != self._last_modified_time:
            self.config = self._read_config()
            self._load_sessions()
            self._last_modified_time = current_modified_time

    def _read_config(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as file:
            return self.yaml.load(file)

    def _load_sessions(self):
        self.sessions.clear()
        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session_config in slice_config['session']:
                    session = Session(self, session_config['name'])
                    session.set_type(session_config['type'])
                    session.ambr.downlink(value=session_config['ambr']['downlink']['value'],
                                          unit=session_config['ambr']['downlink']['unit'])
                    session.ambr.uplink(value=session_config['ambr']['uplink']['value'],
                                        unit=session_config['ambr']['uplink']['unit'])
                    session.qos(index=session_config['qos']['index'])
                    session.qos.arp(priority_level=session_config['qos']['arp']['priority_level'],
                                    pre_emption_vulnerability=session_config['qos']['arp']['pre_emption_vulnerability'],
                                    pre_emption_capability=session_config['qos']['arp']['pre_emption_capability'])
                    
                    for i, pcc_rule_config in enumerate(session_config.get('pcc_rule', [])):
                        if i < len(session.pcc_rule):
                            pcc_rule = session.pcc_rule[i]
                            pcc_rule.qos(index=pcc_rule_config['qos']['index'])
                            pcc_rule.qos.arp(priority_level=pcc_rule_config['qos']['arp']['priority_level'],
                                             pre_emption_vulnerability=pcc_rule_config['qos']['arp']['pre_emption_vulnerability'],
                                             pre_emption_capability=pcc_rule_config['qos']['arp']['pre_emption_capability'])
                            pcc_rule.mbr.downlink(value=pcc_rule_config['qos']['mbr']['downlink']['value'],
                                                  unit=pcc_rule_config['qos']['mbr']['downlink']['unit'])
                            pcc_rule.mbr.uplink(value=pcc_rule_config['qos']['mbr']['uplink']['value'],
                                                unit=pcc_rule_config['qos']['mbr']['uplink']['unit'])
                            pcc_rule.gbr.downlink(value=pcc_rule_config['qos']['gbr']['downlink']['value'],
                                                  unit=pcc_rule_config['qos']['gbr']['downlink']['unit'])
                            pcc_rule.gbr.uplink(value=pcc_rule_config['qos']['gbr']['uplink']['value'],
                                                unit=pcc_rule_config['qos']['gbr']['uplink']['unit'])
                            for flow in pcc_rule_config['flow']:
                                pcc_rule.add_flow(flow['direction'], flow['description'])
                    
                    self.sessions[session.name] = session

    def set_config_path(self, config_path: str):
        self.config_path = config_path
        self._ensure_config_loaded(force_reload=True)

    def session(self, name: str) -> Session:
        self._ensure_config_loaded()
        if name not in self.sessions:
            self.sessions[name] = Session(self, name)
        return self.sessions[name]

    def add_session(self, name: str) -> Session:
        self._ensure_config_loaded()
        if name in self.sessions:
            raise ConfigurationError(f"Session '{name}' already exists")
        
        new_session = Session(self, name)
        self.sessions[name] = new_session

        new_session_config = {
            'name': name,
            'type': 1,
            'ambr': {
                'downlink': {'value': 1, 'unit': 0},
                'uplink': {'value': 1, 'unit': 0}
            },
            'qos': {
                'index': 9,
                'arp': {
                    'priority_level': 8,
                    'pre_emption_vulnerability': 1,
                    'pre_emption_capability': 1
                }
            },
            'pcc_rule': [
                {
                    'qos': {
                        'index': 9,
                        'arp': {
                            'priority_level': 8,
                            'pre_emption_vulnerability': 1,
                            'pre_emption_capability': 1
                        },
                        'mbr': {
                            'downlink': {'value': 1, 'unit': 0},
                            'uplink': {'value': 1, 'unit': 0}
                        },
                        'gbr': {
                            'downlink': {'value': 1, 'unit': 0},
                            'uplink': {'value': 1, 'unit': 0}
                        }
                    },
                    'flow': [
                        {'direction': 2, 'description': 'permit out ip from any to assigned'},
                        {'direction': 1, 'description': 'permit out ip from any to assigned'}
                    ]
                }
            ]
        }

        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                slice_config['session'].append(new_session_config)
                break
        
        return new_session

    def remove_session(self, name: str):
        self._ensure_config_loaded()
        if name not in self.sessions:
            raise ConfigurationError(f"Session '{name}' does not exist")
        
        del self.sessions[name]

        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                slice_config['session'] = [s for s in slice_config['session'] if s['name'] != name]

    def list_sessions(self) -> List[str]:
        self._ensure_config_loaded()
        return list(self.sessions.keys())

    def rename_session(self, old_name: str, new_name: str):
        self._ensure_config_loaded()
        if old_name not in self.sessions:
            raise ConfigurationError(f"Session '{old_name}' does not exist")
        if new_name in self.sessions:
            raise ConfigurationError(f"Session '{new_name}' already exists")
        
        self.sessions[new_name] = self.sessions.pop(old_name)
        self.sessions[new_name].name = new_name

        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    if session['name'] == old_name:
                        session['name'] = new_name
                        return 

    def get_session_details(self, name: str) -> Dict[str, Any]:
        self._ensure_config_loaded()
        if name not in self.sessions:
            raise ConfigurationError(f"Session '{name}' does not exist")
        
        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session in slice_config['session']:
                    if session['name'] == name:
                        return session
        
        raise ConfigurationError(f"Session '{name}' not found in configuration")

    def update_config(self):
        self._ensure_config_loaded()
        for policy in self.config['pcf']['policy']:
            for slice_config in policy['slice']:
                for session_config in slice_config['session']:
                    if session_config['name'] in self.sessions:
                        session = self.sessions[session_config['name']]
                        
                        if 'type' in session_config:
                            session_config['type'] = session.type
                        
                        if 'ambr' in session_config:
                            if 'downlink' in session_config['ambr']:
                                if session.ambr.downlink.value is not None:
                                    session_config['ambr']['downlink']['value'] = session.ambr.downlink.value
                                if session.ambr.downlink.unit is not None:
                                    session_config['ambr']['downlink']['unit'] = session.ambr.downlink.unit
                            if 'uplink' in session_config['ambr']:
                                if session.ambr.uplink.value is not None:
                                    session_config['ambr']['uplink']['value'] = session.ambr.uplink.value
                                if session.ambr.uplink.unit is not None:
                                    session_config['ambr']['uplink']['unit'] = session.ambr.uplink.unit
                        
                        if 'qos' in session_config:
                            if session.qos.index is not None:
                                session_config['qos']['index'] = session.qos.index
                            if 'arp' in session_config['qos']:
                                if session.qos.arp.priority_level is not None:
                                    session_config['qos']['arp']['priority_level'] = session.qos.arp.priority_level
                                if session.qos.arp.pre_emption_vulnerability is not None:
                                    session_config['qos']['arp']['pre_emption_vulnerability'] = session.qos.arp.pre_emption_vulnerability
                                if session.qos.arp.pre_emption_capability is not None:
                                    session_config['qos']['arp']['pre_emption_capability'] = session.qos.arp.pre_emption_capability

                        if 'pcc_rule' in session_config:
                            for i, pcc_rule_config in enumerate(session_config['pcc_rule']):
                                if i < len(session.pcc_rule):
                                    pcc_rule = session.pcc_rule[i]
                                    if 'qos' in pcc_rule_config:
                                        if pcc_rule.qos.index is not None:
                                            pcc_rule_config['qos']['index'] = pcc_rule.qos.index
                                        if 'arp' in pcc_rule_config['qos']:
                                            if pcc_rule.qos.arp.priority_level is not None:
                                                pcc_rule_config['qos']['arp']['priority_level'] = pcc_rule.qos.arp.priority_level
                                            if pcc_rule.qos.arp.pre_emption_vulnerability is not None:
                                                pcc_rule_config['qos']['arp']['pre_emption_vulnerability'] = pcc_rule.qos.arp.pre_emption_vulnerability
                                            if pcc_rule.qos.arp.pre_emption_capability is not None:
                                                pcc_rule_config['qos']['arp']['pre_emption_capability'] = pcc_rule.qos.arp.pre_emption_capability
                                        if 'mbr' in pcc_rule_config['qos']:
                                            if 'downlink' in pcc_rule_config['qos']['mbr']:
                                                if pcc_rule.mbr.downlink.value is not None:
                                                    pcc_rule_config['qos']['mbr']['downlink']['value'] = pcc_rule.mbr.downlink.value
                                                if pcc_rule.mbr.downlink.unit is not None:
                                                    pcc_rule_config['qos']['mbr']['downlink']['unit'] = pcc_rule.mbr.downlink.unit
                                            if 'uplink' in pcc_rule_config['qos']['mbr']:
                                                if pcc_rule.mbr.uplink.value is not None:
                                                    pcc_rule_config['qos']['mbr']['uplink']['value'] = pcc_rule.mbr.uplink.value
                                                if pcc_rule.mbr.uplink.unit is not None:
                                                    pcc_rule_config['qos']['mbr']['uplink']['unit'] = pcc_rule.mbr.uplink.unit
                                        if 'gbr' in pcc_rule_config['qos']:
                                            if 'downlink' in pcc_rule_config['qos']['gbr']:
                                                if pcc_rule.gbr.downlink.value is not None:
                                                    pcc_rule_config['qos']['gbr']['downlink']['value'] = pcc_rule.gbr.downlink.value
                                                if pcc_rule.gbr.downlink.unit is not None:
                                                    pcc_rule_config['qos']['gbr']['downlink']['unit'] = pcc_rule.gbr.downlink.unit
                                            if 'uplink' in pcc_rule_config['qos']['gbr']:
                                                if pcc_rule.gbr.uplink.value is not None:
                                                    pcc_rule_config['qos']['gbr']['uplink']['value'] = pcc_rule.gbr.uplink.value
                                                if pcc_rule.gbr.uplink.unit is not None:
                                                    pcc_rule_config['qos']['gbr']['uplink']['unit'] = pcc_rule.gbr.uplink.unit
                                    if pcc_rule.flow:
                                        pcc_rule_config['flow'] = pcc_rule.flow

        with open(self.config_path, 'w') as file:
            self.yaml.dump(self.config, file)
            
class CommunicationInterface:
    def __init__(self, base_url: str):
        if ':' in base_url:
            base_parts = base_url.rsplit(':', 1)
            self.base_url = base_parts[0]
            self.base_port = int(base_parts[1])
        else:
            self.base_url = base_url
            self.base_port = None

    def send_data(self, endpoint: str, data: Dict[str, Any], port_offset: int = 0) -> Dict[str, Any]:
        try:
            url = self.base_url
            if self.base_port:
                port = self.base_port + port_offset
                url = f"{url}:{port}"
            
            response = requests.post(f"{url}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise CommunicationError(f"Error sending data: {str(e)}", endpoint=endpoint)

    def receive_data(self, endpoint: str) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}:{self.base_port}" if self.base_port else self.base_url
            response = requests.get(f"{url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise CommunicationError(f"Error receiving data: {str(e)}", endpoint=endpoint)

class UEInterface(CommunicationInterface):
    pass

class UPFInterface(CommunicationInterface):
    pass

class Open5GS:
    _instance = None
    _update_pcf_complete = False
    _update_config_complete = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Open5GS, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.policy = Policy()
        self.ue_base_url = "http://10.10.0.132:8080"
        self.upf_base_url = "http://10.10.0.112:8081"
        self.env_path = None
        self._env_config = None
        self._last_env_modified_time = None
        self.tunnel_handler = TunnelHandler(upf_ip="10.45.0.1", upf_port=5005)
        self.tunnel_handler.start()
        logger.info("TunnelHandler initialized and started")
        self.interface_ready = False
        self.max_interface_wait = 60

    def set_config_path(self, config_path: str):
        self.policy.set_config_path(config_path)

    def reload_config(self):
        self.policy._ensure_config_loaded(force_reload=True)

    def set_env_path(self, env_path: str):
        if not os.path.exists(env_path):
            raise ConfigurationError(f"Environment file not found: {env_path}")
        self.env_path = env_path
        self._ensure_env_loaded()

    def _ensure_env_loaded(self, force_reload: bool = False):
        if not self.env_path:
            raise ConfigurationError("Environment file path not set")
        
        current_modified_time = os.path.getmtime(self.env_path)
        if (force_reload or self._env_config is None or 
            current_modified_time != self._last_env_modified_time):
            self._env_config = self._read_env_file()
            self._last_env_modified_time = current_modified_time

    def _read_env_file(self) -> Dict[str, str]:
        env_config = {}
        try:
            with open(self.env_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            env_config[key.strip()] = value.strip()
                        except ValueError:
                            continue
            return env_config
        except Exception as e:
            raise ConfigurationError(f"Failed to read environment file: {str(e)}")

    def _write_env_file(self):
        try:
            with open(self.env_path, 'w') as file:
                for key, value in self._env_config.items():
                    file.write(f"{key}={value}\n")
        except Exception as e:
            raise ConfigurationError(f"Failed to write environment file: {str(e)}")

    def get_num_ues(self) -> int:
        self._ensure_env_loaded()
        try:
            return int(self._env_config.get('NUM_UES', 1))
        except ValueError:
            logger.warning("Invalid NUM_UES value in .env file, defaulting to 1")
            return 1

    def set_num_ues(self, num_ues: int):
        if self._update_config_complete:
            raise ConfigurationError(
                "Cannot modify NUM_UES after update_config() has been called. "
                "Please set NUM_UES before calling update_config()."
            )

        if not isinstance(num_ues, int) or num_ues < 1:
            raise ValueError("Number of UEs must be a positive integer")

        self._ensure_env_loaded()
        self._env_config['NUM_UES'] = str(num_ues)
        self._write_env_file()
        logger.info(f"Updated NUM_UES to {num_ues}")

    def reload_env(self):
        if not self.env_path:
            raise ConfigurationError("Environment file path not set")
        self._ensure_env_loaded(force_reload=True)
        logger.info("Environment configuration reloaded successfully")

    def reload_env_config(self):
        self.reload_env()

    def ue(self, endpoint: str) -> str:
        return urljoin(self.ue_base_url, endpoint)

    def upf(self, endpoint: str) -> str:
        return urljoin(self.upf_base_url, endpoint)
    
    def _check_tunnel_status(self) -> Tuple[bool, Optional[str]]:
        """Check if tunnel interfaces are properly set up"""
        try:
            result = subprocess.run(
                ["docker", "exec", "ue", "python3", "-c", "import netifaces; print(len([i for i in netifaces.interfaces() if i.startswith('uesimtun')]))"],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip() == "0":
                return False, "No TUN interfaces found"
            return True, None
            
        except Exception as e:
            return False, f"Error checking tunnel interfaces: {str(e)}"

    def is_tunnel_ready(self) -> bool:
        """Check if tunnel communication is ready"""
        tunnel_status, error = self._check_tunnel_status()
        if not tunnel_status:
            logger.error(f"Tunnel not ready: {error}")
            return False
        return True

    def _parse_endpoint_type(self, endpoint: str) -> str:
        """Determine the type of data based on the endpoint"""
        if 'sensor' in endpoint:
            return 'sensor'
        elif 'stream' in endpoint or 'video' in endpoint:
            return 'stream'
        return 'default'
    
    def _wait_for_interfaces(self, timeout: int = 60) -> bool:
        """Wait for TUN interfaces using ip command"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Use 'ip link' command instead of Python module
                result = subprocess.run(
                    ["docker", "exec", "ue", "ip", "link", "show"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Count TUN interfaces from ip link output
                tun_interfaces = [
                    line for line in result.stdout.split('\n')
                    if 'uesimtun' in line
                ]
                
                num_interfaces = len(tun_interfaces)
                if num_interfaces > 0:
                    logger.info(f"Found {num_interfaces} TUN interfaces")
                    self.interface_ready = True
                    return True
                    
                logger.debug("Waiting for TUN interfaces...")
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error checking interfaces: {e}")
                time.sleep(2)
                
        return False
    
    def get_ue_ips(self) -> List[Dict[str, Any]]:
        """Get list of available UE IPs using ip addr command"""
        if not self.interface_ready and not self._wait_for_interfaces(self.max_interface_wait):
            logger.error("Timed out waiting for TUN interfaces")
            return []
            
        try:
            # Use 'ip addr' command to get interface IPs
            result = subprocess.run(
                ["docker", "exec", "ue", "ip", "addr", "show"],
                capture_output=True,
                text=True,
                check=True
            )
            
            interfaces = []
            current_iface = None
            
            for line in result.stdout.split('\n'):
                if 'uesimtun' in line:
                    # Extract interface name
                    current_iface = line.split(':')[1].strip()
                elif current_iface and 'inet' in line and not 'inet6' in line:
                    # Extract IP address
                    ip = line.strip().split()[1].split('/')[0]
                    interfaces.append({
                        'ip': ip,
                        'interface': current_iface,
                        'port': self._get_port_for_interface(current_iface),
                        'port_offset': self._get_port_offset(current_iface)
                    })
                    current_iface = None
            
            return interfaces
                
        except Exception as e:
            logger.error(f"Error getting UE IPs: {e}")
            return []

    def _get_port_for_interface(self, interface: str) -> int:
        """Get port number from interface name"""
        try:
            # Extract number from uesimtun<n>
            index = int(''.join(filter(str.isdigit, interface)))
            return 8080 + index
        except ValueError:
            return 8080

    def _get_port_offset(self, interface: str) -> int:
        """Get port offset from interface name"""
        try:
            return int(''.join(filter(str.isdigit, interface)))
        except ValueError:
            return 0

    def verify_ue_ready(self, ue_index: int = 0) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Verify if a specific UE is ready
        Args:
            ue_index: Index of the UE to verify
        Returns:
            Tuple of (is_ready, error_message, ue_info)
        """
        ue_ips = self.get_ue_ips()
        if not ue_ips:
            return False, "No UE interfaces found", None
            
        if ue_index >= len(ue_ips):
            return False, f"UE index {ue_index} out of range", None
            
        return True, None, ue_ips[ue_index]
    
    def verify_ue_ready(self, ue_index: int = 0) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """Verify if a specific UE is ready with interface waiting"""
        # Wait for interfaces if not ready
        if not self.interface_ready and not self._wait_for_interfaces(self.max_interface_wait):
            return False, "Timed out waiting for TUN interfaces", None
            
        ue_ips = self.get_ue_ips()
        if not ue_ips:
            return False, "No UE interfaces found", None
            
        if ue_index >= len(ue_ips):
            return False, f"UE index {ue_index} out of range (max: {len(ue_ips)-1})", None
            
        return True, None, ue_ips[ue_index]

    def send_data(self, url: str, data: Dict[str, Any], port_offset: int = 0) -> Dict[str, Any]:
        """Enhanced send_data with automatic UE verification"""
        try:
            if not self._ensure_tunnel_handler():
                raise CommunicationError("TunnelHandler is not running and failed to start", endpoint=url)

            is_ue_endpoint = self.ue_base_url in url
            
            if is_ue_endpoint:
                # Verify UE is ready for the given port offset
                is_ready, error, ue_info = self.verify_ue_ready(port_offset)
                if not is_ready:
                    raise CommunicationError(f"UE not ready: {error}", endpoint=url)
                
                # Update data with UE info
                if isinstance(data, dict):
                    data.update({
                        'ue_ip': ue_info['ip'],
                        'port': ue_info['port']
                    })

            # Rest of the send_data implementation remains the same
            parsed_url = urlparse(url)
            endpoint_type = self._parse_endpoint_type(parsed_url.path)
            if isinstance(data, dict) and 'type' not in data:
                data['type'] = endpoint_type

            # Determine target details
            if is_ue_endpoint:
                target_ip = "10.45.0.1"  # UPF IP
                target_port = 5005       # UPF port
            else:
                parsed_url = urlparse(url)
                host_parts = parsed_url.netloc.split(':')
                target_ip = host_parts[0]
                target_port = int(host_parts[1]) if len(host_parts) > 1 else 80

            # Send through tunnel
            success = self.tunnel_handler.send_data(data, target_ip, target_port)
            
            if success:
                return {"status": "success", "message": "Data sent successfully"}
            else:
                raise CommunicationError("Failed to send data through tunnel", endpoint=url)

        except Exception as e:
            logger.error(f"Error sending data: {str(e)}")
            raise CommunicationError(f"Error sending data: {str(e)}", endpoint=url)

    def receive_data(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Receive data from the tunnel"""
        try:
            data_type = self._parse_endpoint_type(endpoint)
            result = self.tunnel_handler.receive_data(data_type)
            
            if result is None:
                return None
                
            data, source_ip = result
            
            try:
                if isinstance(data, bytes):
                    json_data = json.loads(data.decode())
                else:
                    json_data = data
                    
                if isinstance(json_data, dict):
                    json_data.update({
                        "source_ip": source_ip,
                        "timestamp": time.time(),
                        "endpoint": endpoint
                    })
                return json_data
                
            except (json.JSONDecodeError, UnicodeDecodeError):
                return {
                    "data": data,
                    "source_ip": source_ip,
                    "timestamp": time.time(),
                    "endpoint": endpoint
                }
                
        except Exception as e:
            logger.error(f"Error receiving data: {str(e)}")
            raise CommunicationError(f"Error receiving data: {str(e)}", endpoint=endpoint)

    def list_sessions(self) -> List[str]:
        return self.policy.list_sessions()

    def rename_session(self, old_name: str, new_name: str):
        self.policy.rename_session(old_name, new_name)

    def get_session_details(self, name: str) -> Dict[str, Any]:
        return self.policy.get_session_details(name)

    def update_pcf(self):
        self.policy.update_config()
        self._update_pcf_complete = True
        logger.info("PCF YAML file updated successfully")

    def update_config(self):
        """Enhanced update_config with interface waiting"""
        if not self.env_path:
            logger.warning("Environment file path not set. NUM_UES configuration may not be applied.")
        
        # Stop tunnel handler before restart
        if hasattr(self, 'tunnel_handler'):
            self.tunnel_handler.stop()
        
        self._restart_pcf_service()
        
        # Reset interface ready flag
        self.interface_ready = False
        
        # Wait for interfaces after restart
        if not self._wait_for_interfaces(self.max_interface_wait):
            logger.warning("Timed out waiting for interfaces after restart")
        
        # Restart tunnel handler
        self.tunnel_handler = TunnelHandler(upf_ip="10.45.0.1", upf_port=5005)
        self.tunnel_handler.start()
        
        self._update_config_complete = True
        logger.info("Configuration updated and tunnel handler restarted")

    def _restart_pcf_service(self):
        try:
            result = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
            if result.stdout.strip():
                logger.info("Existing Docker containers found. Tearing down...")
                subprocess.run(["docker", "compose", "down", "-t", "1", "-v"], check=True)
            else:
                logger.info("No running Docker containers found.")

            logger.info("Bringing up Docker deployment...")
            subprocess.run(["docker", "compose", "up", "-d"], check=True)
            logger.info("PCF service restarted successfully")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to restart PCF service: {str(e)}")
            raise ConfigurationError(f"Failed to restart PCF service: {str(e)}")
        
    def run_background_nodes(self):
        """
        Maintained for backward compatibility.
        Now just checks if tunnel is ready.
        """
        logger.info("Checking tunnel status")
        if self.is_tunnel_ready():
            self._run_background_nodes_complete = True
            logger.info("Tunnel is ready")
            return True
        else:
            self._run_background_nodes_complete = False
            logger.error("Tunnel is not ready")
            return False
        
    def is_update_pcf_complete(self) -> bool:
        return self._update_pcf_complete

    def is_update_config_complete(self) -> bool:
        return self._update_config_complete

    def is_run_background_nodes_complete(self) -> bool:
        """Now checks if tunnel communication is ready"""
        return self.is_tunnel_ready()

    def get_background_process_status(self) -> Dict[str, Any]:
        """
        Maintained for backward compatibility.
        Now returns tunnel status instead of API status.
        """
        tunnel_ready, error = self._check_tunnel_status()
        return {
            'completed': tunnel_ready,
            'ue_api_ready': tunnel_ready,  # Maintained for compatibility
            'upf_api_ready': tunnel_ready, # Maintained for compatibility
            'error_message': error if not tunnel_ready else None
        }
    
    def _monitor_background_processes(self, timeout: int = 60):
        """
        Maintained for backward compatibility.
        Now just monitors tunnel status.
        """
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            tunnel_ready, error = self._check_tunnel_status()
            if tunnel_ready:
                self._run_background_nodes_complete = True
                return
            time.sleep(1)

        # If we get here, we've timed out
        self._background_process_status['error_message'] = "Timeout waiting for tunnel to be ready"
        logger.error(self._background_process_status['error_message'])

    def _check_wireshark_installed(self) -> bool:
        paths = ["/usr/bin/wireshark", "/usr/local/bin/wireshark"]
        return any(os.path.exists(path) for path in paths)
    
    def _check_ue_interfaces(self) -> Tuple[bool, Optional[str]]:
        """
        Maintained for backward compatibility.
        Now just checks tunnel interfaces.
        """
        return self._check_tunnel_status()

    def _check_upf_api(self) -> Tuple[bool, Optional[str]]:
        """
        Maintained for backward compatibility.
        Now always returns tunnel status.
        """
        tunnel_ready, error = self._check_tunnel_status()
        if tunnel_ready:
            return True, None
        return False, error
        
    def _get_interface_name(self, ip_address: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ["ip", "-o", "addr", "show"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if ip_address in line:
                    return line.split()[1]
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Error getting interface name: {str(e)}")
            return None

    def _get_display_environment(self) -> dict:
        """Get environment variables needed for GUI applications"""
        env = os.environ.copy()
        if 'DISPLAY' not in env:
            env['DISPLAY'] = ':0'
        
        try:
            subprocess.run(['xhost', '+'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            pass
        
        return env

    def launch_wireshark(self, 
                        ip_address: str = "10.10.0.1", 
                        display_filter: str = "gtp",
                        capture_filter: Optional[str] = None) -> bool:
        try:
            wireshark_cmd = "/usr/bin/wireshark"
            if not os.path.exists(wireshark_cmd):
                raise ConfigurationError("Wireshark not found. Please install via: sudo apt install wireshark")
                
            logger.info(f"Using Wireshark from: {wireshark_cmd}")
            
            interface_name = self._get_interface_name(ip_address)
            if not interface_name:
                raise ConfigurationError(f"No interface found with IP address {ip_address}")
            
            command = [wireshark_cmd, "-i", interface_name, "-k"]
            if display_filter:
                command.extend(["-Y", display_filter])
            if capture_filter:
                command.extend(["-f", capture_filter])
                
            clean_env = {
                'DISPLAY': os.environ.get('DISPLAY', ':0'),
                'HOME': os.environ.get('HOME', ''),
                'USER': os.environ.get('USER', ''),
                'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
                'XAUTHORITY': os.environ.get('XAUTHORITY', ''),
                'LANG': os.environ.get('LANG', 'en_US.UTF-8'),
                'LC_ALL': 'C'
            }
            
            if 'LD_LIBRARY_PATH' in clean_env:
                paths = clean_env['LD_LIBRARY_PATH'].split(':')
                clean_paths = [p for p in paths if 'snap' not in p.lower()]
                if clean_paths:
                    clean_env['LD_LIBRARY_PATH'] = ':'.join(clean_paths)
                
            try:
                subprocess.run(['xhost', '+local:'], check=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
            except Exception as e:
                logger.warning(f"Could not set xhost permissions: {e}")
                
            process = subprocess.Popen(
                command,
                env=clean_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            time.sleep(1)  
            
            if process.poll() is None:  
                logger.info(f"Wireshark launched successfully on interface {interface_name}")
                return True
            else:
                stdout, stderr = process.communicate()
                error_msg = (f"Wireshark failed to start.\n"
                            f"Command: {' '.join(command)}\n"
                            f"Environment: {clean_env}\n"
                            f"stdout: {stdout.decode()}\n"
                            f"stderr: {stderr.decode()}")
                raise ConfigurationError(error_msg)
                
        except Exception as e:
            error_msg = f"Failed to launch Wireshark: {str(e)}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

    def launch_gtp_wireshark(self) -> bool:
        try:
            return self.launch_wireshark(
                ip_address="10.10.0.1",
                display_filter="gtp"  # Simple GTP filter
            )
        except Exception as e:
            logger.error(f"Failed to launch GTP Wireshark: {e}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'tunnel_handler'):
            self.tunnel_handler.stop()
            logger.info("TunnelHandler stopped")

# Global instance
open5gs = Open5GS()

