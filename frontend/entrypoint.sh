#!/bin/sh

set -e

DOMAIN=${DOMAIN_NAME}
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
    export DOMAIN_NAME="$DOMAIN"
    export host='$host'
    export uri='$uri'
    export request_uri='$request_uri'
    export http_upgrade='$http_upgrade'
    envsubst < /etc/nginx/nginx.conf.ssl.template > /etc/nginx/nginx.conf
  else
    echo "No SSL certificates found, configuring HTTP only..."
    export DOMAIN_NAME="$DOMAIN"
    export host='$host'
    export uri='$uri'
    export request_uri='$request_uri'
    export http_upgrade='$http_upgrade'
    envsubst < /etc/nginx/nginx.conf.nonssl.template > /etc/nginx/nginx.conf
  fi
  echo "Nginx configuration generated"
  cat /etc/nginx/nginx.conf
}

# Initial configuration
generate_nginx_config

# Start nginx
echo "Starting nginx..."
nginx -g 'daemon off;' 