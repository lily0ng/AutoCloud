# Comprehensive Nginx Configuration Guide for Ubuntu

## Installation and Initial Setup

1. Update the package list and upgrade existing packages:

```bash
sudo apt update
sudo apt upgrade -y
```

2. Install Nginx:

```bash
sudo apt install nginx -y
```

3. Verify installation and check Nginx status:

```bash
sudo systemctl status nginx
```

4. Enable Nginx to start on boot:

```bash
sudo systemctl enable nginx
```

5. Check Nginx version:

```bash
nginx -v
```

## Understanding Directory Structure

### Key Directories and Their Purpose

- `/etc/nginx/` - Main Nginx configuration directory
  - `nginx.conf` - Primary configuration file
  - `sites-available/` - Storage for all server block configurations
  - `sites-enabled/` - Symbolic links to enabled sites from sites-available
  - `conf.d/` - Additional configuration files
- `/var/www/html/` - Default web root directory
- `/var/log/nginx/` - Log files location
  - `access.log` - Records all requests
  - `error.log` - Records all errors

## Detailed Server Block Configuration

### Creating a New Website

1. Create the website directory:

```bash
sudo mkdir -p /var/www/your_domain/html
```

2. Set correct ownership:

```bash
sudo chown -R $USER:$USER /var/www/your_domain/html
```

3. Set proper permissions:

```bash
sudo chmod -R 755 /var/www/your_domain
```

4. Create a sample index.html:

```bash
sudo nano /var/www/your_domain/html/index.html
```

Add basic HTML content:

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Welcome to Your Website</title>
    </head>
    <body>
        <h1>Success! Your Nginx server is running.</h1>
    </body>
</html>
```

5. Create detailed server block configuration:

```nginx
server {
    listen 80;
    listen [::]:80;  # IPv6 support
    
    root /var/www/your_domain/html;
    index index.html index.htm index.nginx-debian.html;
    
    server_name your_domain.com www.your_domain.com;
    
    # Logging configuration
    access_log /var/log/nginx/your_domain.access.log;
    error_log /var/log/nginx/your_domain.error.log;
    
    # Main location block
    location / {
        try_files $uri $uri/ =404;
        # Basic cache control
        expires 1h;
        add_header Cache-Control "public, no-transform";
    }
    
    # Handle 404 errors
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
    
    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

## Advanced Configuration Examples

### SSL Configuration with Let's Encrypt

1. Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
```

2. Obtain SSL certificate:

```bash
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

3. Detailed SSL configuration:

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your_domain.com www.your_domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # SSL session configuration
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/your_domain.com/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
}
```

### Advanced Reverse Proxy Configuration

```nginx
location /api/ {
    # Proxy settings
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    
    # Header configurations
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # WebSocket support
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Buffering settings
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 4 32k;
    proxy_busy_buffers_size 64k;
}
```

### Optimized Gzip Configuration

```nginx
# Gzip Settings
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_min_length 1024;
gzip_types
    application/javascript
    application/json
    application/xml
    application/xml+rss
    text/css
    text/javascript
    text/plain
    text/xml
    image/svg+xml;
gzip_disable "MSIE [1-6]\.";
```

## Performance Optimization

### Worker Processes Configuration

```nginx
# Set in nginx.conf
worker_processes auto;  # Automatically detect number of CPU cores
worker_rlimit_nofile 65535;  # Increase system file descriptor limit

events {
    worker_connections 1024;  # Maximum connections per worker
    multi_accept on;
    use epoll;  # Use efficient event processing method
}
```

### FastCGI Cache Configuration

```nginx
# Set up FastCGI cache
fastcgi_cache_path /tmp/nginx_cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;

location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_cache my_cache;
    fastcgi_cache_valid 200 60m;  # Cache successful responses for 60 minutes
    fastcgi_cache_use_stale error timeout http_500 http_503;
    fastcgi_cache_min_uses 1;
    fastcgi_cache_lock on;
}
```

## Security Hardening

### Enhanced Security Headers

```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
```

### Rate Limiting Configuration

```nginx
# Define limit zones
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

# Apply rate limiting to specific locations
location /login/ {
    limit_req zone=one burst=5 nodelay;
    proxy_pass http://backend;
}
```

## Monitoring and Troubleshooting

### Real-time Monitoring

1. Monitor active connections:

```bash
watch -n1 "netstat -an | grep :80 | wc -l"
```

2. Monitor Nginx access logs in real-time:

```bash
sudo tail -f /var/log/nginx/access.log | ccze -A  # ccze for colored output
```

3. Check for syntax errors:

```bash
sudo nginx -t
```

### Common Issues and Solutions

1. 502 Bad Gateway:

- Check if backend service is running
- Verify proxy_pass configuration
- Check backend service logs

2. Permission Issues:

```bash
# Fix file permissions
sudo chown -R www-data:www-data /var/www/your_domain
sudo chmod -R 755 /var/www/your_domain
```

3. SSL Certificate Issues:

```bash
# Test SSL configuration
sudo openssl s_client -connect your_domain.com:443 -tls1_2