# Docker Hub Templates Collection

Complete collection of 35 production-ready Docker Compose templates for popular open-source applications.

## 📦 Templates Overview

### Web Applications (5 templates)
1. **wordpress-blog-template.yml** - WordPress + MySQL + Redis + Nginx
2. **ghost-cms-template.yml** - Ghost CMS + MySQL
3. **drupal-template.yml** - Drupal + MySQL
4. **joomla-template.yml** - Joomla + MySQL
5. **mediawiki-template.yml** - MediaWiki + MySQL

### E-commerce & Business (5 templates)
6. **magento-template.yml** - Magento + MariaDB + Elasticsearch
7. **odoo-erp-template.yml** - Odoo ERP + PostgreSQL
8. **saleor-template.yml** - Saleor E-commerce + PostgreSQL + Redis
9. **pretix-template.yml** - Pretix Ticketing + PostgreSQL + Redis
10. **dolibarr-template.yml** - Dolibarr ERP + MariaDB

### Development Tools (5 templates)
11. **gitlab-ce-template.yml** - GitLab CE + GitLab Runner
12. **gitea-template.yml** - Gitea + PostgreSQL
13. **jenkins-template.yml** - Jenkins + Agent
14. **sonarqube-template.yml** - SonarQube + PostgreSQL
15. **nexus-template.yml** - Nexus Repository Manager

### Collaboration & Communication (5 templates)
16. **mattermost-template.yml** - Mattermost + PostgreSQL
17. **rocketchat-template.yml** - Rocket.Chat + MongoDB
18. **nextcloud-template.yml** - Nextcloud + PostgreSQL + Redis
19. **discourse-template.yml** - Discourse + PostgreSQL + Redis
20. **matrix-synapse-template.yml** - Matrix Synapse + PostgreSQL

### Monitoring & Analytics (5 templates)
21. **grafana-prometheus-template.yml** - Grafana + Prometheus + AlertManager + Node Exporter
22. **zabbix-template.yml** - Zabbix Server + Web + PostgreSQL
23. **metabase-template.yml** - Metabase + PostgreSQL
24. **netdata-template.yml** - NetData Real-time Monitoring

### Database & Storage (5 templates)
25. **postgresql-template.yml** - PostgreSQL + pgAdmin
26. **redis-template.yml** - Redis + Redis Commander
27. **mongodb-template.yml** - MongoDB + Mongo Express
28. **mysql-template.yml** - MySQL + phpMyAdmin
29. **minio-template.yml** - MinIO Object Storage

### Application Stacks (6 templates)
30. **lamp-stack-template.yml** - Linux + Apache + MySQL + PHP
31. **lemp-stack-template.yml** - Linux + Nginx + MySQL + PHP
32. **mean-stack-template.yml** - MongoDB + Express + Angular + Node.js
33. **mern-stack-template.yml** - MongoDB + Express + React + Node.js
34. **django-template.yml** - Django + PostgreSQL + Redis + Nginx

## 🚀 Quick Start

### Basic Usage

```bash
# Clone or download the template
cd Template/DockerHub

# Start any application
docker-compose -f wordpress-blog-template.yml up -d

# View logs
docker-compose -f wordpress-blog-template.yml logs -f

# Stop application
docker-compose -f wordpress-blog-template.yml down
```

### With Environment Variables

```bash
# Create .env file
cat > .env << EOF
DB_PASSWORD=securepassword123
ADMIN_PASSWORD=adminpass456
REDIS_PASSWORD=redispass789
EOF

# Start with environment
docker-compose -f nextcloud-template.yml --env-file .env up -d
```

## 🔧 Configuration

### Environment Variables

Most templates support these common variables:

```bash
# Database
DB_PASSWORD=your_db_password
MYSQL_ROOT_PASSWORD=root_password
POSTGRES_PASSWORD=postgres_password
MONGO_PASSWORD=mongo_password

# Admin Credentials
ADMIN_USER=admin
ADMIN_PASSWORD=admin_password

# Cache
REDIS_PASSWORD=redis_password

# Email (for applications that need it)
SMTP_ADDRESS=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Customization

Each template can be customized by:

1. **Editing the compose file** - Modify ports, volumes, environment variables
2. **Adding volumes** - Mount configuration files or data directories
3. **Networking** - Connect multiple services across templates
4. **Resource limits** - Add memory/CPU constraints

Example:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## 📊 Resource Requirements

### Minimum Requirements

| Template | CPU | RAM | Storage |
|----------|-----|-----|---------|
| WordPress | 1 core | 1GB | 10GB |
| GitLab CE | 4 cores | 8GB | 50GB |
| Nextcloud | 2 cores | 2GB | 20GB |
| Grafana+Prometheus | 2 cores | 4GB | 20GB |
| Magento | 4 cores | 4GB | 30GB |

### Recommended for Production

- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB for heavy applications)
- **Storage**: SSD with 100GB+ available
- **Network**: 1Gbps connection

## 🔒 Security Best Practices

1. **Change Default Passwords**
   ```bash
   # Always set strong passwords in .env
   DB_PASSWORD=$(openssl rand -base64 32)
   ```

2. **Use Secrets Management**
   ```yaml
   services:
     app:
       secrets:
         - db_password
   secrets:
     db_password:
       file: ./secrets/db_password.txt
   ```

3. **Enable SSL/TLS**
   - Use reverse proxy (Nginx/Traefik)
   - Mount SSL certificates
   - Enable HTTPS redirects

4. **Network Isolation**
   ```yaml
   networks:
     frontend:
       driver: bridge
     backend:
       driver: bridge
       internal: true
   ```

5. **Regular Updates**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

## 🔄 Backup & Restore

### Backup Volumes

```bash
# Backup all volumes
docker run --rm -v wordpress_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/wordpress_backup_$(date +%Y%m%d).tar.gz /data

# Backup database
docker exec wordpress_mysql mysqldump -u root -p wordpress > backup.sql
```

### Restore Volumes

```bash
# Restore volume
docker run --rm -v wordpress_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/wordpress_backup_20231101.tar.gz -C /

# Restore database
docker exec -i wordpress_mysql mysql -u root -p wordpress < backup.sql
```

## 📈 Monitoring

### Health Checks

Add health checks to services:

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Logging

Configure logging drivers:

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Check what's using the port
sudo lsof -i :80

# Change port in compose file
ports: ["8080:80"]
```

**Permission Denied**
```bash
# Fix volume permissions
sudo chown -R 1000:1000 ./data
```

**Container Won't Start**
```bash
# Check logs
docker-compose logs app

# Inspect container
docker inspect container_name
```

**Database Connection Failed**
```bash
# Wait for database to be ready
docker-compose up -d db
sleep 30
docker-compose up -d app
```

## 🔗 Integration Examples

### Multiple Services

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  wordpress:
    networks:
      - monitoring
  
networks:
  monitoring:
    external: true
    name: grafana-prometheus_monitoring
```

### Reverse Proxy

```yaml
# nginx-proxy.yml
version: '3.8'
services:
  nginx-proxy:
    image: nginxproxy/nginx-proxy
    ports: ["80:80", "443:443"]
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - ./certs:/etc/nginx/certs
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Hub](https://hub.docker.com/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 📝 License

These templates are provided as-is for production use. Customize according to your requirements.

## 🤝 Contributing

To add new templates:
1. Follow the existing format
2. Include all necessary services
3. Add environment variables
4. Test thoroughly
5. Document special requirements
