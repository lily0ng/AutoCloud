#!/bin/bash
# SSL Certificate Manager

set -e

CERT_DIR="/etc/ssl/certs"
KEY_DIR="/etc/ssl/private"

install_certbot() {
    if ! command -v certbot &> /dev/null; then
        apt-get update
        apt-get install -y certbot python3-certbot-nginx
    fi
}

generate_self_signed() {
    local domain=$1
    
    echo "Generating self-signed certificate for $domain..."
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$KEY_DIR/$domain.key" \
        -out "$CERT_DIR/$domain.crt" \
        -subj "/CN=$domain"
    
    echo "✅ Self-signed certificate created"
}

request_letsencrypt() {
    local domain=$1
    local email=$2
    
    install_certbot
    
    echo "Requesting Let's Encrypt certificate for $domain..."
    
    certbot certonly --nginx \
        -d "$domain" \
        --email "$email" \
        --agree-tos \
        --non-interactive
    
    echo "✅ Let's Encrypt certificate obtained"
}

renew_certificates() {
    echo "Renewing certificates..."
    certbot renew --quiet
    echo "✅ Certificates renewed"
}

list_certificates() {
    echo "Installed certificates:"
    certbot certificates
}

case "${1:-list}" in
    self-signed)
        generate_self_signed "$2"
        ;;
    letsencrypt)
        request_letsencrypt "$2" "$3"
        ;;
    renew)
        renew_certificates
        ;;
    list)
        list_certificates
        ;;
esac
