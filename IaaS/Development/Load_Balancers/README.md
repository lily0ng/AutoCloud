# Load Balancer Configuration

This repository contains configuration files for load balancers across multiple cloud providers and Linux OS instances.

## Structure
- `terraform/` - Infrastructure as Code configurations
- `ansible/` - Automation playbooks for Linux configuration
- `configs/` - Load balancer configuration templates
- `scripts/` - Utility scripts

## Supported Platforms
- AWS Application Load Balancer
- Google Cloud Load Balancer
- Azure Load Balancer
- HAProxy
- NGINX

## Prerequisites
- Terraform >= 1.0
- Ansible >= 2.9
- Python >= 3.8
