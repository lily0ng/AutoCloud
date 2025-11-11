#!/bin/bash

# Cloud Provider Detection
detect_cloud_provider() {
    if curl -s http://169.254.169.254/latest/meta-data/ &> /dev/null; then
        echo "aws"
    elif curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/ &> /dev/null; then
        echo "gcp"
    elif curl -s -H "Metadata:true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" &> /dev/null; then
        echo "azure"
    else
        echo "unknown"
    fi
}

# Install Common Dependencies
install_common_deps() {
    if [ -f /etc/debian_version ]; then
        apt-get update
        apt-get install -y curl wget unzip jq python3 python3-pip
    elif [ -f /etc/redhat-release ]; then
        yum update -y
        yum install -y curl wget unzip jq python3 python3-pip
    fi
    
    pip3 install boto3 google-cloud-monitoring azure-monitor-ingestion
}

# Setup AWS CloudWatch Agent
setup_aws() {
    wget https://s3.amazonaws.com/amazoncloudwatch-agent/linux/amd64/latest/amazon-cloudwatch-agent.rpm
    rpm -U ./amazon-cloudwatch-agent.rpm
    cp ../configs/aws/cloudwatch-agent.json /opt/aws/amazon-cloudwatch-agent/etc/
    /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-agent.json
}

# Setup Google Cloud Operations Agent
setup_gcp() {
    curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
    bash add-google-cloud-ops-agent-repo.sh --also-install
    cp ../configs/gcp/monitoring-config.yaml /etc/google-cloud-ops-agent/config.yaml
    systemctl restart google-cloud-ops-agent
}

# Setup Azure Monitor Agent
setup_azure() {
    wget https://raw.githubusercontent.com/Microsoft/OMS-Agent-for-Linux/master/installer/scripts/onboard_agent.sh
    chmod +x onboard_agent.sh
    ./onboard_agent.sh -w $WORKSPACE_ID -s $WORKSPACE_KEY
    cp ../configs/azure/monitoring-config.json /etc/opt/microsoft/azuremonitoragent/config.json
    systemctl restart azuremonitoragent
}

# Main Setup
CLOUD_PROVIDER=$(detect_cloud_provider)
install_common_deps

case $CLOUD_PROVIDER in
    "aws")
        setup_aws
        ;;
    "gcp")
        setup_gcp
        ;;
    "azure")
        setup_azure
        ;;
    *)
        echo "Unknown cloud provider or running on-premises"
        exit 1
        ;;
esac

echo "Monitoring agent setup complete for $CLOUD_PROVIDER"
