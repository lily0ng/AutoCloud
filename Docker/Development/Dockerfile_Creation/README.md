# Dockerfile Best Practices Guide

This guide explains the best practices implemented in our Dockerfile.

## Key Features

1. **Multi-stage Build**
   - Reduces final image size
   - Separates build dependencies from runtime dependencies
   - Only necessary artifacts are copied to the final image

2. **Security Best Practices**
   - Uses non-root user
   - Implements health checks
   - Minimal base image (Alpine-based)
   - Proper permission management

3. **Optimization Techniques**
   - Layer caching
   - Proper ordering of commands
   - Minimal number of layers
   - Production-only dependencies in final image

## Dockerfile Breakdown

### Build Stage
```dockerfile
FROM node:18-alpine AS builder
```
- Uses lightweight Alpine-based Node.js image
- Named stage for multi-stage build

### Working Directory
```dockerfile
WORKDIR /app
```
- Sets consistent working directory
- Prevents path confusion

### Dependency Management
```dockerfile
COPY package*.json ./
RUN npm ci
```
- Copies package files first to leverage layer caching
- Uses `npm ci` for reproducible builds

### Production Stage
```dockerfile
FROM node:18-alpine
```
- Fresh start with minimal base image

### Security
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```
- Creates non-root user
- Switches to non-root user for security

### Environment Configuration
```dockerfile
ENV NODE_ENV=production \
    PORT=3000
```
- Clear environment variable definition
- Runtime configuration

## CLI Usage Instructions

### Dockerfile CLI Generator

A command-line tool to generate and validate Dockerfiles interactively.

#### Features

- Interactive Dockerfile generation
- Support for multiple programming languages (Python, Node.js, Go, Java)
- Dockerfile validation
- Customizable port exposure and commands
- Best practices implementation

#### Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Make the script executable:
```bash
chmod +x dockerfile_cli.py
```

#### Usage

##### Generate a new Dockerfile

```bash
./dockerfile_cli.py create
```

This will start an interactive prompt asking for:
- Application type (python/node/golang/java)
- Base image selection
- Port to expose
- Command to run

You can also use command-line options:
```bash
./dockerfile_cli.py create --type python --port 8000 --cmd "python app.py"
```

##### Validate an existing Dockerfile

```bash
./dockerfile_cli.py validate Dockerfile
```

#### Supported Base Images

##### Python
- python:3.9
- python:3.8-slim
- python:3.9-alpine

##### Node.js
- node:16
- node:16-alpine
- node:14-slim

##### Go
- golang:1.17
- golang:1.17-alpine

##### Java
- openjdk:11
- openjdk:11-slim
- openjdk:8

## Example Generated Dockerfile

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
```

## Usage

1. Build the image:
   ```bash
   docker build -t myapp .
   ```

2. Run the container:
   ```bash
   docker run -p 3000:3000 myapp
   ```

## Best Practices Implemented

1. **Layer Optimization**
   - Combines RUN commands where logical
   - Orders commands from least to most frequently changing

2. **Security**
   - Non-root user
   - Minimal base image
   - Production-only dependencies

3. **Maintainability**
   - Clear documentation
   - Consistent formatting
   - Logical stage separation

4. **Reliability**
   - Health checks
   - Explicit versions
   - Reproducible builds
