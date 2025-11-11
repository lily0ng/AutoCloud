# Custom ISO Template Creation Guide

## Introduction
Learn how to create custom ISO templates for any operating system or specialized deployment scenario.

## Template Structure

### Basic Template Schema
```json
{
  "name": "string",
  "version": "string",
  "type": "string",
  "distribution": "string",
  "architecture": "string",
  "iso_url": "string",
  "checksum": "string",
  "boot_command": ["array"],
  "system_requirements": {
    "min_ram": "string",
    "min_disk": "string",
    "min_cpu": "string"
  },
  "installation_config": {}
}
```

### Required Fields
- **name**: Human-readable OS name
- **version**: OS version number
- **type**: OS category (linux, windows, bsd, etc.)
- **iso_url**: Direct download link to ISO
- **checksum**: SHA256 checksum for verification

### Optional Fields
- **distribution**: Specific distro (ubuntu, centos, etc.)
- **architecture**: CPU architecture (x86_64, arm64, etc.)
- **boot_command**: Automated boot sequence
- **system_requirements**: Minimum hardware specs

## Step-by-Step Creation

### Step 1: Gather Information
```bash
# Download ISO
wget https://example.com/os.iso

# Calculate checksum
sha256sum os.iso

# Test boot in VM
qemu-system-x86_64 -cdrom os.iso -m 2048
```

### Step 2: Create Base Template
```json
{
  "name": "Custom Linux Distribution",
  "version": "1.0",
  "type": "linux",
  "distribution": "custom",
  "architecture": "x86_64",
  "iso_url": "https://example.com/custom-linux-1.0.iso",
  "checksum": "sha256:abc123...",
  "system_requirements": {
    "min_ram": "2048",
    "min_disk": "20",
    "min_cpu": "2"
  }
}
```

### Step 3: Configure Boot Command
```json
{
  "boot_command": [
    "<esc><wait>",
    "linux /casper/vmlinuz autoinstall ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/",
    "<enter><wait>",
    "initrd /casper/initrd",
    "<enter><wait>",
    "boot<enter>"
  ]
}
```

### Step 4: Add Installation Configuration

#### For Debian/Ubuntu (Preseed)
```json
{
  "preseed": {
    "locale": "en_US.UTF-8",
    "keyboard": "us",
    "network": {
      "auto": true
    },
    "partitioning": {
      "method": "regular",
      "disk": "/dev/sda"
    },
    "accounts": {
      "user": {
        "username": "admin",
        "password": "encrypted_password"
      }
    }
  }
}
```

#### For RHEL/CentOS (Kickstart)
```json
{
  "kickstart": {
    "install": true,
    "text": true,
    "lang": "en_US.UTF-8",
    "keyboard": "us",
    "network": "--bootproto=dhcp",
    "rootpw": "--iscrypted $6$...",
    "bootloader": "--location=mbr",
    "zerombr": true,
    "clearpart": "--all --initlabel",
    "autopart": true,
    "packages": ["@core"]
  }
}
```

#### For Windows (Autounattend)
```json
{
  "autounattend": {
    "settings": {
      "windowsPE": {
        "setupUILanguage": "en-US"
      },
      "diskConfiguration": {
        "disk": {
          "diskID": "0",
          "willWipeDisk": true
        }
      }
    }
  }
}
```

### Step 5: Add Post-Installation Tasks
```json
{
  "post_install": {
    "scripts": [
      "#!/bin/bash",
      "apt-get update",
      "apt-get install -y vim git curl",
      "systemctl enable ssh"
    ],
    "files": [
      {
        "path": "/etc/motd",
        "content": "Welcome to Custom Linux!"
      }
    ],
    "commands": [
      "useradd -m -s /bin/bash deploy",
      "echo 'deploy ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/deploy"
    ]
  }
}
```

## Testing Your Template

### Validation
```bash
# Validate JSON syntax
autocloud template validate custom-template.json

# Check for required fields
autocloud template check custom-template.json

# Verify ISO accessibility
autocloud template verify-iso custom-template.json
```

### Test Deployment
```bash
# Deploy to test environment
autocloud vm create --template custom-template.json \
  --name test-vm \
  --environment test \
  --auto-destroy 1h

# Monitor installation
autocloud vm logs test-vm --follow

# Verify installation
autocloud vm exec test-vm "uname -a"
```

## Advanced Customization

### Dynamic Variables
```json
{
  "variables": {
    "hostname": {
      "type": "string",
      "default": "server",
      "description": "System hostname"
    },
    "ip_address": {
      "type": "string",
      "required": true,
      "description": "Static IP address"
    },
    "packages": {
      "type": "array",
      "default": ["vim", "git"],
      "description": "Additional packages to install"
    }
  }
}
```

### Conditional Logic
```json
{
  "conditions": {
    "if": "{{ENVIRONMENT}} == 'production'",
    "then": {
      "packages": ["monitoring-agent", "security-tools"],
      "firewall": "enabled"
    },
    "else": {
      "packages": ["debug-tools"],
      "firewall": "disabled"
    }
  }
}
```

### Template Inheritance
```json
{
  "extends": "base-linux-template.json",
  "overrides": {
    "packages": ["custom-package"],
    "network": {
      "static_ip": true
    }
  }
}
```

## Best Practices

### 1. Version Control
```bash
git init
git add custom-template.json
git commit -m "Initial template version"
git tag v1.0.0
```

### 2. Documentation
```json
{
  "metadata": {
    "author": "Your Name",
    "created": "2024-01-01",
    "description": "Custom template for XYZ deployment",
    "changelog": [
      "v1.0.0 - Initial release",
      "v1.1.0 - Added Docker support"
    ]
  }
}
```

### 3. Security
- Never hardcode passwords
- Use encrypted passwords
- Store secrets in vault
- Implement key rotation

### 4. Testing Matrix
Test on multiple:
- Hypervisors (KVM, VMware, VirtualBox)
- Hardware configurations
- Network setups
- Storage backends

## Common Patterns

### Web Server Template
```json
{
  "name": "LAMP Stack Server",
  "packages": [
    "apache2",
    "mysql-server",
    "php",
    "php-mysql"
  ],
  "post_install": {
    "commands": [
      "systemctl enable apache2",
      "systemctl enable mysql",
      "a2enmod rewrite",
      "systemctl restart apache2"
    ]
  }
}
```

### Database Server Template
```json
{
  "name": "PostgreSQL Server",
  "packages": [
    "postgresql",
    "postgresql-contrib"
  ],
  "storage": {
    "data_dir": "/var/lib/postgresql",
    "size": "100G"
  },
  "post_install": {
    "commands": [
      "systemctl enable postgresql",
      "systemctl start postgresql"
    ]
  }
}
```

### Container Host Template
```json
{
  "name": "Docker Host",
  "packages": [
    "docker.io",
    "docker-compose"
  ],
  "post_install": {
    "commands": [
      "systemctl enable docker",
      "usermod -aG docker {{USERNAME}}",
      "docker network create app-network"
    ]
  }
}
```

## Troubleshooting

### Boot Command Issues
- Add `<wait>` between commands
- Increase wait times for slow systems
- Use serial console for debugging
- Check BIOS/UEFI settings

### Installation Hangs
- Verify preseed/kickstart syntax
- Check network connectivity
- Ensure ISO is not corrupted
- Review installation logs

### Post-Install Failures
- Test scripts independently
- Check file permissions
- Verify package availability
- Review system logs

## Publishing Templates

### Template Registry
```bash
# Publish to AutoCloud registry
autocloud template publish custom-template.json \
  --name "Custom Linux" \
  --version "1.0.0" \
  --public

# Update existing template
autocloud template update custom-template.json \
  --version "1.1.0"
```

### Sharing Templates
```bash
# Export template
autocloud template export custom-template.json \
  --output custom-template-bundle.tar.gz

# Import template
autocloud template import custom-template-bundle.tar.gz
```

## Resources
- ISO Download Sites
- Preseed Documentation
- Kickstart Reference
- Autounattend Guide
- Community Templates

## Conclusion
Creating custom templates enables automated, repeatable deployments tailored to your specific needs. Follow this guide to build robust, production-ready templates.
