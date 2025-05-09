#!/bin/bash

# Get the absolute path of the project directory
dirname=$( realpath $(dirname $0)/.. )
cd $dirname

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

# Run custom logic to apply migrations and insert default data (like games, admin user, etc.)
echo "Running database initialization..."
python3 scripts/init_db.py

# Start the Gunicorn server with Gevent workers
exec gunicorn -w 4 -k gevent -b 0.0.0.0:5000 wsgi:app
