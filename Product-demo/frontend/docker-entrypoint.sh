#!/bin/sh
# Inject BACKEND_URL into nginx config at container start.
# In Azure: BACKEND_URL = https://genai-pm-backend.<env>.azurecontainerapps.io
# Locally:  not set — React falls back to /api/v1 (Vite proxy)

BACKEND_URL="${BACKEND_URL:-}"

export BACKEND_URL

envsubst '${BACKEND_URL}' \
  < /etc/nginx/templates/nginx.template.conf \
  > /etc/nginx/conf.d/default.conf

echo "[entrypoint] BACKEND_URL = ${BACKEND_URL:-not set, using relative /api/v1}"

exec nginx -g 'daemon off;'
