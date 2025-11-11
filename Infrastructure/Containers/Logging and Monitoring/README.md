# Infrastructure Logging and Monitoring Setup

A comprehensive logging and monitoring infrastructure setup with support for multiple operating systems, featuring automated setup scripts, maintenance tools, and extensive configuration files.

## Features

- Multi-OS Support (Ubuntu, CentOS)
- Automated Setup Scripts
- Centralized Logging
- System and Service Monitoring
- Alert Management
- Automated Maintenance
- Visualization Dashboards

## Directory Structure
```
.
├── scripts/
│   ├── setup/
│   │   ├── ubuntu_setup.sh
│   │   └── centos_setup.sh
│   └── maintenance/
│       └── maintenance.sh
├── config/
│   ├── ubuntu/
│   │   ├── prometheus.yml
│   │   └── filebeat.yml
│   ├── centos/
│   │   ├── prometheus.yml
│   │   └── filebeat.yml
│   └── common/
│       ├── prometheus.yml
│       └── filebeat.yml
└── monitoring/
    ├── prometheus/
    ├── grafana/
    │   └── system_dashboard.json
    └── alertmanager/
        └── alertmanager.yml
```

## Components

### Monitoring Stack
- **Prometheus**: Metrics collection and storage
  - OS-specific configurations
  - Custom service discovery
  - Built-in alerting rules
- **Grafana**: Visualization and dashboards
  - Pre-configured system dashboard
  - CPU, Memory, Disk, and Network metrics
  - Custom alert thresholds
- **AlertManager**: Alert handling and notifications
  - Email notifications
  - Alert grouping and routing
  - Inhibition rules

### Logging Stack
- **Filebeat**: Log collection
  - OS-specific log paths
  - Structured logging
  - Custom field enrichment
- **Elasticsearch**: Log storage and analysis
- **Kibana**: Log visualization

## OS-Specific Features

### Ubuntu
- System Logs: syslog, auth.log, kern.log, dpkg.log
- Service Logs: Apache2, Nginx
- Journald Integration
- Process Monitoring
- Container Metrics

### CentOS
- System Logs: messages, secure, yum.log, audit.log
- Service Logs: HTTPD, Nginx
- SELinux Monitoring
- Process Monitoring
- Container Metrics

## Setup Instructions

1. Choose your OS-specific setup script:
```bash
# For Ubuntu
chmod +x scripts/setup/ubuntu_setup.sh
sudo ./scripts/setup/ubuntu_setup.sh

# For CentOS
chmod +x scripts/setup/centos_setup.sh
sudo ./scripts/setup/centos_setup.sh
```

2. Configure Maintenance:
```bash
chmod +x scripts/maintenance/maintenance.sh
# Add to crontab for automated maintenance
0 0 * * * /path/to/maintenance.sh
```

3. Access Services:
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Kibana: http://localhost:5601
- AlertManager: http://localhost:9093

## Maintenance Tasks

The maintenance script performs:
- Service health checks
- Log rotation
- Disk space monitoring
- Prometheus data retention
- System cleanup

## Customization

### Adding New Monitoring Targets
1. Add target to OS-specific `prometheus.yml`
2. Add relevant log paths to `filebeat.yml`
3. Create Grafana dashboard panels

### Alert Configuration
1. Modify `alertmanager.yml` for notification settings
2. Add new alert rules in Prometheus
3. Configure alert thresholds in Grafana

## Requirements

- Ubuntu 20.04+ or CentOS 8+
- Minimum 4GB RAM
- 20GB disk space
- Root/sudo access

## Security Considerations

- All services run with minimal required permissions
- Secure communication with TLS
- Regular security updates via maintenance script
- SELinux/AppArmor profiles included
- Secure default configurations

## Support

For issues and feature requests:
1. Check the maintenance script logs
2. Verify service status and configurations
3. Review system requirements
4. Check OS compatibility
