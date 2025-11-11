# Datadog Monitoring Configuration

A comprehensive Datadog monitoring setup for cloud infrastructure, servers, and multiple operating systems.

## Directory Structure
```
.
├── README.md
├── cloud/
│   ├── aws-config.yaml      # AWS-specific monitoring
│   └── gcp-config.yaml      # GCP-specific monitoring
├── server/
│   └── datadog-agent.yaml   # General server monitoring
└── os_configs/
    ├── ubuntu/
    │   └── datadog.yaml     # Ubuntu-specific configuration
    ├── centos/
    │   └── datadog.yaml     # CentOS-specific configuration
    ├── debian/
    │   └── datadog.yaml     # Debian-specific configuration
    ├── rhel/
    │   └── datadog.yaml     # RHEL-specific configuration
    ├── amazon_linux/
    │   └── datadog.yaml     # Amazon Linux configuration
    └── README.md            # OS-specific instructions
```

## Configuration Components

### 1. Cloud Monitoring
- **AWS Integration**:
  - EC2, RDS, ElastiCache monitoring
  - ELB and CloudFront metrics
  - Lambda function monitoring
  - CloudWatch metrics integration

- **GCP Integration**:
  - Compute Engine monitoring
  - Cloud SQL and Cloud Run
  - GKE cluster monitoring
  - Storage and Pub/Sub metrics

### 2. Server Monitoring
- System metrics collection
- Process monitoring
- Network performance tracking
- Log aggregation and analysis
- APM (Application Performance Monitoring)
- Custom integrations

### 3. OS-Specific Monitoring
- **Ubuntu**:
  - Systemd service monitoring
  - APT package tracking
  - System and auth logs

- **CentOS**:
  - SELinux integration
  - YUM/DNF tracking
  - System security monitoring

- **Debian**:
  - APT history logging
  - System performance metrics
  - Package management

- **RHEL**:
  - Subscription management
  - SELinux security context
  - Enterprise system monitoring

- **Amazon Linux**:
  - Cloud-init monitoring
  - AWS integration
  - EKS and CloudWatch metrics

## Quick Start

1. **Install Datadog Agent**:
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

2. **Choose Your Configuration**:
- For cloud monitoring: Use configs from `cloud/`
- For server monitoring: Use config from `server/`
- For OS-specific monitoring: Use appropriate config from `os_configs/`

3. **Apply Configuration**:
```bash
# Copy appropriate config
sudo cp <config_path> /etc/datadog-agent/datadog.yaml
sudo chown dd-agent:dd-agent /etc/datadog-agent/datadog.yaml
sudo chmod 640 /etc/datadog-agent/datadog.yaml

# Restart agent
sudo systemctl restart datadog-agent
```

## Security Considerations

1. **API Key Protection**:
   - Store API keys securely
   - Use environment variables
   - Implement proper access controls

2. **Log Security**:
   - Implement log rotation
   - Use credential masking
   - Set appropriate file permissions

3. **Network Security**:
   - Configure firewalls appropriately
   - Allow required Datadog endpoints
   - Use SSL/TLS for all communications

4. **Access Control**:
   - Implement RBAC
   - Use service accounts
   - Regular audit of access patterns

## Monitoring Features

1. **Metrics Collection**:
   - CPU, Memory, Disk usage
   - Network performance
   - Custom application metrics
   - Cloud service metrics

2. **Log Management**:
   - Centralized log collection
   - Log parsing and filtering
   - Pattern detection
   - Alert configuration

3. **APM & Tracing**:
   - Request tracing
   - Service mapping
   - Performance monitoring
   - Error tracking

4. **Alerting**:
   - Metric-based alerts
   - Log-based alerts
   - Multi-condition alerts
   - Custom notification channels

## Maintenance

1. **Regular Updates**:
```bash
sudo datadog-agent update
```

2. **Health Checks**:
```bash
sudo datadog-agent status
sudo datadog-agent configcheck
```

3. **Log Rotation**:
```bash
sudo datadog-agent log-rotate
```

## Troubleshooting

1. **Check Agent Status**:
```bash
sudo datadog-agent status
```

2. **View Agent Logs**:
```bash
sudo tail -f /var/log/datadog/agent.log
```

3. **Validate Configuration**:
```bash
sudo datadog-agent configcheck
```

## Support

- Datadog Documentation: [https://docs.datadoghq.com/](https://docs.datadoghq.com/)
- Community Forums: [https://discuss.datadog.com/](https://discuss.datadog.com/)
- Support Email: support@datadoghq.com
