# ISO Template Troubleshooting Guide

## Common Issues and Solutions

### Template Validation Errors
- Check JSON syntax
- Verify required fields
- Validate checksums
- Test ISO accessibility

### Boot Issues
- Increase wait times in boot commands
- Check firmware mode (UEFI vs BIOS)
- Verify boot parameters
- Enable console logging

### Installation Failures
- Verify preseed/kickstart configuration
- Check disk partitioning settings
- Ensure network connectivity
- Validate package names

### Network Problems
- Test DHCP configuration
- Verify static IP settings
- Check DNS resolution
- Review firewall rules

### Post-Installation Issues
- Verify SSH configuration
- Check service status
- Review system logs
- Validate user permissions

## Debugging Commands
```bash
# Validate template
autocloud template validate template.json

# Enable debug mode
autocloud vm create --template template.json --debug

# View console
autocloud vm console vm-name

# Check logs
autocloud vm logs vm-name

# Execute commands
autocloud vm exec vm-name "command"
```

## Getting Help
- Check documentation
- Review logs
- Search community forums
- Contact support
