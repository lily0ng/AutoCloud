.PHONY: build up down logs clean test help

COMPOSE_FILE := docker/docker-compose.yml
COMPOSE_DEV := docker/docker-compose.dev.yml
COMPOSE_PROD := docker/docker-compose.prod.yml
COMPOSE_TEST := docker/docker-compose.test.yml

help:
	@echo "Available targets:"
	@echo "  build       - Build all Docker images"
	@echo "  up          - Start all services"
	@echo "  down        - Stop all services"
	@echo "  logs        - View logs"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean Docker resources"
	@echo "  dev         - Start development environment"
	@echo "  prod        - Start production environment"
	@echo "  stats       - Show container statistics"
	@echo "  health      - Check container health"

build:
	@echo "Building Docker images..."
	./docker/scripts/build-all.sh

up:
	@echo "Starting services..."
	docker-compose -f $(COMPOSE_FILE) up -d

down:
	@echo "Stopping services..."
	docker-compose -f $(COMPOSE_FILE) down

logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

test:
	@echo "Running tests..."
	docker-compose -f $(COMPOSE_TEST) up --abort-on-container-exit

clean:
	@echo "Cleaning Docker resources..."
	./docker/scripts/clean.sh

dev:
	@echo "Starting development environment..."
	docker-compose -f $(COMPOSE_DEV) up -d

prod:
	@echo "Starting production environment..."
	docker-compose -f $(COMPOSE_PROD) up -d

stats:
	./docker/utils/docker-stats.sh

health:
	./docker/scripts/health-check.sh

backup:
	./docker/scripts/backup.sh

restore:
	./docker/scripts/restore.sh

scale:
	@read -p "Service name: " service; \
	read -p "Number of replicas: " replicas; \
	./docker/scripts/scale.sh $$service $$replicas
