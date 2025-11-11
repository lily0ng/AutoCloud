#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Log Management Automation Framework Installation${NC}"
echo "================================================"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
echo -e "${YELLOW}Detected Python version: ${python_version}${NC}"

# Create virtual environment
echo -e "\n${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "\n${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip

# Install OS-specific dependencies
os_name=$(uname -s)
echo -e "\n${GREEN}Installing OS-specific dependencies for ${os_name}...${NC}"

case "$os_name" in
    "Linux")
        # Install Linux dependencies
        sudo apt-get update
        sudo apt-get install -y \
            build-essential \
            python3-dev \
            libssl-dev \
            libffi-dev \
            libxml2-dev \
            libxslt1-dev \
            zlib1g-dev \
            libjpeg-dev \
            libpq-dev \
            libsystemd-dev
        ;;
    "Darwin")
        # Install macOS dependencies
        brew install openssl
        brew install libffi
        brew install xz
        ;;
    "FreeBSD")
        # Install FreeBSD dependencies
        pkg install -y \
            python3 \
            py39-pip \
            gcc \
            openssl \
            libffi
        ;;
    "SunOS")
        # Install Solaris dependencies
        pkg install -y \
            developer/gcc \
            security/openssl \
            library/libffi
        ;;
    *)
        echo -e "${RED}Unsupported operating system${NC}"
        exit 1
        ;;
esac

# Install Python packages
echo -e "\n${GREEN}Installing Python packages...${NC}"
pip install -r requirements.txt

# Install network device SDK dependencies
echo -e "\n${GREEN}Installing network device SDKs...${NC}"

# Cisco
echo "Installing Cisco SDK..."
pip install ansible-pylibssh

# Palo Alto
echo "Installing Palo Alto SDK..."
pip install pan-os-python

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Installation completed successfully!${NC}"
    echo -e "\nTo activate the virtual environment, run:"
    echo -e "${YELLOW}source venv/bin/activate${NC}"
else
    echo -e "\n${RED}Installation failed. Please check the error messages above.${NC}"
    exit 1
fi

# Create .env file template
echo -e "\n${GREEN}Creating .env file template...${NC}"
cat > .env.template << EOL
# AWS Credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Slack Credentials
SLACK_BOT_TOKEN=

# Network Device Credentials
CISCO_PASSWORD=
CISCO_ENABLE=
PALOALTO_PASSWORD=
FORTIGATE_PASSWORD=
F5_PASSWORD=
CHECKPOINT_PASSWORD=
ARISTA_PASSWORD=
JUNIPER_PASSWORD=
HUAWEI_PASSWORD=
MIKROTIK_PASSWORD=
VMWARE_PASSWORD=

# OS Credentials
WIN_PASSWORD=
LINUX_PASSWORD=
MAC_PASSWORD=
BSD_PASSWORD=
SOLARIS_PASSWORD=

# Encryption
ENCRYPTION_KEY=

# API Settings
API_PORT=5000
PROMETHEUS_PORT=8000
EOL

echo -e "\n${GREEN}Installation complete! Please configure your .env file using the .env.template${NC}"
