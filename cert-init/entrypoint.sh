#!/bin/sh

set -e

DOMAIN=${DOMAIN_NAME:-}
EMAIL=${CERTBOT_EMAIL:-}

if [ -z "$DOMAIN" ] || [ "$DOMAIN" = "localhost" ]; then
  echo "No domain specified, skipping certificate generation"
  exit 0
fi

if [ -z "$EMAIL" ]; then
  echo "Error: CERTBOT_EMAIL environment variable is required"
  exit 1
fi

# Function to check if certificate exists
check_cert_exists() {
  certbot certificates | grep -q "Domains: $DOMAIN"
  return $?
}

# Function to obtain new certificate
obtain_certificate() {
  echo "Obtaining new certificate for domain: $DOMAIN"
  certbot certonly \
    --webroot \
    --webroot-path=/var/www/html \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    --non-interactive \
    --keep-until-expiring \
    --reuse-key \
    -d "$DOMAIN"
}

# Start nginx in the background
echo "Starting nginx..."
nginx

# Initial certificate generation
if ! check_cert_exists; then
  obtain_certificate
  echo "✅ Initial certificate obtained"
else
  echo "✅ Certificate already exists for $DOMAIN"
fi

# Stop nginx
echo "Stopping nginx..."
nginx -s quit

# Exit successfully
echo "Certificate initialization complete, exiting..."
exit 0

