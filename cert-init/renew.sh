#!/bin/bash

# Load environment variables
if [ -f "../.env.prod" ]; then
  source ../.env.prod
fi

# Check if DOMAIN_NAME is set and not localhost
if [ -z "$DOMAIN_NAME" ] || [ "$DOMAIN_NAME" = "localhost" ]; then
  echo "No domain specified or localhost, skipping renewal"
  exit 0
fi

# Run the renewal service
echo "Starting certificate renewal..."
docker compose -f ../docker-compose.yml --env-file ../.env.prod --profile renewal up cert-renewal

# Wait for renewal to complete
docker compose -f ../docker-compose.yml --env-file ../.env.prod --profile renewal wait cert-renewal

# Clean up
docker compose -f ../docker-compose.yml --env-file ../.env.prod --profile renewal down 