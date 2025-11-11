# GitLab configuration file

# External URL
external_url 'https://gitlab.yourdomain.com'

# GitLab Redis settings
gitlab_rails['redis_host'] = "127.0.0.1"
gitlab_rails['redis_port'] = 6379

# GitLab PostgreSQL settings
postgresql['enable'] = true
postgresql['username'] = "gitlab"
postgresql['password'] = "secure_password_here"
postgresql['database'] = "gitlabhq_production"

# GitLab email settings
gitlab_rails['gitlab_email_enabled'] = true
gitlab_rails['gitlab_email_from'] = 'gitlab@yourdomain.com'
gitlab_rails['gitlab_email_display_name'] = 'GitLab'

# Backup settings
gitlab_rails['backup_path'] = "/var/opt/gitlab/backups"
gitlab_rails['backup_keep_time'] = 604800

# LDAP configuration (optional)
# gitlab_rails['ldap_enabled'] = true
# gitlab_rails['ldap_servers'] = {
#   'main' => {
#     'label' => 'LDAP',
#     'host' =>  'ldap.example.com',
#     'port' => 389,
#     'uid' => 'sAMAccountName',
#     'bind_dn' => 'CN=Service Account,CN=Users,DC=example,DC=com',
#     'password' => 'ldap_password',
#     'base' => 'DC=example,DC=com'
#   }
# }

# Container Registry settings
registry_external_url 'https://registry.yourdomain.com'
registry['enable'] = true

# GitLab Pages settings
pages_external_url "https://pages.yourdomain.com"
gitlab_pages['enable'] = true

# Monitoring
prometheus['enable'] = true
grafana['enable'] = true

# Rate limiting
gitlab_rails['rack_attack_git_basic_auth'] = {
  'enabled' => true,
  'ip_whitelist' => ["127.0.0.1"],
  'maxretry' => 10,
  'findtime' => 60,
  'bantime' => 3600
}
