# Custom PostgreSQL Dockerfile
FROM postgres:15-alpine

# Install additional extensions
RUN apk add --no-cache \
    postgresql-contrib \
    postgresql-dev

# Copy initialization scripts
COPY docker/postgres/init-scripts/ /docker-entrypoint-initdb.d/

# Copy custom configuration
COPY docker/postgres/postgresql.conf /etc/postgresql/postgresql.conf

# Set permissions
RUN chmod -R 755 /docker-entrypoint-initdb.d/

EXPOSE 5432

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD pg_isready -U ${POSTGRES_USER:-postgres} || exit 1

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
