#!/bin/sh
# Substitute BACKEND_HOST and BACKEND_PORT into nginx config at container start.
# Defaults work for local Docker Compose; Azure overrides via environment variables.

BACKEND_HOST="${BACKEND_HOST:-backend}"
BACKEND_PORT="${BACKEND_PORT:-8000}"

export BACKEND_HOST BACKEND_PORT

envsubst '${BACKEND_HOST} ${BACKEND_PORT}' \
  < /etc/nginx/templates/nginx.template.conf \
  > /etc/nginx/conf.d/default.conf

echo "[entrypoint] Backend proxy → http://${BACKEND_HOST}:${BACKEND_PORT}"

exec nginx -g 'daemon off;'
