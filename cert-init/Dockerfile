FROM nginx:alpine

# Install certbot and its nginx plugin
RUN apk add --no-cache certbot certbot-nginx

# Copy nginx configuration for ACME challenge
COPY nginx.conf /etc/nginx/nginx.conf

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
