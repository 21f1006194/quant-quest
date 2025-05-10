#!/bin/sh

set -e

DOMAIN=${DOMAIN_NAME:-}

# Case: Use self-signed if empty or localhost
if [ -z "$DOMAIN" ] || [ "$DOMAIN" = "localhost" ]; then
  echo "Generating self-signed certificate for localhost..."

  mkdir -p /etc/selfsigned

  openssl req -x509 -nodes -days 365 \
    -subj "/CN=localhost" \
    -newkey rsa:2048 \
    -keyout /etc/selfsigned/localhost.key \
    -out /etc/selfsigned/localhost.crt

  echo "✅ Self-signed cert generated."

else
  echo "Running Certbot for domain: $DOMAIN"

  certbot certonly \
    --webroot \
    --webroot-path=/var/www/html \
    --email "$CERTBOT_EMAIL" \
    --agree-tos \
    --no-eff-email \
    --non-interactive \
    --keep-until-expiring \
    --reuse-key \
    -d "$DOMAIN"

  echo "✅ Certbot certificate obtained."
fi
