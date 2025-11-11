# Custom Redis Dockerfile
FROM redis:7-alpine

# Install additional tools
RUN apk add --no-cache \
    bash \
    curl

# Copy custom configuration
COPY docker/redis/redis.conf /usr/local/etc/redis/redis.conf

# Create data directory
RUN mkdir -p /data && \
    chown redis:redis /data

EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD redis-cli ping || exit 1

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
