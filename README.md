# Cricket Site Registry

A Django REST Framework application for managing cricket site registrations.

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cric-site-registry
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration if needed.

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

5. **Create a superuser** (in a new terminal)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Local Development

1. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Update POSTGRES_HOST=localhost in .env for local development
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

## Docker Commands

- **Start services**: `docker-compose up`
- **Start in background**: `docker-compose up -d`
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs -f`
- **Rebuild**: `docker-compose up --build`
- **Run management commands**: `docker-compose exec web python manage.py <command>`

## Database

The application uses PostgreSQL in Docker. The data is persisted in a Docker volume named `postgres_data`.

**Port Mapping:** PostgreSQL is exposed on port **5433** on your host machine (to avoid conflicts with local PostgreSQL instances).

To access the database directly from inside the container:
```bash
docker compose exec db psql -U postgres -d site_registry
```

To connect from your host machine:
```bash
psql -h localhost -p 5433 -U postgres -d site_registry
# Or use any PostgreSQL client with: localhost:5433
```

## Environment Variables

See `.env.example` for all available configuration options:
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `POSTGRES_NAME`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port

## Security Best Practices

**⚠️ IMPORTANT: Never commit the `.env` file to version control!**

1. **SECRET_KEY**: Generate a new secret key for production:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Database Credentials**: Use strong passwords for production:
   - Minimum 16 characters
   - Mix of uppercase, lowercase, numbers, and symbols
   - Different from default values

3. **DEBUG Mode**: Always set `DEBUG=False` in production

4. **ALLOWED_HOSTS**: Set specific domains for production (not `*`)

5. **Environment Files**:
   - `.env` is gitignored and contains actual secrets
   - `.env.example` is committed as a template (no real secrets)
   - [docker-compose.yml](docker-compose.yml) references environment variables, not hardcoded values

## Project Structure

```
cric-site-registry/
├── site_registry/       # Django project settings
├── sites/              # Sites app
├── manage.py           # Django management script
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── pyproject.toml      # Python dependencies
```

## Contributing

1. Create a new branch
2. Make your changes
3. Run tests: `pytest`
4. Submit a pull request

## License

[Add your license here]
