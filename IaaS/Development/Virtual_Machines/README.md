# Virtual Machine Automation Setup

This repository contains configuration and automation scripts for managing Virtual Machines with networking services.

## Directory Structure
```
Virtual_Machines/
├── config/
│   ├── vm_config.yaml
│   └── network_config.yaml
├── scripts/
│   ├── vm_setup.sh
│   └── network_setup.sh
└── README.md
```

## Prerequisites
- Virtualization software (VirtualBox/KVM/VMware)
- Python 3.8+
- YAML support
- Network management tools

## Quick Start
1. Configure VM settings in `config/vm_config.yaml`
2. Configure network settings in `config/network_config.yaml`
3. Run setup script: `./scripts/vm_setup.sh`

## Configuration Guide
Refer to individual configuration files for detailed settings:
- VM Configuration: See `config/vm_config.yaml`
- Network Configuration: See `config/network_config.yaml`
