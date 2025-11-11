# Kubernetes Persistent Volumes Setup

This directory contains configuration files and automation scripts for setting up Persistent Volumes in Kubernetes.

## Contents

- `pv-config.yaml`: Basic PV configurations
- `pvc-config.yaml`: Persistent Volume Claims configurations
- `storage-class.yaml`: Storage Class definitions
- `setup-pv.sh`: Automation script for PV setup
- `cleanup-pv.sh`: Cleanup script for PV resources

## Usage

1. Edit the configuration files as needed
2. Make the scripts executable:
   ```bash
   chmod +x setup-pv.sh cleanup-pv.sh
   ```
3. Run the setup script:
   ```bash
   ./setup-pv.sh
   ```

## Configuration

Modify the YAML files according to your storage requirements:
- Storage size
- Access modes
- Storage class
- Volume types
