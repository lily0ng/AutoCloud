# Kubernetes Persistent Volume Management Tools

This repository contains tools for managing Kubernetes Persistent Volumes (PV) and Persistent Volume Claims (PVC).

## Files Overview

- `pv-config.yaml`: Basic PV and PVC configuration templates
- `pv-automation.sh`: Bash script for basic PV operations
- `pv_manager.py`: Advanced Python script for PV management
- `requirements.txt`: Python dependencies

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make the scripts executable:
```bash
chmod +x pv-automation.sh
chmod +x pv_manager.py
```

## Using the Tools

### Bash Script (pv-automation.sh)
Run the script and follow the interactive menu:
```bash
./pv-automation.sh
```

Features:
- Create PV and PVC from YAML
- List all PVs and PVCs
- Delete PV
- Check PV status
- Create storage directory

### Python Script (pv_manager.py)
Run the Python script for advanced management:
```bash
./pv_manager.py
```

Features:
- Create PV/PVC from YAML
- List all PVs and PVCs with detailed information
- Delete PV
- Get detailed PV status
- Error handling and logging

### Configuration (pv-config.yaml)
Contains template configurations for:
- PersistentVolume (10Gi capacity)
- PersistentVolumeClaim (5Gi request)

## Notes

- Ensure you have kubectl configured correctly
- The default storage path is `/mnt/data`
- Default storage class is set to "manual"
- Make sure you have the necessary permissions to create/delete PVs
