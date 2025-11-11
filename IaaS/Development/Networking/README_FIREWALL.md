# Firewall Automation Configuration

This project provides automated configuration for 10 firewall devices with comprehensive security policies and monitoring.

## Features
- Zone-based firewall configuration
- Access Control Lists (ACLs)
- Security policies
- IPS configuration
- Interface security settings
- Logging and monitoring

## Security Features
1. Zone Security
   - INSIDE zone
   - OUTSIDE zone
   - DMZ zone
   - Zone-pair security policies

2. Access Control Lists
   - INSIDE-OUT rules
   - OUTSIDE-IN rules
   - DMZ-specific rules
   - Logging for denied traffic

3. Security Policies
   - Inspection policies
   - Drop policies with logging
   - IPS policies

4. Interface Security
   - Zone membership
   - DHCP configuration
   - Security timestamps

## Installation
1. Install required packages:
```bash
pip install netmiko
```

2. Configure your firewall details in `firewall_devices.json`:
   - Update IP addresses
   - Set proper credentials
   - Verify device types

## Usage
Run the automation script:
```bash
python firewall_automation.py
```

## Logging
- All configurations are logged to `firewall_config.log`
- Includes timestamps and success/failure status
- Detailed error messages for troubleshooting

## Security Note
- Replace default passwords in firewall_devices.json
- Use environment variables for credentials
- Keep logs secure
- Regularly update IPS signatures
