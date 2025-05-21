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
ARG VITE_GOOGLE_CLIENT_ID
RUN echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" > .env
RUN echo "VITE_GOOGLE_CLIENT_ID=${VITE_GOOGLE_CLIENT_ID}" >> .env

# Build the application
RUN npm run build

# Production stage (use Nginx to serve the frontend)
FROM nginx:alpine

# Copy the built app into Nginx's default directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the custom Nginx configurations and entrypoint script
COPY nginx.conf.ssl.template /etc/nginx/nginx.conf.ssl.template
COPY nginx.conf.nonssl.template /etc/nginx/nginx.conf.nonssl.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directory for certbot webroot
RUN mkdir -p /var/www/html

ENTRYPOINT ["/entrypoint.sh"]
