#!/bin/bash

# CentOS Setup Script for Logging and Monitoring Infrastructure
set -e

echo "Starting logging and monitoring setup for CentOS..."

# Update system
yum update -y
yum install -y epel-release

# Install dependencies
yum install -y \
    wget \
    curl \
    python3 \
    python3-pip \
    tar \
    gzip \
    vim

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
rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch
cat > /etc/yum.repos.d/elastic.repo << EOF
[elastic-8.x]
name=Elastic repository for 8.x packages
baseurl=https://artifacts.elastic.co/packages/8.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

yum install -y filebeat

# Start services
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter
systemctl enable prometheus
systemctl start prometheus
systemctl enable filebeat
systemctl start filebeat

echo "Setup completed successfully!"
