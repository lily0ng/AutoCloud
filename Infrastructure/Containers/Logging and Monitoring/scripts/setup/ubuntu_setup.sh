#!/bin/bash

# Ubuntu Setup Script for Logging and Monitoring Infrastructure
set -e

echo "Starting logging and monitoring setup for Ubuntu..."

# Update system
apt-get update
apt-get upgrade -y

# Install dependencies
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    python3 \
    python3-pip \
    wget \
    gnupg2

# Install Node Exporter
NODE_EXPORTER_VERSION="1.7.0"
wget https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
tar xvfz node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz
mv node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter /usr/local/bin/
rm -rf node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64*

# Create Node Exporter service
cat > /etc/systemd/system/node_exporter.service << EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
Type=simple
User=node_exporter
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# Create node_exporter user
useradd -rs /bin/false node_exporter

# Install Prometheus
PROMETHEUS_VERSION="2.45.0"
wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
tar xvfz prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
mv prometheus-${PROMETHEUS_VERSION}.linux-amd64/prometheus /usr/local/bin/
mv prometheus-${PROMETHEUS_VERSION}.linux-amd64/promtool /usr/local/bin/
rm -rf prometheus-${PROMETHEUS_VERSION}.linux-amd64*

# Create Prometheus directories
mkdir -p /etc/prometheus /var/lib/prometheus

# Install Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.11.1-amd64.deb
dpkg -i filebeat-8.11.1-amd64.deb
rm filebeat-8.11.1-amd64.deb

# Start services
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter
systemctl enable prometheus
systemctl start prometheus
systemctl enable filebeat
systemctl start filebeat

echo "Setup completed successfully!"
