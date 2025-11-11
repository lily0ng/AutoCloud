# Custom Prometheus Dockerfile
FROM prom/prometheus:latest

# Copy configuration
COPY docker/prometheus/prometheus.yml /etc/prometheus/prometheus.yml
COPY docker/prometheus/alerts/ /etc/prometheus/alerts/

# Create data directory
USER root
RUN mkdir -p /prometheus && \
    chown -R nobody:nobody /prometheus /etc/prometheus

USER nobody

EXPOSE 9090

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --spider http://localhost:9090/-/healthy || exit 1

CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.console.libraries=/usr/share/prometheus/console_libraries", \
     "--web.console.templates=/usr/share/prometheus/consoles"]
