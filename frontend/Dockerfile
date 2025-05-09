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
COPY nginx.conf /etc/nginx/nginx.conf
