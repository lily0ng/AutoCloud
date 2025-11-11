# Alpine Minimal Server
FROM alpine:3.18

# Install basic utilities
RUN apk update && apk add --no-cache \
    nginx \
    curl \
    bash \
    supervisor

# Configure nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Create directory for nginx
RUN mkdir -p /run/nginx

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
