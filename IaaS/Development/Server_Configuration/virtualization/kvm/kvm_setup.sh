#!/bin/bash

# KVM Installation and Configuration Script
set -e

echo "Starting KVM installation and configuration..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Install required packages
echo "Installing KVM and related packages..."
apt-get update
apt-get install -y \
    qemu-kvm \
    libvirt-daemon-system \
    libvirt-clients \
    bridge-utils \
    virt-manager \
    virtinst

# Enable and start libvirtd service
systemctl enable libvirtd
systemctl start libvirtd

# Configure networking bridge
cat > /etc/netplan/01-netcfg.yaml << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: no
  bridges:
    br0:
      interfaces: [ens33]
      dhcp4: yes
EOF

# Apply network configuration
netplan apply

# Create default storage pool
virsh pool-define-as --name default --type dir --target /var/lib/libvirt/images
virsh pool-build default
virsh pool-start default
virsh pool-autostart default

# Configure QEMU settings
sed -i 's/#security_driver = "selinux"/security_driver = "none"/' /etc/libvirt/qemu.conf
systemctl restart libvirtd

# Verify installation
echo "Verifying KVM installation..."
if [ -c /dev/kvm ]; then
    echo "KVM installation successful!"
else
    echo "KVM installation failed!"
    exit 1
fi

# Check virtualization support
if grep -E 'svm|vmx' /proc/cpuinfo > /dev/null; then
    echo "CPU supports hardware virtualization"
else
    echo "CPU does not support hardware virtualization!"
    exit 1
fi

echo "KVM setup completed successfully!"
