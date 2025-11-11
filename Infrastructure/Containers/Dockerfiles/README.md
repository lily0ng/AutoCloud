# Infrastructure Automation Container

A comprehensive Docker container for infrastructure automation, configuration management, and deployment tasks. Built on Ubuntu 22.04 with essential tools and best practices for DevOps workflows.

## Features

- **Base System**: Ubuntu 22.04 LTS
- **Core Tools**:
  - Python 3 with pip
  - Ansible for configuration management
  - Git for version control
  - Vim for text editing
  - curl, wget for network operations
  - jq for JSON processing
  
- **Python Packages**:
  - `ansible==8.5.0`: Infrastructure as Code
  - `boto3==1.28.0`: AWS SDK
  - `requests==2.31.0`: HTTP client
  - `pyyaml==6.0.1`: YAML processing
  - `python-dotenv==1.0.0`: Environment management
  - `paramiko==3.3.1`: SSH protocol implementation

## Quick Start

### Building the Container

```bash
# Build with default settings
docker build -t infra-automation .

# Build with custom arguments
docker build -t infra-automation:custom --build-arg PYTHON_VERSION=3.10 .
```

### Running the Container

```bash
# Run interactive shell
docker run -it --name infra-automation -v $(pwd)/data:/app/data infra-automation

# Run specific script
docker run -it --name infra-automation -v $(pwd)/data:/app/data infra-automation /app/scripts/setup.sh

# Execute command in running container
docker exec -it infra-automation /app/scripts/setup.sh
```

## Directory Structure

```
/app/
├── scripts/           # Automation scripts
│   └── setup.sh      # Initial setup script
├── data/             # Persistent data volume
│   ├── config/       # Configuration files
│   └── logs/         # Log files
└── requirements.txt  # Python dependencies
```

## Configuration

### Environment Variables

- `DEBIAN_FRONTEND=noninteractive`: Prevents interactive prompts during package installation
- `PATH="/app/scripts:${PATH}"`: Makes scripts directly executable

### Volume Mounts

The container uses a volume mount for persistent data:
- Host: `$(pwd)/data`
- Container: `/app/data`

### Default Configuration

The `setup.sh` script creates a default configuration in `/app/data/config/config.yaml`:

```yaml
environment: development
logging:
  level: INFO
  path: /app/data/logs
settings:
  auto_update: true
  backup_enabled: true
```

## Security Considerations

- Container runs with minimal required permissions
- Sensitive data should be managed through environment variables or secure vaults
- Regular security updates are recommended
- Avoid running container as root in production

## Development

### Adding New Scripts

1. Place your script in the `scripts/` directory
2. Make it executable: `chmod +x scripts/your_script.sh`
3. Rebuild the container

### Customizing Python Dependencies

1. Update `requirements.txt`
2. Rebuild the container

## Troubleshooting

Common issues and solutions:

1. **Permission Issues**:
   ```bash
   chmod -R 755 scripts/
   chown -R 1000:1000 data/
   ```

2. **Volume Mount Problems**:
   ```bash
   # Verify volume mount
   docker inspect infra-automation
   ```

3. **Package Installation Failures**:
   ```bash
   # Rebuild with no cache
   docker build --no-cache -t infra-automation .
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details
