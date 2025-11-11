#!/bin/bash

# Maintenance and Backup Script for Version Control Systems
# This script handles automated backups, updates, and maintenance tasks

# Configuration
BACKUP_DIR="/path/to/backups"
GITLAB_HOME="/etc/gitlab"
GITBUCKET_HOME="/path/to/gitbucket"
RETENTION_DAYS=30
LOG_FILE="/var/log/vcs_maintenance.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# GitLab Backup
gitlab_backup() {
    log "Starting GitLab backup..."
    
    # Create GitLab backup
    gitlab-rake gitlab:backup:create STRATEGY=copy
    
    # Backup GitLab configuration
    cp "$GITLAB_HOME/gitlab.rb" "$BACKUP_DIR/gitlab.rb.$(date +%Y%m%d)"
    cp "$GITLAB_HOME/gitlab-secrets.json" "$BACKUP_DIR/gitlab-secrets.json.$(date +%Y%m%d)"
    
    log "GitLab backup completed"
}

# GitBucket Backup
gitbucket_backup() {
    log "Starting GitBucket backup..."
    
    # Stop GitBucket service
    systemctl stop gitbucket
    
    # Backup GitBucket data
    tar -czf "$BACKUP_DIR/gitbucket_$(date +%Y%m%d).tar.gz" "$GITBUCKET_HOME"
    
    # Start GitBucket service
    systemctl start gitbucket
    
    log "GitBucket backup completed"
}

# System maintenance
system_maintenance() {
    log "Starting system maintenance..."
    
    # Clean old backups
    find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete
    
    # Clean Docker images
    docker system prune -af --volumes
    
    # Clean GitLab CI/CD cache
    gitlab-rake gitlab:cleanup:purge_redis_cache
    gitlab-rake gitlab:cleanup:project_uploads
    
    log "System maintenance completed"
}

# Update GitLab
update_gitlab() {
    log "Starting GitLab update..."
    
    # Update GitLab packages
    apt-get update
    apt-get upgrade gitlab-ce
    
    # Reconfigure GitLab
    gitlab-ctl reconfigure
    
    log "GitLab update completed"
}

# Update GitBucket
update_gitbucket() {
    log "Starting GitBucket update..."
    
    # Download latest GitBucket release
    latest_version=$(curl -s https://api.github.com/repos/gitbucket/gitbucket/releases/latest | grep tag_name | cut -d '"' -f 4)
    wget "https://github.com/gitbucket/gitbucket/releases/download/$latest_version/gitbucket.war" -O /tmp/gitbucket.war
    
    # Stop service
    systemctl stop gitbucket
    
    # Backup current war
    cp /opt/gitbucket/gitbucket.war "/opt/gitbucket/gitbucket.war.$(date +%Y%m%d)"
    
    # Replace with new version
    mv /tmp/gitbucket.war /opt/gitbucket/gitbucket.war
    
    # Start service
    systemctl start gitbucket
    
    log "GitBucket update completed"
}

# Health check function
health_check() {
    log "Starting health checks..."
    
    # Check GitLab
    curl -sf http://localhost:80/health_check > /dev/null
    if [ $? -eq 0 ]; then
        log "GitLab health check: OK"
    else
        log "GitLab health check: FAILED"
        # Send alert
        send_alert "GitLab health check failed"
    fi
    
    # Check GitBucket
    curl -sf http://localhost:8080 > /dev/null
    if [ $? -eq 0 ]; then
        log "GitBucket health check: OK"
    else
        log "GitBucket health check: FAILED"
        # Send alert
        send_alert "GitBucket health check failed"
    fi
    
    log "Health checks completed"
}

# Alert function
send_alert() {
    # Replace with your preferred alerting mechanism
    echo "$1" | mail -s "VCS Alert" admin@yourdomain.com
}

# Main execution
case "$1" in
    "backup")
        gitlab_backup
        gitbucket_backup
        ;;
    "maintenance")
        system_maintenance
        ;;
    "update")
        update_gitlab
        update_gitbucket
        ;;
    "health")
        health_check
        ;;
    "all")
        gitlab_backup
        gitbucket_backup
        system_maintenance
        update_gitlab
        update_gitbucket
        health_check
        ;;
    *)
        echo "Usage: $0 {backup|maintenance|update|health|all}"
        exit 1
        ;;
esac

exit 0
