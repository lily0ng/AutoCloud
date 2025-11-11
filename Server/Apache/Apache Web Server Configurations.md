# Apache Web Server Configuration Guide for Ubuntu

## Table of Contents

1. [Installation](#installation)
2. [Basic Configuration](#basic-configuration)
3. [Virtual Hosts](#virtual-hosts)
4. [SSL Configuration](#ssl-configuration)
5. [Security Hardening](#security-hardening)
6. [Performance Tuning](#performance-tuning)
7. [Troubleshooting](#troubleshooting)

## Installation

```bash
# Update package list
sudo apt update

# Install Apache
sudo apt install apache2

# Check status
sudo systemctl status apache2
```

## Basic Configuration

### Important Directories

- `/etc/apache2/` - Main configuration directory
- `/etc/apache2/apache2.conf` - Main configuration file
- `/etc/apache2/sites-available/` - Available virtual host configurations
- `/etc/apache2/sites-enabled/` - Enabled virtual host configurations
- `/var/log/apache2/` - Log files
- `/var/www/html/` - Default web root directory

### Essential Apache Commands

```bash
# Start Apache
sudo systemctl start apache2

# Stop Apache
sudo systemctl stop apache2

# Restart Apache
sudo systemctl restart apache2

# Reload Configuration
sudo systemctl reload apache2

# Enable Apache on system startup
sudo systemctl enable apache2
```

## Virtual Hosts

### Creating a New Virtual Host

1. Create directory for your site:

```bash
sudo mkdir /var/www/your-domain
sudo chown -R $USER:$USER /var/www/your-domain
```

2. Create a new virtual host file:

```bash
sudo nano /etc/apache2/sites-available/your-domain.conf
```

3. Basic Virtual Host Configuration:

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@your-domain
    ServerName your-domain
    ServerAlias www.your-domain
    DocumentRoot /var/www/your-domain
    ErrorLog ${APACHE_LOG_DIR}/your-domain_error.log
    CustomLog ${APACHE_LOG_DIR}/your-domain_access.log combined

    <Directory /var/www/your-domain>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

4. Enable the site:

```bash
sudo a2ensite your-domain.conf
sudo systemctl reload apache2
```

## SSL Configuration

### Installing SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-apache

# Obtain and install certificate
sudo certbot --apache -d your-domain
```

### Manual SSL Configuration

```apache
<VirtualHost *:443>
    ServerName your-domain
    DocumentRoot /var/www/your-domain
    
    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key
    SSLCertificateChainFile /path/to/chain.crt
</VirtualHost>
```

## Security Hardening

### Basic Security Configuration

```apache
# Disable server signature
ServerSignature Off
ServerTokens Prod

# Prevent directory browsing
<Directory /var/www/html>
    Options -Indexes
</Directory>

# Disable CGI execution
<Directory /var/www/html>
    Options -ExecCGI
    AddHandler cgi-script .cgi .pl .py
</Directory>
```

### ModSecurity Installation

```bash
# Install ModSecurity
sudo apt install libapache2-mod-security2

# Enable ModSecurity
sudo a2enmod security2
sudo systemctl restart apache2
```

## Performance Tuning

### MPM Configuration

```apache
<IfModule mpm_prefork_module>
    StartServers             5
    MinSpareServers         5
    MaxSpareServers         10
    MaxRequestWorkers       150
    MaxConnectionsPerChild  0
</IfModule>
```

### Enable Caching

```apache
# Enable cache modules
sudo a2enmod expires
sudo a2enmod headers

# Cache configuration
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

## Troubleshooting

### Common Issues and Solutions

1. **Apache Won't Start**

```bash
# Check error logs
sudo tail -f /var/log/apache2/error.log

# Check configuration syntax
sudo apache2ctl configtest
```

2. **Permission Issues**

```bash
# Fix permissions for web root
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html
```

3. **SSL Certificate Issues**

```bash
# Check SSL configuration
sudo apache2ctl -t -D DUMP_MODULES | grep ssl
sudo openssl verify /path/to/certificate.crt
```

### Useful Debug Commands

```bash
# Test configuration
sudo apache2ctl -t

# Show loaded modules
sudo apache2ctl -M

# Show virtual hosts
sudo apache2ctl -S