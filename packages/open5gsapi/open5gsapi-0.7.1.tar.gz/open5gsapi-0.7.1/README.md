# Open5GS API

This package provides a Python API for interacting with Open5GS components and managing PCF configurations.

## Usage

First, import the package and set the configuration paths:

```python
from open5gsapi import open5gs

# Sets the PCF configuration file path
open5gs.set_config_path('/path/to/pcf.yaml')
```
```python
# Sets the UERANSIM configuration file path
open5gs.set_env_path('/path/to/.env')
```

If the configuration files are edited manually after loading:

```python
# Explicitly reload the configurations
open5gs.reload_config()  # Reload PCF configuration
open5gs.reload_env()     # Reload environment configuration
```

### UE Configuration

#### Setting Number of UEs

```python
# Get current number of UEs
current_ues = open5gs.get_num_ues()
print(f"Current number of UEs: {current_ues}")

# Set new number of UEs (must be done before update_config())
open5gs.set_num_ues(3)
```

### Network Traffic Analysis

#### Launching Wireshark

```python
# Launch Wireshark with default GTP filtering
open5gs.launch_gtp_wireshark()

# Launch with custom filters
open5gs.launch_wireshark(
    ip_address="10.10.0.1",
    display_filter="gtp && ip.addr == 10.10.0.1",
    capture_filter="port 2123 or port 2152"
)
```

### UE and UPF Operations

#### Getting API URLs

```python
# Get UE API URL
UE_API_URL = open5gs.ue("send")
# Result: "http://10.10.0.132:8080/send"

# Get UPF API URL
UPF_API_URL = open5gs.upf("receive/sensor")
# Result: "http://10.10.0.112:8081/receive/sensor"
```

#### Sending and Receiving Data

```python
# Send data
data = {"sensor_id": 1, "temperature": 25.5, "humidity": 60}
response = open5gs.send_data(UE_API_URL, data)

# Receive data
received_data = open5gs.receive_data(UPF_API_URL)
```

### PCF Configuration Management

#### Listing and Viewing Sessions

```python
# List all sessions
sessions = open5gs.list_sessions()
print("Current sessions:", sessions)

# Get details of a specific session
session_name = "video-streaming"
session_details = open5gs.get_session_details(session_name)
print(f"Details of session '{session_name}':", session_details)
```

#### Modifying Session Parameters

```python
# Modify session parameters
session = open5gs.policy.session('video-streaming')
session.ambr.downlink(value=10000000, unit=1)
session.ambr.uplink(value=20000000, unit=1)
session.qos(index=5)
session.arp(priority_level=7, pre_emption_vulnerability=2, pre_emption_capability=1)

# Modify PCC rule parameters
session.pcc_rule[0].qos(index=3)
session.pcc_rule[0].mbr.downlink(value=2000000, unit=1)
session.pcc_rule[0].gbr.uplink(value=1000000, unit=1)
session.pcc_rule[0].add_flow(direction=2, description="permit out ip from any to assigned")
```

#### Managing Sessions

```python
# Add a new session
new_session = open5gs.policy.add_session('new-session-name')
new_session.ambr.downlink(value=5000000, unit=1)
new_session.ambr.uplink(value=1000000, unit=1)

# Remove a session
open5gs.policy.remove_session('session-to-remove')

# Rename a session
open5gs.rename_session('old-session-name', 'new-session-name')
```

#### Updating Configuration

After making changes to the configuration, you need to update the system:

```python
# Update PCF YAML file
open5gs.update_pcf()

# Tear down and redeploy containers with new configuration
open5gs.update_config()

# Run initialization scripts and start background processes
open5gs.run_background_nodes()
```

You can check the status of these operations:

```python
# Check completion status
if open5gs.is_update_pcf_complete():
    print("PCF update complete")

if open5gs.is_update_config_complete():
    print("Configuration update complete")

# Check background nodes status
if open5gs.is_run_background_nodes_complete():
    print("Background nodes are running")
else:
    status = open5gs.get_background_process_status()
    print(f"Background process status: {status}")
```

## API Reference

### Configuration Management

- `open5gs.set_config_path(path: str)`: Set the PCF configuration file path
- `open5gs.set_env_path(path: str)`: Set the environment file path
- `open5gs.reload_config()`: Reload the PCF configuration
- `open5gs.reload_env()`: Reload the environment configuration
- `open5gs.get_num_ues() -> int`: Get current number of UEs
- `open5gs.set_num_ues(num_ues: int)`: Set number of UEs

### Network Analysis

- `open5gs.launch_wireshark(ip_address: str, display_filter: str, capture_filter: str) -> bool`: Launch Wireshark with custom filters
- `open5gs.launch_gtp_wireshark() -> bool`: Launch Wireshark with GTP filtering

### UE and UPF Operations

- `open5gs.ue(endpoint: str) -> str`: Get the UE API URL
- `open5gs.upf(endpoint: str) -> str`: Get the UPF API URL
- `open5gs.send_data(url: str, data: Any) -> Dict[str, Any]`: Send data to the specified URL
- `open5gs.receive_data(url: str) -> Any`: Receive data from the specified URL

### PCF Configuration Management

- `open5gs.list_sessions() -> List[str]`: Get a list of all session names
- `open5gs.get_session_details(name: str) -> Dict[str, Any]`: Get details of a specific session
- `open5gs.rename_session(old_name: str, new_name: str)`: Rename a session
- `open5gs.policy.session(name: str) -> Session`: Get or create a session
- `open5gs.policy.add_session(name: str) -> Session`: Add a new session
- `open5gs.policy.remove_session(name: str)`: Remove a session

#### Session Methods

- `session.ambr.downlink(value: int, unit: int)`: Set downlink AMBR
- `session.ambr.uplink(value: int, unit: int)`: Set uplink AMBR
- `session.qos(index: int)`: Set QoS index
- `session.arp(priority_level: int, pre_emption_vulnerability: int, pre_emption_capability: int)`: Set ARP parameters

#### PCC Rule Methods

- `session.pcc_rule[index].qos(index: int)`: Set QoS index for a PCC rule
- `session.pcc_rule[index].mbr.downlink(value: int, unit: int)`: Set downlink MBR for a PCC rule
- `session.pcc_rule[index].mbr.uplink(value: int, unit: int)`: Set uplink MBR for a PCC rule
- `session.pcc_rule[index].gbr.downlink(value: int, unit: int)`: Set downlink GBR for a PCC rule
- `session.pcc_rule[index].gbr.uplink(value: int, unit: int)`: Set uplink GBR for a PCC rule
- `session.pcc_rule[index].add_flow(direction: int, description: str)`: Add a flow to a PCC rule

### Configuration Update

- `open5gs.update_pcf()`: Update the PCF YAML file
- `open5gs.update_config()`: Tear down and redeploy containers with new configuration
- `open5gs.run_background_nodes()`: Run initialization scripts and start background processes in UE and UPF containers

### Background Process Management

- `open5gs.is_run_background_nodes_complete() -> bool`: Check if background nodes are running
- `open5gs.get_background_process_status() -> Dict[str, Any]`: Get detailed status of background processes

## Error Handling

This API uses custom exception classes to handle various error scenarios. When using the API, you may catch the following exceptions:

### ConfigurationError

Raised when there are issues related to the overall configuration of the Open5GS system. It may occur in the following scenarios:

- The configuration file (pcf.yaml) cannot be found or read.
- The environment file (.env) cannot be found or read.
- There are structural problems with the configuration files.
- Unable to initialize or access necessary components of the Open5GS system.
- Attempting to access or modify a non-existent session.
- Failing to restart the PCF service.
- Attempting to modify NUM_UES after update_config() has been called.
- Wireshark is not installed when attempting to launch packet capture.

Example usage:
```python
try:
    open5gs.set_config_path('/path/to/pcf.yaml')
    open5gs.set_env_path('/path/to/.env')
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Handle the error (e.g., exit the program or use a default configuration)
```

### ValidationError

Raised when the input values provided for specific configuration parameters are invalid or out of the allowed range. It typically occurs when:

- Setting an invalid QoS index.
- Providing an out-of-range value for AMBR.
- Using an incorrect value for ARP parameters.
- Setting an invalid session type.
- Adding an invalid flow direction in PCC rules.
- Setting an invalid number of UEs (must be positive integer).
- Providing invalid Wireshark filter expressions.

Example usage:
```python
try:
    session = open5gs.policy.session('internet')
    session.qos(index=100)  # 100 is not a valid QoS index
    open5gs.set_num_ues(0)  # 0 is not a valid number of UEs
except ValidationError as e:
    print(f"Validation error: {e}")
    # Handle the error (e.g., use a default value or prompt the user for valid input)
```

### CommunicationError

Raised when there are issues communicating with the UE or UPF components. It may occur when:

- Sending data to the UE API fails.
- Receiving data from the UPF API fails.
- Unable to establish connection with Wireshark for packet capture.
- Background nodes (UE/UPF) fail to start or become unresponsive.
- TUN interfaces are not properly set up for UE communication.

Example usage:
```python
try:
    response = open5gs.send_data(UE_API_URL, data)
    if not open5gs.launch_gtp_wireshark():
        raise CommunicationError("Failed to launch Wireshark")
except CommunicationError as e:
    print(f"Communication error: {e}")
    # Handle the error (e.g., retry the operation or log the failure)
```

You can also check the detailed status of background processes when encountering errors:

```python
try:
    open5gs.run_background_nodes()
    if not open5gs.is_run_background_nodes_complete():
        status = open5gs.get_background_process_status()
        if status['error_message']:
            raise CommunicationError(f"Background process error: {status['error_message']}")
except CommunicationError as e:
    print(f"Communication error: {e}")
    # Handle the error (e.g., check system requirements or restart services)
```