# OS-Specific Datadog Configurations

This directory contains Datadog monitoring configurations optimized for different operating systems.

## Supported Operating Systems

1. Ubuntu
2. CentOS
3. Debian
4. RHEL (Red Hat Enterprise Linux)
5. Amazon Linux

## Installation Instructions

### Ubuntu
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
cp ubuntu/datadog.yaml /etc/datadog-agent/datadog.yaml
systemctl restart datadog-agent
```

### CentOS
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
cp centos/datadog.yaml /etc/datadog-agent/datadog.yaml
systemctl restart datadog-agent
```

### Debian
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
cp debian/datadog.yaml /etc/datadog-agent/datadog.yaml
systemctl restart datadog-agent
```

### RHEL
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
cp rhel/datadog.yaml /etc/datadog-agent/datadog.yaml
systemctl restart datadog-agent
```

### Amazon Linux
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
cp amazon_linux/datadog.yaml /etc/datadog-agent/datadog.yaml
systemctl restart datadog-agent
```

## Configuration Features

Each OS-specific configuration includes:
- System log monitoring
- Process monitoring
- Security monitoring
- Package management monitoring
- OS-specific service monitoring
- Custom integrations
- APM (Application Performance Monitoring)
- Network monitoring
- Container monitoring (if applicable)

## Important Notes

1. Replace `<YOUR_API_KEY>` with your actual Datadog API key
2. Ensure proper permissions on configuration files:
```bash
chmod 640 /etc/datadog-agent/datadog.yaml
chown dd-agent:dd-agent /etc/datadog-agent/datadog.yaml
```

3. SELinux Considerations (CentOS/RHEL):
```bash
semodule -i datadog-agent.pp
```

4. Firewall Configuration:
- Allow outbound traffic to *.datadoghq.com
- Default ports: 443 (HTTPS)
