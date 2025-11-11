# Security Hardening Guide for ISO Templates

## Overview
This guide provides security best practices and hardening techniques for ISO templates to ensure secure deployments.

## Table of Contents
1. [Pre-Installation Security](#pre-installation-security)
2. [User and Access Control](#user-and-access-control)
3. [Network Security](#network-security)
4. [System Hardening](#system-hardening)
5. [Compliance and Auditing](#compliance-and-auditing)

## Pre-Installation Security

### Secure Boot Configuration
```json
{
  "boot_security": {
    "secure_boot": true,
    "tpm_required": true,
    "disk_encryption": true
  }
}
```

### ISO Verification
```bash
# Always verify ISO checksums
sha256sum -c <<< "expected_checksum  os.iso"

# Verify GPG signature
gpg --verify os.iso.sig os.iso
```

### Template Validation
```json
{
  "security_checks": {
    "verify_iso_checksum": true,
    "scan_for_malware": true,
    "validate_signatures": true
  }
}
```

## User and Access Control

### Disable Root Login
```json
{
  "users": [
    {
      "name": "admin",
      "groups": ["sudo", "wheel"],
      "shell": "/bin/bash",
      "sudo": "NOPASSWD:ALL"
    }
  ],
  "root_account": {
    "locked": true,
    "password_login": false
  }
}
```

### SSH Key-Based Authentication
```json
{
  "ssh": {
    "password_authentication": false,
    "pubkey_authentication": true,
    "permit_root_login": "no",
    "authorized_keys": [
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... user@host"
    ]
  }
}
```

### Strong Password Policy
```json
{
  "password_policy": {
    "min_length": 14,
    "require_uppercase": true,
    "require_lowercase": true,
    "require_numbers": true,
    "require_special": true,
    "max_age_days": 90,
    "min_age_days": 1,
    "remember_passwords": 5
  },
  "late-commands": [
    "echo 'password requisite pam_pwquality.so retry=3 minlen=14 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1' >> /target/etc/pam.d/common-password"
  ]
}
```

### Multi-Factor Authentication
```json
{
  "packages": ["libpam-google-authenticator"],
  "post_install": {
    "commands": [
      "echo 'auth required pam_google_authenticator.so' >> /etc/pam.d/sshd"
    ]
  }
}
```

## Network Security

### Firewall Configuration
```json
{
  "firewall": {
    "enabled": true,
    "default_policy": "deny",
    "rules": [
      {
        "port": 22,
        "protocol": "tcp",
        "source": "10.0.0.0/8",
        "action": "allow"
      },
      {
        "port": 443,
        "protocol": "tcp",
        "action": "allow"
      }
    ]
  },
  "late-commands": [
    "in-target ufw default deny incoming",
    "in-target ufw default allow outgoing",
    "in-target ufw allow from 10.0.0.0/8 to any port 22",
    "in-target ufw allow 443/tcp",
    "in-target ufw --force enable"
  ]
}
```

### SSH Hardening
```json
{
  "ssh_config": {
    "Port": 2222,
    "Protocol": 2,
    "PermitRootLogin": "no",
    "PasswordAuthentication": "no",
    "PubkeyAuthentication": "yes",
    "PermitEmptyPasswords": "no",
    "X11Forwarding": "no",
    "MaxAuthTries": 3,
    "MaxSessions": 2,
    "ClientAliveInterval": 300,
    "ClientAliveCountMax": 2,
    "AllowUsers": "admin deploy",
    "DenyUsers": "root",
    "Ciphers": "chacha20-poly1305@openssh.com,aes256-gcm@openssh.com",
    "MACs": "hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com",
    "KexAlgorithms": "curve25519-sha256,curve25519-sha256@libssh.org"
  }
}
```

### Network Segmentation
```json
{
  "network": {
    "vlans": [
      {
        "id": 10,
        "name": "management",
        "subnet": "10.0.10.0/24"
      },
      {
        "id": 20,
        "name": "application",
        "subnet": "10.0.20.0/24"
      },
      {
        "id": 30,
        "name": "database",
        "subnet": "10.0.30.0/24"
      }
    ]
  }
}
```

### Intrusion Detection
```json
{
  "packages": ["fail2ban", "aide"],
  "fail2ban_config": {
    "enabled": true,
    "bantime": 3600,
    "findtime": 600,
    "maxretry": 3,
    "jails": [
      {
        "name": "sshd",
        "enabled": true,
        "port": "ssh",
        "logpath": "/var/log/auth.log"
      }
    ]
  }
}
```

## System Hardening

### Kernel Hardening
```json
{
  "sysctl_config": {
    "net.ipv4.conf.all.rp_filter": 1,
    "net.ipv4.conf.default.rp_filter": 1,
    "net.ipv4.icmp_echo_ignore_broadcasts": 1,
    "net.ipv4.conf.all.accept_source_route": 0,
    "net.ipv4.conf.default.accept_source_route": 0,
    "net.ipv4.conf.all.send_redirects": 0,
    "net.ipv4.conf.default.send_redirects": 0,
    "net.ipv4.tcp_syncookies": 1,
    "net.ipv4.tcp_max_syn_backlog": 2048,
    "net.ipv4.tcp_synack_retries": 2,
    "net.ipv4.tcp_syn_retries": 5,
    "kernel.randomize_va_space": 2,
    "kernel.exec-shield": 1,
    "kernel.kptr_restrict": 2
  }
}
```

### File System Security
```json
{
  "fstab_options": {
    "/tmp": "nodev,nosuid,noexec",
    "/var": "nodev",
    "/var/tmp": "nodev,nosuid,noexec",
    "/home": "nodev,nosuid"
  },
  "late-commands": [
    "echo 'tmpfs /tmp tmpfs defaults,nodev,nosuid,noexec 0 0' >> /target/etc/fstab",
    "echo 'tmpfs /var/tmp tmpfs defaults,nodev,nosuid,noexec 0 0' >> /target/etc/fstab"
  ]
}
```

### SELinux/AppArmor
```json
{
  "selinux": {
    "enabled": true,
    "mode": "enforcing",
    "policy": "targeted"
  },
  "packages": ["selinux-basics", "selinux-policy-default", "auditd"],
  "late-commands": [
    "in-target selinux-activate",
    "in-target selinux-config-enforcing"
  ]
}
```

### Disable Unnecessary Services
```json
{
  "services": {
    "disabled": [
      "avahi-daemon",
      "cups",
      "bluetooth",
      "iscsid",
      "rpcbind"
    ],
    "masked": [
      "ctrl-alt-del.target"
    ]
  }
}
```

### Audit Logging
```json
{
  "packages": ["auditd", "audispd-plugins"],
  "audit_rules": [
    "-w /etc/passwd -p wa -k passwd_changes",
    "-w /etc/group -p wa -k group_changes",
    "-w /etc/shadow -p wa -k shadow_changes",
    "-w /etc/sudoers -p wa -k sudoers_changes",
    "-w /var/log/lastlog -p wa -k logins",
    "-w /var/run/faillock/ -p wa -k logins",
    "-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change",
    "-w /etc/localtime -p wa -k time-change"
  ]
}
```

## Disk Encryption

### Full Disk Encryption
```json
{
  "storage": {
    "encryption": {
      "enabled": true,
      "method": "luks",
      "cipher": "aes-xts-plain64",
      "key_size": 512,
      "hash": "sha512"
    },
    "config": [
      {
        "type": "dm_crypt",
        "volume": "/dev/sda2",
        "key": "{{ENCRYPTION_KEY}}"
      }
    ]
  }
}
```

### Encrypted Swap
```json
{
  "late-commands": [
    "echo 'swap /dev/mapper/cryptswap /dev/urandom swap,cipher=aes-xts-plain64,size=256' >> /target/etc/crypttab"
  ]
}
```

## Compliance and Auditing

### CIS Benchmark Compliance
```json
{
  "compliance": {
    "framework": "CIS",
    "level": 2,
    "automated_remediation": true
  },
  "packages": ["cis-cat-lite"],
  "post_install": {
    "commands": [
      "cis-cat-lite --benchmark CIS_Ubuntu_Linux_22.04_Benchmark_v1.0.0"
    ]
  }
}
```

### STIG Compliance
```json
{
  "compliance": {
    "framework": "STIG",
    "version": "V1R1"
  },
  "packages": ["scap-security-guide"],
  "post_install": {
    "commands": [
      "oscap xccdf eval --profile stig --results-arf arf.xml /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml"
    ]
  }
}
```

### Automated Security Scanning
```json
{
  "security_scanning": {
    "enabled": true,
    "tools": ["lynis", "rkhunter", "chkrootkit"],
    "schedule": "daily"
  },
  "packages": ["lynis", "rkhunter", "chkrootkit"],
  "post_install": {
    "commands": [
      "lynis audit system --quick",
      "rkhunter --update",
      "rkhunter --propupd"
    ]
  }
}
```

## Security Monitoring

### Log Management
```json
{
  "logging": {
    "centralized": true,
    "syslog_server": "syslog.example.com:514",
    "retention_days": 90
  },
  "packages": ["rsyslog", "logrotate"],
  "late-commands": [
    "echo '*.* @@syslog.example.com:514' >> /target/etc/rsyslog.conf"
  ]
}
```

### Security Updates
```json
{
  "automatic_updates": {
    "enabled": true,
    "security_only": true,
    "reboot_if_required": true,
    "reboot_time": "03:00"
  },
  "packages": ["unattended-upgrades"],
  "late-commands": [
    "echo 'Unattended-Upgrade::Automatic-Reboot \"true\";' >> /target/etc/apt/apt.conf.d/50unattended-upgrades"
  ]
}
```

## Best Practices Checklist

- [ ] Disable root login
- [ ] Use SSH keys only
- [ ] Enable firewall
- [ ] Configure SELinux/AppArmor
- [ ] Enable disk encryption
- [ ] Implement strong password policy
- [ ] Disable unnecessary services
- [ ] Configure audit logging
- [ ] Enable automatic security updates
- [ ] Implement intrusion detection
- [ ] Configure centralized logging
- [ ] Regular security scanning
- [ ] Compliance validation
- [ ] Network segmentation
- [ ] Multi-factor authentication

## Conclusion
Security hardening is an ongoing process. Regularly review and update your templates to address new threats and vulnerabilities.
