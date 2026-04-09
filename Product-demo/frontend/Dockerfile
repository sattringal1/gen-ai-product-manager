# ── Build stage ──────────────────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app
COPY package.json ./
RUN npm install --silent
COPY . .
RUN npm run build

# ── Production stage ─────────────────────────────────────────────
FROM nginx:1.27-alpine AS production

# Copy built React app
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx template (envsubst fills BACKEND_HOST / BACKEND_PORT at runtime)
COPY nginx.template.conf /etc/nginx/templates/nginx.template.conf

# Copy entrypoint that runs envsubst then starts nginx
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost/health || exit 1

ENTRYPOINT ["/docker-entrypoint.sh"]
