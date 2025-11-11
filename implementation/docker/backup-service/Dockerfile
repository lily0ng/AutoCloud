# Backup Service Dockerfile
FROM alpine:latest

RUN apk add --no-cache \
    bash \
    postgresql-client \
    redis \
    aws-cli \
    curl

COPY docker/backup-service/backup-script.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/backup-script.sh

CMD ["/usr/local/bin/backup-script.sh"]
