# Custom Kafka Dockerfile
FROM confluentinc/cp-kafka:latest

USER root

# Install additional tools
RUN yum install -y \
    curl \
    netcat \
    && yum clean all

# Copy custom scripts
COPY docker/kafka/scripts/ /usr/local/bin/

RUN chmod +x /usr/local/bin/*.sh

USER appuser

EXPOSE 9092 9093

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD kafka-broker-api-versions --bootstrap-server localhost:9092 || exit 1
