# ISO Template Quick Start Guide

## Overview
This guide provides a quick introduction to using ISO templates for automated OS deployment in AutoCloud.

## What are ISO Templates?
ISO templates are JSON configuration files that define:
- Operating system details (name, version, architecture)
- Download URLs and checksums
- Automated installation parameters
- Post-installation configurations
- System requirements

## Quick Start Steps

### 1. Choose Your Template
Navigate to the appropriate directory:
```
ISO-Template/
├── Linux/          # Ubuntu, CentOS, Debian, etc.
├── Windows/        # Windows Server, Windows 10/11
├── BSD/            # FreeBSD, OpenBSD
├── Virtualization/ # Proxmox, ESXi
├── Container/      # CoreOS, RancherOS
├── Security/       # Kali, Parrot
├── Embedded/       # Raspberry Pi OS
└── Specialized/    # pfSense, OPNsense
```

### 2. Review Template Structure
```json
{
  "name": "Ubuntu 22.04 LTS Server",
  "version": "22.04",
  "type": "linux",
  "iso_url": "https://...",
  "checksum": "sha256:...",
  "system_requirements": {
    "min_ram": "2048",
    "min_disk": "25",
    "min_cpu": "2"
  },
  "autoinstall": { ... }
}
```

### 3. Customize Configuration
Edit the template to match your requirements:
- **Hostname**: Change default hostname
- **Network**: Configure static IP or DHCP
- **Packages**: Add/remove software packages
- **Users**: Set usernames and passwords
- **Partitioning**: Modify disk layout

### 4. Deploy Using AutoCloud CLI
```bash
# Validate template
autocloud template validate ubuntu-22.04-server.json

# Deploy VM from template
autocloud vm create --template ubuntu-22.04-server.json \
  --name my-server \
  --cpu 4 \
  --ram 8192 \
  --disk 50

# Monitor deployment
autocloud vm status my-server
```

### 5. Access Your System
Once deployment completes:
```bash
# SSH into the system
ssh username@<ip-address>

# Or use console access
autocloud vm console my-server
```

## Common Use Cases

### Development Environment
```bash
autocloud vm create --template ubuntu-22.04-server.json \
  --name dev-server \
  --packages "docker.io,git,nodejs"
```

### Production Server
```bash
autocloud vm create --template centos-stream-9.json \
  --name prod-web \
  --cpu 8 \
  --ram 16384 \
  --disk 100 \
  --network static \
  --ip 192.168.1.100
```

### Testing Environment
```bash
autocloud vm create --template debian-12-bookworm.json \
  --name test-env \
  --snapshot-enabled \
  --auto-destroy 24h
```

## Template Variables
Use variables for dynamic configuration:
```json
{
  "hostname": "{{VM_NAME}}",
  "ip_address": "{{IP_ADDRESS}}",
  "gateway": "{{GATEWAY}}",
  "dns_servers": ["{{DNS1}}", "{{DNS2}}"]
}
```

Pass variables during deployment:
```bash
autocloud vm create --template ubuntu-22.04-server.json \
  --var VM_NAME=web-server-01 \
  --var IP_ADDRESS=192.168.1.50 \
  --var GATEWAY=192.168.1.1
```

## Best Practices
1. **Always validate** templates before deployment
2. **Use version control** for custom templates
3. **Test in dev** before production deployment
4. **Document changes** to templates
5. **Keep checksums updated** when using new ISOs
6. **Use secure passwords** (never commit passwords to git)
7. **Enable logging** for troubleshooting

## Troubleshooting

### Template Validation Fails
```bash
# Check JSON syntax
autocloud template validate --verbose template.json

# Verify ISO URL is accessible
curl -I <iso_url>
```

### Deployment Hangs
- Check system requirements are met
- Verify network connectivity
- Review boot command sequence
- Check hypervisor logs

### Post-Install Issues
- Verify SSH keys are correctly configured
- Check firewall rules
- Ensure services are enabled
- Review system logs

## Next Steps
- Read the [Advanced Configuration Guide](02-Advanced-Configuration-Guide.md)
- Explore [Custom Template Creation](03-Custom-Template-Creation-Guide.md)
- Learn about [Security Hardening](04-Security-Hardening-Guide.md)
- Check [Troubleshooting Guide](05-Troubleshooting-Guide.md)

## Support
- Documentation: https://docs.autocloud.io
- Community: https://community.autocloud.io
- Issues: https://github.com/autocloud/issues
