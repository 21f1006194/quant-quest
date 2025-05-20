#!/bin/bash
set -e

DEV_COMPOSE_FILE="docker-compose.dev.yml"
PROD_COMPOSE_FILE="docker-compose.yml"
PROD_ENV_FILE=".env.prod"
DEV_ENV_FILE=".env.dev"

case "$1" in
  dev)
    shift
    echo "👉 Using dev compose file..."
    docker compose -f $DEV_COMPOSE_FILE --env-file $DEV_ENV_FILE "$@"
    ;;

  prod)
    shift
    echo "👉 Using production compose file..."
    docker compose -f $PROD_COMPOSE_FILE --env-file $PROD_ENV_FILE "$@"
    ;;

  *)
    echo "❌ Unknown command: $1"
    echo ""
    echo "Usage:"
    echo "  ./compose.sh dev up -d --build        # Start dev in detached mode"
    echo "  ./compose.sh dev down                 # Stop dev"
    echo "  ./compose.sh prod up -d --build       # Start prod in detached mode"
    echo "  ./compose.sh prod down                # Stop prod"
    echo "  ./compose.sh dev build               # Build dev containers"
    echo "  ./compose.sh prod build               # Build prod containers"
    exit 1
    ;;
esac
