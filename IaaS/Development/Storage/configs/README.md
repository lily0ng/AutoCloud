# Storage Configurations

This directory contains storage configuration templates for various Linux distributions. Each configuration is designed to provide optimal storage setup while following distribution-specific best practices.

## Configuration Files

- `base_storage_config.yaml`: Base configuration template with common settings
- `ubuntu_storage.yaml`: Ubuntu-specific storage configuration
- `centos_storage.yaml`: CentOS-specific storage configuration
- `rocky_os9_storage.yaml`: Rocky OS 9-specific configuration
- `debian_storage.yaml`: Debian-based systems configuration

## Features

- LVM (Logical Volume Management) support
- Disk encryption configurations
- File system optimizations
- Maintenance schedules
- Backup configurations
- Performance tuning
- Security hardening

## Usage

1. Select the appropriate configuration file for your distribution
2. Modify the settings according to your needs
3. Apply the configuration using your system's storage management tools

## Common Settings

- File system types and mount options
- Partition schemes
- LVM configurations
- Backup and snapshot policies
- Maintenance schedules
- Security settings

## Distribution-Specific Features

### Ubuntu
- LUKS2 encryption
- Swap configuration
- TRIM scheduling

### CentOS
- XFS as default filesystem
- SELinux context configuration
- LVM snapshot support

### Rocky OS 9
- Stratis storage management
- Advanced encryption options
- IO scheduler optimization

### Debian
- Ext4 optimization
- Advanced quota management
- Compression settings
