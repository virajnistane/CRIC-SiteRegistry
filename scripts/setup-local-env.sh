#!/bin/bash
# Configuration for local development environment

# Copy this content to .env to use local development:
cat > .env << 'EOF'
# Django settings
DEBUG=True
SECRET_KEY=django-insecure-fp#*z+)1scwfhq(jml+vy-o+z!7g&@)&%_dr0br0jov6!=4=@6qiq
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings (configured for LOCAL development)
# Docker PostgreSQL accessed from host machine
POSTGRES_NAME=site_registry
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
EOF

echo "✅ .env configured for local development"
echo "Make sure Docker PostgreSQL is running: docker compose up -d db"
echo "Then run: python manage.py runserver"
