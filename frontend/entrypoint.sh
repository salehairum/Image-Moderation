#!/bin/sh

# Export all environment variables for envsubst
export $(env | cut -d= -f1)

# Replace placeholders
envsubst '${API_BASE_URL}' < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js

# Start Nginx
nginx -g 'daemon off;'
