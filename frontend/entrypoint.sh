#!/bin/sh

set -e

DOMAIN=${DOMAIN_NAME:-localhost}
CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/$DOMAIN/privkey.pem"

# Function to check if SSL certificates exist
check_ssl_certs() {
  [ -f "$CERT_PATH" ] && [ -f "$KEY_PATH" ]
  return $?
}

# Function to generate nginx config
generate_nginx_config() {
  if check_ssl_certs; then
    echo "SSL certificates found, configuring HTTPS..."
    export SSL_CERT_PATH="$CERT_PATH"
    export SSL_KEY_PATH="$KEY_PATH"
    envsubst '${DOMAIN_NAME} ${SSL_CERT_PATH} ${SSL_KEY_PATH}' < /etc/nginx/nginx.conf.ssl.template > /etc/nginx/nginx.conf
  else
    echo "No SSL certificates found, configuring HTTP only..."
    envsubst '${DOMAIN_NAME}' < /etc/nginx/nginx.conf.nonssl.template > /etc/nginx/nginx.conf
  fi
}

# Initial configuration
generate_nginx_config

# Start nginx
echo "Starting nginx..."
nginx -g 'daemon off;' 