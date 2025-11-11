#!/bin/bash
# Create Kafka Topics

set -e

KAFKA_BROKER=${KAFKA_BROKER:-localhost:9092}

echo "Waiting for Kafka to be ready..."
sleep 10

echo "Creating topics..."

kafka-topics --create \
  --bootstrap-server $KAFKA_BROKER \
  --topic events \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

kafka-topics --create \
  --bootstrap-server $KAFKA_BROKER \
  --topic logs \
  --partitions 5 \
  --replication-factor 1 \
  --if-not-exists

kafka-topics --create \
  --bootstrap-server $KAFKA_BROKER \
  --topic transactions \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "Topics created successfully"

kafka-topics --list --bootstrap-server $KAFKA_BROKER
