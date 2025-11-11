# System Monitoring Script 🖥️

<div align="center">

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/)

</div>

A comprehensive cross-platform system monitoring solution that collects and exports system performance metrics. The script supports integration with Prometheus and can be extended to work with other monitoring tools.

## 🌟 Features

- Real-time monitoring of system metrics:
  - CPU usage
  - Memory usage
  - Disk usage
  - System logs (syslog, journald, event logs)
  - Process information
  - Network statistics
- Prometheus metrics export
- Configurable monitoring intervals
- Advanced logging capabilities with log rotation
- YAML-based configuration
- Support for multiple operating systems

## 🔧 Prerequisites

- Python 3.7+
- Required Python packages (install using requirements.txt)
- System permissions for log access

### Operating System Requirements

<details>
<summary>🐧 Linux</summary>

- sudo privileges for system log access
- syslog or journald access
- Required packages:
  ```bash
  sudo apt-get install python3-dev
  sudo apt-get install systemd-dev  # For journald support
  ```
</details>

<details>
<summary>🪟 Windows</summary>

- Administrator privileges for Event Log access
- PowerShell access
- Required packages:
  ```powershell
  pip install pywin32
  ```
</details>

<details>
<summary>🍎 macOS</summary>

- sudo privileges for system log access
- Command Line Tools installed
- Required packages:
  ```bash
  xcode-select --install
  ```
</details>

## 📥 Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

### System-Specific Setup

<details>
<summary>🐧 Linux Setup</summary>

```bash
# Add user to syslog group
sudo usermod -a -G syslog $USER
# For journald access
sudo usermod -a -G systemd-journal $USER
```
</details>

<details>
<summary>🪟 Windows Setup</summary>

- Run PowerShell as Administrator
- Enable Event Log collection:
  ```powershell
  Set-ExecutionPolicy RemoteSigned
  # Verify Event Log service is running
  Get-Service EventLog
  ```
</details>

<details>
<summary>🍎 macOS Setup</summary>

```bash
# Grant log access
sudo chmod +r /var/log/system.log
```
</details>

## ⚙️ Configuration

Edit `config.yaml` to customize the monitoring settings:

<details>
<summary>📝 Configuration Options</summary>

```yaml
# Basic Settings
interval: 60
disk_paths:
  - "/"
  - "/home"

# Log Configuration
logs:
  enabled: true
  sources:
    - type: syslog
      path: /var/log/syslog
      enabled: true
  filters:
    severity: [ERROR, WARNING, CRITICAL]
```
</details>

## 🚀 Usage

1. Start the monitoring script:
   ```bash
   python system_monitor.py
   ```

2. Access metrics:
   - Prometheus: `http://localhost:8000`
   - Log files: `system_monitor.log`

## 📊 Metrics & Logging

### Available Metrics

| Metric | Description | Platform |
|--------|-------------|----------|
| CPU Usage | System CPU utilization | All |
| Memory Usage | RAM utilization | All |
| Disk Usage | Storage utilization | All |
| Network Stats | Network I/O | All |
| System Logs | OS-specific logs | All |

### Log Sources by OS

| OS | Log Sources | Access Method |
|----|------------|---------------|
| 🐧 Linux | syslog, journald | File, API |
| 🪟 Windows | Event Log | Windows API |
| 🍎 macOS | system.log | File |

## 🔍 Monitoring Integration

### 📈 Grafana Dashboard

![Grafana Dashboard](https://img.shields.io/badge/Grafana-Dashboard-F46800?style=for-the-badge&logo=grafana&logoColor=white)

Sample dashboard available at `grafana/dashboards/system_monitor.json`

### 🔥 Prometheus Integration

```yaml
scrape_configs:
  - job_name: 'system_monitor'
    static_configs:
      - targets: ['localhost:8000']
```

## 🛠️ Troubleshooting

<details>
<summary>Common Issues</summary>

### 🐧 Linux Issues
```bash
# Permission denied
sudo chmod +r /var/log/syslog
groups $USER  # Verify group membership
```

### 🪟 Windows Issues
- Run as Administrator
- Check Event Viewer access
- Verify service status:
  ```powershell
  Get-Service EventLog
  ```

### 🍎 macOS Issues
```bash
# Log access issues
sudo chmod +r /var/log/system.log
```
</details>

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
<div align="center">
Made with ❤️ by [MrGh0st](https://github.com/MrGh0st) - Cyber Insights Forum - CIF Community

![Visitors](https://img.shields.io/badge/dynamic/json?color=blue&label=Visitors&query=value&url=https://api.countapi.xyz/hit/system-monitor/readme)
</div>
