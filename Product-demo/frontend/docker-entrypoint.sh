#!/bin/sh
# Copy nginx config and start server.
# BACKEND_URL is hardcoded in nginx.template.conf for Azure deployment.

cp /etc/nginx/templates/nginx.template.conf /etc/nginx/conf.d/default.conf

echo "[entrypoint] Starting nginx with hardcoded backend URL"

exec nginx -g 'daemon off;'
