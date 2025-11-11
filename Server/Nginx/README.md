# Nginx Advanced Configuration Structure

🌐 A comprehensive Nginx configuration with modular structure for better management and scalability.

## Directory Structure

```
nginx/
├── nginx.conf              # Main configuration file
├── conf.d/                 # Configuration modules
│   ├── apps.conf          # Web applications configuration
│   ├── proxy.conf         # Proxy settings
│   ├── security.conf      # Security settings
│   ├── ssl.conf           # SSL/TLS configuration
│   └── load-balancer.conf # Load balancer settings
├── sites-available/        # Available site configurations
│   └── default.conf       # Default site configuration
└── sites-enabled/         # Enabled site configurations (symlinks)
```

## Configuration Files Overview

### nginx.conf
- Main configuration file
- Worker processes and events
- Global settings
- Includes other configuration files

### conf.d/apps.conf
- Web application configurations
- Static file handling
- Caching rules
- Security headers

### conf.d/proxy.conf
- Proxy buffer settings
- Cache configuration
- Header settings
- WebSocket support
- Timeout configurations

### conf.d/security.conf
- Security headers
- Rate limiting
- DDoS protection
- File upload security
- Server tokens

### conf.d/ssl.conf
- SSL protocols
- Cipher suites
- HSTS settings
- OCSP stapling
- Session settings

### conf.d/load-balancer.conf
- Backend server groups
- Load balancing algorithms
- Health checks
- Session persistence
- Rate limiting

## Installation Instructions

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install nginx
sudo mkdir -p /etc/nginx/conf.d
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
```

### CentOS/RHEL
```bash
sudo yum install epel-release
sudo yum install nginx
sudo mkdir -p /etc/nginx/conf.d
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
```

### macOS
```bash
brew install nginx
mkdir -p /usr/local/etc/nginx/conf.d
mkdir -p /usr/local/etc/nginx/sites-available
mkdir -p /usr/local/etc/nginx/sites-enabled
```

### Windows
1. Download Nginx for Windows
2. Create directory structure:
```
C:\nginx\
├── conf\
    ├── conf.d\
    ├── sites-available\
    └── sites-enabled\
```

### Alpine Linux
```bash
apk add nginx
mkdir -p /etc/nginx/conf.d
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled
```

## Configuration Setup

1. Copy configuration files:
```bash
sudo cp nginx.conf /etc/nginx/
sudo cp conf.d/* /etc/nginx/conf.d/
sudo cp sites-available/* /etc/nginx/sites-available/
```

2. Create symbolic links:
```bash
sudo ln -s /etc/nginx/sites-available/default.conf /etc/nginx/sites-enabled/
```

3. Create SSL certificates:
```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/key.pem \
  -out /etc/nginx/ssl/cert.pem
```

4. Set permissions:
```bash
sudo chown -R nginx:nginx /etc/nginx
sudo chmod -R 755 /etc/nginx
```

5. Test configuration:
```bash
sudo nginx -t
```

6. Restart Nginx:
```bash
sudo systemctl restart nginx
```

## Port Forwarding Configuration

Default port mappings in load balancer:
- Web Backend (80) → 8001-8003
- API Backend → 9001-9003

Additional ports in apps.conf:
- HTTP (80) → 3000
- HTTPS (443) → 8080
- WebSocket (8080) → 9000

## Monitoring and Maintenance

### Log Locations
- Access Log: `/var/log/nginx/access.log`
- Error Log: `/var/log/nginx/error.log`
- Load Balancer Logs: 
  - `/var/log/nginx/loadbalancer.access.log`
  - `/var/log/nginx/loadbalancer.error.log`

### Monitoring Commands
```bash
# Check Nginx status
sudo systemctl status nginx

# Monitor logs in real-time
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check configuration
sudo nginx -t

# Check open ports
sudo netstat -tulpn | grep nginx
```

## Security Best Practices

1. Regular Updates
```bash
sudo apt update
sudo apt upgrade nginx
```

2. SSL/TLS Configuration
- Use strong cipher suites
- Enable HSTS
- Configure OCSP stapling

3. Rate Limiting
- Configure in security.conf
- Adjust limits based on traffic

4. DDoS Protection
- Use rate limiting
- Configure buffer sizes
- Enable connection limits

5. File Permissions
- Restrict access to configuration files
- Use proper user and group permissions

## Troubleshooting

1. Configuration Issues
```bash
sudo nginx -t
sudo nginx -T
```

2. Permission Issues
```bash
sudo chmod -R 755 /etc/nginx
sudo chown -R nginx:nginx /etc/nginx
```

3. Port Conflicts
```bash
sudo netstat -tulpn | grep LISTEN
sudo fuser -k 80/tcp  # Kill process using port 80
```

4. SSL Issues
```bash
openssl x509 -in /etc/nginx/ssl/cert.pem -text -noout
```

## Support

For issues and contributions, please create an issue or pull request in the repository.

## License

MIT License
