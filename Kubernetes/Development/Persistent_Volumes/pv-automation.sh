#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Function to create persistent volume
create_pv() {
    echo -e "${GREEN}Creating Persistent Volume...${NC}"
    kubectl apply -f pv-config.yaml
}

# Function to list all PVs
list_pvs() {
    echo -e "${GREEN}Listing all Persistent Volumes:${NC}"
    kubectl get pv
}

# Function to list all PVCs
list_pvcs() {
    echo -e "${GREEN}Listing all Persistent Volume Claims:${NC}"
    kubectl get pvc
}

# Function to delete PV
delete_pv() {
    if [ -z "$1" ]; then
        echo -e "${RED}Please provide PV name${NC}"
        return 1
    fi
    echo -e "${GREEN}Deleting Persistent Volume: $1${NC}"
    kubectl delete pv "$1"
}

# Function to check PV status
check_pv_status() {
    if [ -z "$1" ]; then
        echo -e "${RED}Please provide PV name${NC}"
        return 1
    fi
    echo -e "${GREEN}Checking status of PV: $1${NC}"
    kubectl describe pv "$1"
}

# Function to create storage directory
create_storage_dir() {
    echo -e "${GREEN}Creating storage directory...${NC}"
    sudo mkdir -p /mnt/data
    sudo chmod 777 /mnt/data
}

# Main menu
show_menu() {
    echo -e "\n${GREEN}Kubernetes PV Management Menu${NC}"
    echo "1. Create Persistent Volume and PVC"
    echo "2. List all PVs"
    echo "3. List all PVCs"
    echo "4. Delete PV"
    echo "5. Check PV Status"
    echo "6. Create Storage Directory"
    echo "7. Exit"
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-7): " choice

    case $choice in
        1) create_pv ;;
        2) list_pvs ;;
        3) list_pvcs ;;
        4) read -p "Enter PV name: " pv_name
           delete_pv "$pv_name" ;;
        5) read -p "Enter PV name: " pv_name
           check_pv_status "$pv_name" ;;
        6) create_storage_dir ;;
        7) echo "Exiting..."
           exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
done
