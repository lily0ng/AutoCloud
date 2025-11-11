#!/bin/bash

# VM Setup Script
set -e

# Load configurations
CONFIG_DIR="../config"
VM_CONFIG="$CONFIG_DIR/vm_config.yaml"
NETWORK_CONFIG="$CONFIG_DIR/network_config.yaml"

# Check if configuration files exist
if [ ! -f "$VM_CONFIG" ] || [ ! -f "$NETWORK_CONFIG" ]; then
    echo "Error: Configuration files not found!"
    exit 1
fi

# Function to create VM
create_vm() {
    local name=$1
    local role=$2
    
    echo "Creating VM: $name ($role)"
    
    # Create VM using VirtualBox
    VBoxManage createvm --name "$name" --ostype Ubuntu_64 --register
    
    # Configure VM resources
    VBoxManage modifyvm "$name" --cpus 2 --memory 4096 --acpi on --boot1 dvd
    
    # Create and attach virtual hard disk
    VBoxManage createhd --filename "$name.vdi" --size 50000
    VBoxManage storagectl "$name" --name "SATA Controller" --add sata --controller IntelAhci
    VBoxManage storageattach "$name" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$name.vdi"
    
    # Configure networking
    VBoxManage modifyvm "$name" --nic1 bridged --bridgeadapter1 eth0
    
    echo "VM $name created successfully"
}

# Function to configure networking
setup_network() {
    local name=$1
    local role=$2
    
    echo "Configuring network for VM: $name"
    
    # Configure network based on role
    case $role in
        "web")
            VBoxManage modifyvm "$name" --nic2 intnet --intnet2 "web_tier"
            ;;
        "database")
            VBoxManage modifyvm "$name" --nic2 intnet --intnet2 "db_tier"
            ;;
        "cache")
            VBoxManage modifyvm "$name" --nic2 intnet --intnet2 "cache_tier"
            ;;
    esac
    
    echo "Network configuration completed for $name"
}

# Main setup process
echo "Starting VM setup process..."

# Create and configure web server
create_vm "web-server" "web"
setup_network "web-server" "web"

# Create and configure database server
create_vm "db-server" "database"
setup_network "db-server" "database"

# Create and configure cache server
create_vm "cache-server" "cache"
setup_network "cache-server" "cache"

echo "VM setup completed successfully!"
