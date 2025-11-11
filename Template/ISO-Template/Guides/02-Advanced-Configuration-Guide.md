# Advanced ISO Template Configuration Guide

## Table of Contents
1. [Network Configuration](#network-configuration)
2. [Storage Configuration](#storage-configuration)
3. [Security Configuration](#security-configuration)
4. [Post-Installation Scripts](#post-installation-scripts)
5. [Multi-Node Deployments](#multi-node-deployments)

## Network Configuration

### Static IP Configuration
```json
{
  "network": {
    "version": 2,
    "ethernets": {
      "eth0": {
        "addresses": ["192.168.1.100/24"],
        "gateway4": "192.168.1.1",
        "nameservers": {
          "addresses": ["8.8.8.8", "8.8.4.4"]
        }
      }
    }
  }
}
```

### VLAN Configuration
```json
{
  "network": {
    "version": 2,
    "ethernets": {
      "eth0": {}
    },
    "vlans": {
      "vlan10": {
        "id": 10,
        "link": "eth0",
        "addresses": ["10.0.10.100/24"]
      },
      "vlan20": {
        "id": 20,
        "link": "eth0",
        "addresses": ["10.0.20.100/24"]
      }
    }
  }
}
```

### Bonding/Teaming
```json
{
  "network": {
    "version": 2,
    "bonds": {
      "bond0": {
        "interfaces": ["eth0", "eth1"],
        "parameters": {
          "mode": "active-backup",
          "primary": "eth0"
        },
        "addresses": ["192.168.1.100/24"]
      }
    }
  }
}
```

### Bridge Configuration
```json
{
  "network": {
    "version": 2,
    "ethernets": {
      "eth0": {}
    },
    "bridges": {
      "br0": {
        "interfaces": ["eth0"],
        "addresses": ["192.168.1.100/24"],
        "parameters": {
          "stp": true,
          "forward-delay": 4
        }
      }
    }
  }
}
```

## Storage Configuration

### LVM with Multiple Volumes
```json
{
  "storage": {
    "layout": {
      "name": "lvm",
      "match": {
        "size": "largest"
      }
    },
    "config": [
      {
        "type": "disk",
        "id": "disk0",
        "path": "/dev/sda"
      },
      {
        "type": "lvm_volgroup",
        "id": "vg0",
        "name": "vg0",
        "devices": ["disk0"]
      },
      {
        "type": "lvm_partition",
        "id": "lv_root",
        "volgroup": "vg0",
        "name": "root",
        "size": "20G"
      },
      {
        "type": "lvm_partition",
        "id": "lv_var",
        "volgroup": "vg0",
        "name": "var",
        "size": "10G"
      },
      {
        "type": "lvm_partition",
        "id": "lv_home",
        "volgroup": "vg0",
        "name": "home",
        "size": "30G"
      }
    ]
  }
}
```

### RAID Configuration
```json
{
  "storage": {
    "config": [
      {
        "type": "disk",
        "id": "disk0",
        "path": "/dev/sda"
      },
      {
        "type": "disk",
        "id": "disk1",
        "path": "/dev/sdb"
      },
      {
        "type": "raid",
        "id": "md0",
        "name": "md0",
        "raidlevel": 1,
        "devices": ["disk0", "disk1"]
      },
      {
        "type": "format",
        "id": "format0",
        "volume": "md0",
        "fstype": "ext4"
      },
      {
        "type": "mount",
        "id": "mount0",
        "device": "format0",
        "path": "/"
      }
    ]
  }
}
```

### Encrypted Partitions
```json
{
  "storage": {
    "config": [
      {
        "type": "disk",
        "id": "disk0",
        "path": "/dev/sda"
      },
      {
        "type": "partition",
        "id": "part0",
        "device": "disk0",
        "size": "100%"
      },
      {
        "type": "dm_crypt",
        "id": "dmcrypt0",
        "volume": "part0",
        "key": "{{ENCRYPTION_KEY}}"
      },
      {
        "type": "format",
        "id": "format0",
        "volume": "dmcrypt0",
        "fstype": "ext4"
      }
    ]
  }
}
```

## Security Configuration

### SSH Hardening
```json
{
  "ssh": {
    "install-server": true,
    "allow-pw": false,
    "authorized-keys": [
      "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC..."
    ]
  },
  "late-commands": [
    "echo 'PermitRootLogin no' >> /target/etc/ssh/sshd_config",
    "echo 'PasswordAuthentication no' >> /target/etc/ssh/sshd_config",
    "echo 'PubkeyAuthentication yes' >> /target/etc/ssh/sshd_config",
    "echo 'Protocol 2' >> /target/etc/ssh/sshd_config",
    "echo 'MaxAuthTries 3' >> /target/etc/ssh/sshd_config"
  ]
}
```

### Firewall Configuration
```json
{
  "late-commands": [
    "in-target apt-get install -y ufw",
    "in-target ufw default deny incoming",
    "in-target ufw default allow outgoing",
    "in-target ufw allow 22/tcp",
    "in-target ufw allow 80/tcp",
    "in-target ufw allow 443/tcp",
    "in-target ufw --force enable"
  ]
}
```

### SELinux/AppArmor
```json
{
  "packages": ["selinux-basics", "selinux-policy-default"],
  "late-commands": [
    "in-target selinux-activate",
    "in-target selinux-config-enforcing"
  ]
}
```

## Post-Installation Scripts

### System Hardening Script
```json
{
  "late-commands": [
    "curtin in-target -- bash -c 'curl -sSL https://example.com/harden.sh | bash'"
  ]
}
```

### Docker Installation
```json
{
  "late-commands": [
    "in-target curl -fsSL https://get.docker.com -o get-docker.sh",
    "in-target sh get-docker.sh",
    "in-target usermod -aG docker {{USERNAME}}",
    "in-target systemctl enable docker",
    "in-target systemctl start docker"
  ]
}
```

### Kubernetes Node Setup
```json
{
  "late-commands": [
    "in-target curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -",
    "in-target echo 'deb https://apt.kubernetes.io/ kubernetes-xenial main' > /etc/apt/sources.list.d/kubernetes.list",
    "in-target apt-get update",
    "in-target apt-get install -y kubelet kubeadm kubectl",
    "in-target apt-mark hold kubelet kubeadm kubectl"
  ]
}
```

## Multi-Node Deployments

### Cluster Template
```json
{
  "cluster": {
    "name": "k8s-cluster",
    "nodes": [
      {
        "role": "master",
        "count": 3,
        "template": "ubuntu-22.04-server.json",
        "cpu": 4,
        "ram": 8192,
        "disk": 50
      },
      {
        "role": "worker",
        "count": 5,
        "template": "ubuntu-22.04-server.json",
        "cpu": 8,
        "ram": 16384,
        "disk": 100
      }
    ],
    "network": {
      "pod_cidr": "10.244.0.0/16",
      "service_cidr": "10.96.0.0/12"
    }
  }
}
```

### Load Balancer Configuration
```json
{
  "load_balancer": {
    "type": "haproxy",
    "frontend": {
      "bind": "*:80",
      "mode": "http"
    },
    "backend": {
      "balance": "roundrobin",
      "servers": [
        {"name": "web1", "address": "192.168.1.101:80"},
        {"name": "web2", "address": "192.168.1.102:80"},
        {"name": "web3", "address": "192.168.1.103:80"}
      ]
    }
  }
}
```

## Advanced Features

### Cloud-Init Integration
```json
{
  "cloud_init": {
    "user_data": {
      "package_upgrade": true,
      "packages": ["docker.io", "nginx"],
      "runcmd": [
        "systemctl start docker",
        "systemctl enable docker"
      ]
    }
  }
}
```

### Ansible Integration
```json
{
  "post_install": {
    "ansible": {
      "playbook": "site.yml",
      "inventory": "hosts",
      "extra_vars": {
        "env": "production"
      }
    }
  }
}
```

## Performance Tuning

### Kernel Parameters
```json
{
  "late-commands": [
    "echo 'vm.swappiness=10' >> /target/etc/sysctl.conf",
    "echo 'net.ipv4.tcp_fin_timeout=30' >> /target/etc/sysctl.conf",
    "echo 'net.core.somaxconn=1024' >> /target/etc/sysctl.conf"
  ]
}
```

### Resource Limits
```json
{
  "late-commands": [
    "echo '* soft nofile 65536' >> /target/etc/security/limits.conf",
    "echo '* hard nofile 65536' >> /target/etc/security/limits.conf"
  ]
}
```

## Conclusion
This guide covers advanced configuration options for ISO templates. Combine these techniques to create sophisticated, production-ready deployments.
