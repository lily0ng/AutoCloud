# Apache Port Forwarding & Proxy Configuration Guide 🌐

![Apache Logo](https://httpd.apache.org/images/httpd_logo_wide_new.png)

## Overview
This configuration guide provides setup instructions for Apache port forwarding and proxy management across different operating systems (Linux, Windows, macOS, FreeBSD, and Debian).

## Features
- Multi-port forwarding configuration
- Proxy management for different services
- Cross-platform compatibility
- Security best practices
- Load balancing support

## Directory Structure
```
apache-proxy-config/
├── configs/
│   ├── linux/
│   ├── windows/
│   ├── macos/
│   ├── freebsd/
│   └── debian/
└── scripts/
```

## Prerequisites
- Apache 2.4 or higher
- mod_proxy enabled
- mod_proxy_http enabled
- mod_ssl (for HTTPS)

## Configuration Steps

### 1. Enable Required Modules
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod lbmethod_byrequests
```

### 2. Basic Port Forwarding Setup
- Configure virtual hosts
- Set up proxy rules
- Enable SSL if needed
- Configure load balancing

### 3. OS-Specific Instructions

#### Linux
- Configuration location: `/etc/apache2/`
- Restart command: `systemctl restart apache2`

#### Windows
- Configuration location: `C:\Apache24\conf`
- Restart command: `httpd -k restart`

#### macOS
- Configuration location: `/etc/apache2/`
- Restart command: `apachectl restart`

#### FreeBSD
- Configuration location: `/usr/local/etc/apache24/`
- Restart command: `service apache24 restart`

#### Debian
- Configuration location: `/etc/apache2/`
- Restart command: `systemctl restart apache2`

## Configuration File Locations 📁

### Linux (Ubuntu/Debian)
- Main Configuration: `/etc/apache2/apache2.conf`
- Port Configuration: `/etc/apache2/ports.conf`
- Site Configurations: `/etc/apache2/sites-available/`
- Enabled Sites: `/etc/apache2/sites-enabled/`
- Proxy Configuration: `/etc/apache2/mods-available/proxy.conf`

Edit commands:
```bash
sudo nano /etc/apache2/apache2.conf
sudo nano /etc/apache2/ports.conf
sudo nano /etc/apache2/sites-available/000-default.conf
```

### Windows
- Main Configuration: `C:\Apache24\conf\httpd.conf`
- Port Configuration: `C:\Apache24\conf\extra\httpd-vhosts.conf`
- Proxy Configuration: `C:\Apache24\conf\extra\httpd-proxy.conf`

Edit commands:
```cmd
notepad C:\Apache24\conf\httpd.conf
notepad C:\Apache24\conf\extra\httpd-proxy.conf
```

### macOS
- Main Configuration: `/etc/apache2/httpd.conf`
- User Configuration: `/etc/apache2/users/`
- Virtual Hosts: `/etc/apache2/extra/httpd-vhosts.conf`
- Proxy Configuration: `/etc/apache2/extra/httpd-proxy.conf`

Edit commands:
```bash
sudo nano /etc/apache2/httpd.conf
sudo nano /etc/apache2/extra/httpd-proxy.conf
```

### FreeBSD
- Main Configuration: `/usr/local/etc/apache24/httpd.conf`
- Include Files: `/usr/local/etc/apache24/Includes/`
- Proxy Configuration: `/usr/local/etc/apache24/extra/httpd-proxy.conf`

Edit commands:
```bash
ee /usr/local/etc/apache24/httpd.conf
ee /usr/local/etc/apache24/extra/httpd-proxy.conf
```

### Debian
- Main Configuration: `/etc/apache2/apache2.conf`
- Port Configuration: `/etc/apache2/ports.conf`
- Site Configurations: `/etc/apache2/sites-available/`
- Proxy Configuration: `/etc/apache2/mods-available/proxy.conf`

Edit commands:
```bash
sudo nano /etc/apache2/apache2.conf
sudo nano /etc/apache2/ports.conf
sudo nano /etc/apache2/mods-available/proxy.conf
```

## Configuration Tips 💡

1. Always backup configuration files before editing:
```bash
sudo cp /etc/apache2/apache2.conf /etc/apache2/apache2.conf.backup
```

2. Test configuration after changes:
```bash
# Linux/Debian/macOS
sudo apache2ctl configtest

# Windows
httpd -t

# FreeBSD
service apache24 configtest
```

3. Restart Apache after changes:
```bash
# Linux/Debian
sudo systemctl restart apache2

# macOS
sudo apachectl restart

# Windows
httpd -k restart

# FreeBSD
service apache24 restart
```

## Security Considerations
1. Always use SSL/TLS for sensitive traffic
2. Implement proper access controls
3. Regular security updates
4. Monitor logs for suspicious activity

## Troubleshooting
- Check Apache error logs
- Verify port availability
- Confirm module activation
- Test proxy connectivity

## Support
For issues and support, please create an issue in the repository.

## License
Apache License 2.0
