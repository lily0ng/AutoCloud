# Event-Driven Architecture Project

This project demonstrates a modern event-driven architecture implementation using Python, with support for multiple message brokers and event patterns.

## Architecture Overview

The project follows these key architectural principles:
- Event Producer/Consumer Pattern
- Pub/Sub Messaging
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)
- Asynchronous Communication

## Components

1. Event Bus
2. Event Producers
3. Event Consumers
4. Event Store
5. Command Handlers
6. Query Handlers

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
```

3. Run the application:
```bash
python src/main.py
```

## Project Structure

```
src/
├── core/
│   ├── events/
│   ├── commands/
│   └── queries/
├── infrastructure/
│   ├── message_broker/
│   └── event_store/
├── domain/
│   ├── models/
│   └── services/
└── api/
    └── handlers/
```

## Event Flow

1. Events are produced by services
2. Events are published to the Event Bus
3. Event Bus routes events to appropriate consumers
4. Consumers process events and update the system state
5. Query handlers serve read requests from updated state
