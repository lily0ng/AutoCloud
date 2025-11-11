# Docker Orchestration Setup

This project demonstrates a complete Docker orchestration setup using Docker Compose, featuring multiple services working together.

## Services

- **WebApp**: Python Flask application
- **Database**: PostgreSQL database
- **Cache**: Redis cache
- **Monitoring**: Prometheus
- **Visualization**: Grafana

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone this repository
2. Navigate to the project directory
3. Run the following command:
   ```bash
   docker-compose up -d
   ```

## Service Access

- WebApp: http://localhost:8080
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Environment Variables

The services use the following environment variables:
- DB_HOST=db
- DB_USER=user
- DB_PASSWORD=password
- DB_NAME=appdb

## Monitoring

The application exports metrics at `/metrics` endpoint, which are scraped by Prometheus and can be visualized in Grafana.

## Volumes

Persistent data is stored in Docker volumes:
- webapp-data
- db-data
- redis-data
- prometheus-data
- grafana-data
