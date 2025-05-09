#!/bin/bash

# Rebuild and start all containers
echo "...Rebuilding & starting containers..."
docker-compose down
docker-compose up -d --build
