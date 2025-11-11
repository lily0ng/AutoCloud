# Log Management Automation Framework 📊

<div align="center">

```
  _                   __  __                                   
 | |    ___   __ _  |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
 | |   / _ \ / _` | | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |__| (_) | (_| | | |  | | (_| | | | | (_| | (_| |  __/ |   
 |_____\___/ \__, | |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
             |___/                             |___/            
```

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
</div>

A comprehensive framework for automating log management across operating systems and network devices with advanced features for monitoring, analysis, and security.

## Supported Operating Systems

<div align="center">
<table>
<tr>
    <td align="center"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"/><br/>Windows</td>
    <td align="center"><img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/><br/>Linux</td>
    <td align="center"><img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS"/><br/>macOS</td>
    <td align="center"><img src="https://img.shields.io/badge/FreeBSD-AB2B28?style=for-the-badge&logo=freebsd&logoColor=white" alt="FreeBSD"/><br/>FreeBSD</td>
    <td align="center"><img src="https://img.shields.io/badge/Solaris-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Solaris"/><br/>Solaris</td>
</tr>
</table>
</div>

### OS Support Details
| OS | Versions | Features |
|----|----------|-----------|
| Windows | Server 2012+, 10/11 | Event Logs, PowerShell Logs, Security Logs |
| Linux | Ubuntu, CentOS, RHEL, Debian | Syslog, Journald, Audit Logs |
| macOS | 10.15+ | System.log, ASL, Unified Logs |
| FreeBSD | 12+ | System Logs, Security Logs |
| Solaris | 11+ | System Logs, Audit Logs |

## Supported Network Devices

<div align="center">
<table>
<tr>
    <td align="center"><img src="https://img.shields.io/badge/Cisco-1BA0D7?style=for-the-badge&logo=cisco&logoColor=white" alt="Cisco"/><br/>Cisco IOS</td>
    <td align="center"><img src="https://img.shields.io/badge/Palo%20Alto-F04E23?style=for-the-badge&logo=paloaltonetworks&logoColor=white" alt="Palo Alto"/><br/>PAN-OS</td>
    <td align="center"><img src="https://img.shields.io/badge/Fortinet-EE3124?style=for-the-badge&logo=fortinet&logoColor=white" alt="Fortinet"/><br/>FortiOS</td>
    <td align="center"><img src="https://img.shields.io/badge/F5-E4002B?style=for-the-badge&logo=f5&logoColor=white" alt="F5"/><br/>BIG-IP</td>
    <td align="center"><img src="https://img.shields.io/badge/Check%20Point-FFB71B?style=for-the-badge&logo=checkpoint&logoColor=black" alt="Check Point"/><br/>Gaia</td>
</tr>
<tr>
    <td align="center"><img src="https://img.shields.io/badge/Arista-0099D9?style=for-the-badge&logo=arista&logoColor=white" alt="Arista"/><br/>EOS</td>
    <td align="center"><img src="https://img.shields.io/badge/Juniper-84B135?style=for-the-badge&logo=juniper&logoColor=white" alt="Juniper"/><br/>JUNOS</td>
    <td align="center"><img src="https://img.shields.io/badge/Huawei-FF0000?style=for-the-badge&logo=huawei&logoColor=white" alt="Huawei"/><br/>VRP</td>
    <td align="center"><img src="https://img.shields.io/badge/MikroTik-293239?style=for-the-badge&logo=mikrotik&logoColor=white" alt="MikroTik"/><br/>RouterOS</td>
    <td align="center"><img src="https://img.shields.io/badge/VMware-607078?style=for-the-badge&logo=vmware&logoColor=white" alt="VMware"/><br/>ESXi</td>
</tr>
</table>
</div>

### Network Device Support Details
| Device | OS Version | Supported Features |
|--------|------------|-------------------|
| Cisco | IOS 15+, IOS-XE 16+ | Syslog, SNMP, NetFlow |
| Palo Alto | PAN-OS 9+ | System Logs, Traffic Logs, Threat Logs |
| Fortinet | FortiOS 6+ | Traffic Logs, Event Logs, Security Logs |
| F5 | BIG-IP 14+ | System Logs, Traffic Logs, Audit Logs |
| Check Point | R80+ | Security Logs, Audit Logs, Traffic Logs |
| Arista | EOS 4.21+ | Syslog, SNMP, Event Logs |
| Juniper | JUNOS 19+ | System Logs, Security Logs, Traffic Logs |
| Huawei | VRP 8+ | System Logs, Security Logs |
| MikroTik | RouterOS 7+ | System Logs, Firewall Logs |
| VMware | ESXi 6.7+ | System Logs, Virtual Machine Logs |

## 🚀 Features

### Core Features
- Centralized Log Collection (Syslog, SNMP)
- Automated Log Parsing and Processing
- Log Rotation and Compression
- S3 Backup Integration
- Real-time Monitoring and Alerts
- Compliance Checks
- Error Categorization
- Elasticsearch Integration
- Slack Notifications
- Configurable Retention Policies

### Advanced Features
- 📊 Prometheus Metrics Integration
- 🔒 Log Encryption and Security Scanning
- 🔍 Pattern Analysis and Correlation
- 📡 REST API Endpoints
- 🗜️ Automatic Log Compression
- 📈 Real-time Performance Metrics
- 📋 Automated Log Summaries
- 🔗 Session-based Log Correlation
- 🛡️ Sensitive Data Detection
- 🚦 Multi-threaded Log Processing

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- 2GB RAM minimum (4GB recommended)
- 20GB disk space
- Network connectivity to managed devices

### Required Services
- Elasticsearch instance
- AWS Account (for S3 backup)
- Slack Workspace (for alerts)
- Prometheus (for metrics)

### OS-Specific Requirements

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpq-dev \
    libsystemd-dev

# CentOS/RHEL
sudo yum install -y \
    gcc \
    python3-devel \
    openssl-devel \
    libffi-devel \
    libxml2-devel \
    libxslt-devel \
    zlib-devel \
    libjpeg-devel \
    postgresql-devel \
    systemd-devel
```

#### macOS
```bash
brew install openssl libffi xz
```

#### Windows
- Install Visual C++ Build Tools
- Install OpenSSL
- Install Git for Windows

## 🛠️ Installation

### Quick Install (Linux/macOS)
```bash
# Clone the repository
git clone https://github.com/your-username/log-management.git
cd log-management

# Make install script executable
chmod +x install.sh

# Run installation script
./install.sh
```

### Manual Installation

1. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

2. Install dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install core requirements
pip install -r requirements.txt
```

3. Configure environment
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your credentials
nano .env
```

### Package Groups

The framework uses various package groups for different functionalities:

#### Core Dependencies
- python-logstash: Log shipping
- elasticsearch: Log storage and search
- prometheus_client: Metrics collection
- Flask: API endpoints

#### OS-Specific Packages
- Windows: pywinrm, wmi, pywin32
- Linux: systemd-python, linux-metrics
- macOS: pyobjc frameworks
- FreeBSD: py-freebsd
- Solaris: py-solaris

#### Network Device Packages
- Cisco: netmiko, ciscoconfparse
- Palo Alto: pan-python, pan-os-python
- Fortinet: fortiosapi
- F5: f5-sdk, bigsuds
- Check Point: checkpoint-mgmt-api
- Others: Various vendor-specific SDKs

#### Security & Encryption
- cryptography
- pyOpenSSL
- paramiko
- bcrypt

#### Monitoring & Metrics
- statsd
- datadog
- newrelic
- pysnmp

#### Database Connectors
- pymongo
- redis
- sqlalchemy
- psycopg2-binary
- mysql-connector-python

## 🚀 Post-Installation

1. Verify installation
```bash
python3 -c "from log_manager import LogManager; print('Installation successful!')"
```

2. Configure credentials in .env file
```bash
nano .env
```

3. Test connectivity
```bash
python3 -m pytest tests/
```

4. Start the service
```bash
python3 log_manager.py
```

## 🔧 Troubleshooting

### Common Issues

1. SSL Certificate Errors
```bash
# Install certificates
pip install certifi
```

2. Network Device Connection Issues
```bash
# Test network connectivity
python3 tools/test_connectivity.py
```

3. Permission Issues
```bash
# Check log directory permissions
sudo chown -R $USER:$USER logs/
chmod 755 logs/
```

### Getting Help

- Check the logs in `logs/system.log`
- Run diagnostics: `python3 tools/diagnose.py`
- Submit an issue on GitHub
- Contact support team

## 📝 Sample Configurations

### Windows Log Collection
```yaml
os_sources:
  - type: windows
    host: win-server.local
    interval: 5
    credentials:
      username: admin
      password: ${WIN_PASSWORD}
    logs:
      - System
      - Application
      - Security
```

### Cisco Network Device
```yaml
network_sources:
  - type: cisco_ios
    host: core-switch.local
    interval: 5
    credentials:
      username: admin
      password: ${CISCO_PASSWORD}
      enable_secret: ${CISCO_ENABLE}
    collection:
      commands:
        - show logging
        - show log
```

### Linux Server
```yaml
os_sources:
  - type: linux
    host: linux-server.local
    interval: 5
    credentials:
      username: root
      password: ${LINUX_PASSWORD}
    logs:
      - /var/log/syslog
      - /var/log/auth.log
```

## 🚀 Usage Examples

### Collecting Windows Event Logs
```python
from log_manager import LogManager

manager = LogManager()
logs = manager.collect_os_logs('windows', 'win-server.local', {
    'username': 'admin',
    'password': 'your-password'
})
```

### Monitoring Cisco Network Device
```python
logs = manager.collect_network_device_logs('cisco_ios', 'switch.local', {
    'username': 'admin',
    'password': 'your-password',
    'enable_secret': 'enable-password'
})
```

### Analyzing Security Events
```python
security_findings = manager.perform_security_scan(logs)
if security_findings['risk_level'] == 'high':
    manager.send_alert('High-risk security event detected')
```

## 🔒 Security Considerations

- All sensitive credentials should be stored in the `.env` file
- Enable encryption for sensitive log data
- Regularly rotate access keys and tokens
- Monitor security scan results
- Use secure communication channels

## 🛠️ Maintenance

- Monitor Prometheus metrics
- Review security findings
- Check disk usage
- Verify backup success
- Update compliance settings
- Monitor API endpoints

## 📊 Metrics

Access Prometheus metrics at `http://localhost:8000/metrics`:
- `logs_processed_total`: Total number of processed logs
- `error_count`: Current error count
- `processing_latency`: Log processing latency

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

MIT License

## 🌟 Acknowledgments

- Microsoft Windows Team
- Linux Foundation
- Apple Developer Community
- FreeBSD Foundation
- Oracle Solaris Team
- Cisco Systems
- Palo Alto Networks
- VMware, Inc.
- All other network device manufacturers
