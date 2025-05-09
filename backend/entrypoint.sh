#!/bin/bash

# Make sure this file is executable:
# chmod +x backend/entrypoint.sh

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done


# Run migrations
flask db upgrade

# Start Gunicorn server
exec gunicorn -w 4 -b 0.0.0.0:5000 run:app
