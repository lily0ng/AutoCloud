#!/bin/bash
# User Management Automation Script

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}👥 User Management System${NC}"

function create_user() {
    local username=$1
    local groups=$2
    
    echo -e "${BLUE}Creating user: $username${NC}"
    
    if id "$username" &>/dev/null; then
        echo -e "${RED}User already exists${NC}"
        return 1
    fi
    
    useradd -m -s /bin/bash "$username"
    
    if [ -n "$groups" ]; then
        usermod -aG "$groups" "$username"
    fi
    
    echo -e "${GREEN}✅ User created successfully${NC}"
}

function delete_user() {
    local username=$1
    
    echo -e "${BLUE}Deleting user: $username${NC}"
    userdel -r "$username"
    echo -e "${GREEN}✅ User deleted${NC}"
}

function list_users() {
    echo -e "${BLUE}System Users:${NC}"
    awk -F: '$3 >= 1000 {print $1}' /etc/passwd
}

function reset_password() {
    local username=$1
    echo -e "${BLUE}Resetting password for: $username${NC}"
    passwd "$username"
}

case "${1:-list}" in
    create)
        create_user "$2" "$3"
        ;;
    delete)
        delete_user "$2"
        ;;
    list)
        list_users
        ;;
    reset-password)
        reset_password "$2"
        ;;
    *)
        echo "Usage: $0 {create|delete|list|reset-password} [username] [groups]"
        exit 1
        ;;
esac
