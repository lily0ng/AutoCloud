# Custom Grafana Dockerfile
FROM grafana/grafana:latest

USER root

# Install plugins
RUN grafana-cli plugins install grafana-piechart-panel && \
    grafana-cli plugins install grafana-clock-panel

# Copy provisioning files
COPY docker/grafana/provisioning/ /etc/grafana/provisioning/
COPY docker/grafana/dashboards/ /var/lib/grafana/dashboards/

# Set permissions
RUN chown -R grafana:grafana /etc/grafana /var/lib/grafana

USER grafana

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --spider http://localhost:3000/api/health || exit 1
