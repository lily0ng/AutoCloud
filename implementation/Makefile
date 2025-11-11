.PHONY: build test clean deploy help

PROJECT_NAME := autocloud
VERSION := $(shell git describe --tags --always --dirty)
BUILD_DIR := build

help:
	@echo "Available targets:"
	@echo "  build       - Build all services"
	@echo "  test        - Run all tests"
	@echo "  clean       - Clean build artifacts"
	@echo "  deploy      - Deploy to Kubernetes"
	@echo "  docker      - Build Docker images"
	@echo "  lint        - Run linters"
	@echo "  setup       - Setup development environment"

build:
	@echo "Building services..."
	@mkdir -p $(BUILD_DIR)
	cd services/service-a && go build -o ../../$(BUILD_DIR)/service-a
	cd services/service-b && go build -o ../../$(BUILD_DIR)/service-b
	cd services/service-c && go build -o ../../$(BUILD_DIR)/service-c
	gcc security/encryption/encryption.c -o $(BUILD_DIR)/encryption -lcrypto -lssl
	gcc security/firewall/firewall.c -o $(BUILD_DIR)/firewall
	@echo "Build complete!"

test:
	@echo "Running tests..."
	go test ./... -v -cover
	python3 -m pytest tests/ -v
	@echo "Tests complete!"

clean:
	@echo "Cleaning..."
	rm -rf $(BUILD_DIR)
	rm -rf coverage.*
	find . -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

docker:
	@echo "Building Docker images..."
	docker build -t $(PROJECT_NAME)/service-a:$(VERSION) services/service-a
	docker build -t $(PROJECT_NAME)/service-b:$(VERSION) services/service-b
	docker build -t $(PROJECT_NAME)/service-c:$(VERSION) services/service-c
	@echo "Docker images built!"

deploy:
	@echo "Deploying to Kubernetes..."
	./cicd/deploy/deploy.sh production $(VERSION)
	@echo "Deployment complete!"

lint:
	@echo "Running linters..."
	golangci-lint run
	pylint **/*.py
	@echo "Linting complete!"

setup:
	@echo "Setting up development environment..."
	./scripts/setup.sh
	@echo "Setup complete!"

run-local:
	@echo "Starting services locally..."
	docker-compose -f infrastructure/docker/docker-compose.yml up -d
	@echo "Services started!"

stop-local:
	@echo "Stopping services..."
	docker-compose -f infrastructure/docker/docker-compose.yml down
	@echo "Services stopped!"
