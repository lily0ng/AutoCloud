# Version Control System Setup and Configuration Guide

This repository contains comprehensive configurations and automation scripts for setting up and managing version control systems including Git, GitLab, and GitBucket.

## Table of Contents
1. [Directory Structure](#directory-structure)
2. [Git Configuration](#git-configuration)
3. [GitLab Setup](#gitlab-setup)
4. [GitLab CI/CD Configuration](#gitlab-cicd)
5. [GitLab Automations](#gitlab-automations)
6. [GitBucket Setup](#gitbucket-setup)
7. [Maintenance and Backups](#maintenance-and-backups)
8. [Webhooks and Integrations](#webhooks-and-integrations)

## Directory Structure
```
Version_Control/
├── git/
│   └── .gitconfig                 # Git global configuration
├── gitlab/
│   ├── gitlab.rb                  # GitLab server configuration
│   ├── .gitlab-ci.yml            # Basic CI/CD configuration
│   ├── config/
│   │   ├── advanced-gitlab-ci.yml # Advanced CI/CD configuration
│   │   └── webhooks.yml          # Webhook configurations
│   └── scripts/
│       └── gitlab_automation.sh   # GitLab automation scripts
├── gitbucket/
│   └── gitbucket.conf            # GitBucket configuration
├── scripts/
│   └── maintenance.sh            # Maintenance and backup scripts
└── README.md
```

## Git Configuration
### Basic Setup
1. Copy the `.gitconfig` file:
```bash
cp git/.gitconfig ~/.gitconfig
```

2. Configure user information:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Features
- Custom aliases for common commands
- Default branch configuration
- Merge and diff tool settings
- Credential helper configuration

## GitLab Setup
### Server Installation
1. Install GitLab:
```bash
curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
sudo apt-get install gitlab-ce
```

2. Configure GitLab:
```bash
sudo cp gitlab/gitlab.rb /etc/gitlab/gitlab.rb
sudo gitlab-ctl reconfigure
```

### Configuration Features
- External URL configuration
- Database settings
- Redis configuration
- Email settings
- Backup configuration
- LDAP integration
- Container registry
- Pages configuration
- Monitoring setup

## GitLab CI/CD Configuration
### Basic Pipeline
- Standard testing and deployment stages
- Docker build configuration
- Kubernetes deployment

### Advanced Pipeline Features (`advanced-gitlab-ci.yml`)
- Multi-environment deployments
- Security scanning (SAST, Secret Detection)
- Dependency scanning
- Code quality checks
- Performance monitoring
- Automated cleanup
- Environment-specific configurations

## GitLab Automations
### Project Management Script (`gitlab_automation.sh`)
```bash
./gitlab/scripts/gitlab_automation.sh [command] [args...]
```

Available commands:
- `create`: Create new project
- `protect`: Set branch protection
- `labels`: Setup default labels
- `templates`: Create MR templates
- `cicd`: Configure CI/CD
- `setup-all`: Complete project setup

## Webhooks and Integrations
### Configuration (`webhooks.yml`)
- Deployment webhooks
- Monitoring integration
- Security scanning
- Issue tracking
- Notification settings (Email/Slack)

### Setup
1. Access GitLab admin area
2. Configure webhooks using `webhooks.yml`
3. Set up authentication tokens
4. Configure notification channels

## GitBucket Setup
1. Download GitBucket:
```bash
wget https://github.com/gitbucket/gitbucket/releases/latest/download/gitbucket.war
```

2. Configure:
```bash
mkdir -p ~/.gitbucket
cp gitbucket/gitbucket.conf ~/.gitbucket/
```

3. Run GitBucket:
```bash
java -jar gitbucket.war
```

### Configuration Features
- Authentication settings
- Database configuration
- Repository settings
- Plugin management
- SMTP configuration

## Maintenance and Backups
### Automated Maintenance Script
```bash
./scripts/maintenance.sh [command]
```

Available commands:
- `backup`: Create GitLab and GitBucket backups
- `maintenance`: System maintenance tasks
- `update`: Update GitLab and GitBucket
- `health`: Run health checks
- `all`: Execute all maintenance tasks

### Scheduling Maintenance
Add to crontab:
```bash
# Daily backups
0 2 * * * /path/to/maintenance.sh backup

# Weekly maintenance
0 3 * * 0 /path/to/maintenance.sh maintenance

# Weekly updates
0 4 * * 1 /path/to/maintenance.sh update

# Health checks every 15 minutes
*/15 * * * * /path/to/maintenance.sh health
```

## Best Practices
### Git
- Use meaningful commit messages
- Create feature branches
- Regular pulls from main branch
- Use `.gitignore` for sensitive files

### GitLab
- Enable 2FA for all users
- Regular backups
- Use merge request templates
- Configure protected branches
- Regular security updates

### CI/CD
- Use stages for organized pipeline
- Cache dependencies
- Use environment variables for secrets
- Implement proper testing
- Regular security scanning

### Security
- Regular security updates
- Access control review
- Enable audit logging
- Configure SSL/TLS
- Regular backup testing

## Troubleshooting
### Common Issues
1. GitLab Connection Issues
   - Check external URL configuration
   - Verify SSL certificates
   - Check firewall settings

2. CI/CD Pipeline Failures
   - Verify runner configuration
   - Check environment variables
   - Review pipeline logs

3. Backup Failures
   - Check disk space
   - Verify permissions
   - Review backup logs

### Getting Help
- Check GitLab documentation
- Review system logs
- Contact system administrator
- Open issues in GitLab
