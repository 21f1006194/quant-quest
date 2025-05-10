# frontend/Dockerfile

# Build stage
FROM node:20 AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the source code
COPY . .

# Create .env file with the API base URL from build arg
ARG VITE_API_BASE_URL
RUN echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" > .env

# Build the application
RUN npm run build

# Production stage (use Nginx to serve the frontend)
FROM nginx:alpine

# Copy the built app into Nginx's default directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf.template /etc/nginx/nginx.conf.template


# Set defaults for localhost cert paths
ARG DOMAIN_NAME
ENV SSL_CERT_PATH="/etc/selfsigned/localhost.crt"
ENV SSL_KEY_PATH="/etc/selfsigned/localhost.key"

# If DOMAIN_NAME is a real domain, point to Let's Encrypt paths
RUN if [ "$DOMAIN_NAME" != "localhost" ] && [ -n "$DOMAIN_NAME" ]; then \
    export SSL_CERT_PATH="/etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem" && \
    export SSL_KEY_PATH="/etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem"; \
    fi && \
    envsubst '${DOMAIN_NAME} ${SSL_CERT_PATH} ${SSL_KEY_PATH}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
