#!/bin/bash

# Make sure this file is executable:
# chmod +x backend/entrypoint.sh

# Wait for DB to be ready
until nc -z -v -w30 db 5432; do
  echo "Waiting for PostgreSQL to start..."
  sleep 1
done

# Run migrations
flask db upgrade

# Start Gunicorn server
exec gunicorn -w 4 -b 0.0.0.0:5000 run:app
