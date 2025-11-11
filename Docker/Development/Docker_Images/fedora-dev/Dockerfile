# Fedora Development Environment
FROM fedora:37

# Install development tools and utilities
RUN dnf -y update && dnf -y install \
    gcc \
    gcc-c++ \
    make \
    git \
    nodejs \
    python3 \
    python3-pip \
    vim \
    wget \
    && dnf clean all

# Set up development environment
RUN mkdir -p /opt/workspace

# Set working directory
WORKDIR /opt/workspace

# Environment variables
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Default command
CMD ["/bin/bash"]
