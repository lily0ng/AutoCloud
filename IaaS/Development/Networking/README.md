# Network Automation Configuration

This project provides automated configuration for multiple network switches, including:
- Auto service configuration
- Port forwarding setup
- Automatic IP configuration
- Port channel configuration
- Interface monitoring

## Features
- Configures 5 switches automatically
- Sets up VLANs (10-30)
- Configures port channels for link aggregation
- Monitors port status
- Implements service autoconfig
- Sets up IP forwarding

## Requirements
- Python 3.8+
- Network access to switches
- Cisco IOS compatible switches

## Installation
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Configure your switch details in `device_config.json`:
- Update IP addresses
- Set proper credentials
- Verify device types

## Usage
Run the automation script:
```bash
python network_config.py
```

## Security Note
- Replace default passwords in device_config.json with secure credentials
- Use environment variables for sensitive information
- Enable SSH for secure communication
