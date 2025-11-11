# Use Ubuntu as the base image
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set maintainer label
LABEL maintainer="Infrastructure Team"
LABEL version="1.0"
LABEL description="Infrastructure automation and configuration container"

# Set working directory
WORKDIR /app

# Install essential packages and tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    git \
    vim \
    unzip \
    jq \
    ansible \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages for automation
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy installation and configuration scripts
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.sh

# Set environment variables
ENV PATH="/app/scripts:${PATH}"

# Create volume for persistent data
VOLUME ["/app/data"]

# Default command
CMD ["/bin/bash"]
