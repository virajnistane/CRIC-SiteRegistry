#!/bin/bash
# Configuration for Docker environment

# Copy this content to .env to use Docker:
cat > .env << 'EOF'
# Django settings
DEBUG=True
SECRET_KEY=django-insecure-fp#*z+)1scwfhq(jml+vy-o+z!7g&@)&%_dr0br0jov6!=4=@6qiq
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings (configured for DOCKER)
# These values work inside Docker containers
POSTGRES_NAME=site_registry
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
EOF

echo "✅ .env configured for Docker"
echo "Run: docker compose up"
