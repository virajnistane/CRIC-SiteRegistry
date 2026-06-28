# CRIC Site Registry

A Django REST Framework application for managing computing resource site registrations.

**CRIC** = **Computing Resource Information Catalogue**

> This is a toy project demonstrating hands-on experience with Django REST Framework, Docker, PostgreSQL, and infrastructure management APIs. Inspired by [CERN's CRIC system](https://careers.cern/jobs/it-ce-lcg-2026-54-grap/) for cataloging distributed computing resources.

## 🚀 Quick Start

**Docker (Recommended):**
```bash
./run-docker.sh
```
Then visit http://localhost:8000

**Local Development:**
```bash
./run-local.sh
```
Then visit http://localhost:8000

📖 **Documentation:**
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Server setup & development guide
- [docs/API.md](docs/API.md) - API endpoints & usage examples
- [docs/TESTING.md](docs/TESTING.md) - Testing guide

## Desktop Client

The project also includes a PyQt desktop client for managing sites.

1. **Start backend API** (Docker or local):
   ```bash
   uv run python manage.py runserver 127.0.0.1:8000
   ```

2. **Run desktop client**:
   ```bash
   uv run python -m desktop.main
   ```

Desktop client includes:
- Top action row with **Refresh**, **Create New Site**, and **Delete Selected Site** buttons
- Search box filter (name, region, status)
- Double-click row to edit a site
- Alerts/status panel on the right

---

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)

## Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cric-site-registry
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   For Docker, the default values in `.env.example` work out of the box. The `.env` file is already configured for Docker with `POSTGRES_HOST=db`.

3. **Build and run with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

5. **Run migrations and create superuser**
   ```bash
   # Migrations run automatically on startup, but you can run manually:
   docker compose exec web python manage.py migrate
   
   # Create admin user
   docker compose exec web python manage.py createsuperuser
   ```

   Note: Django admin credentials are not stored in `.env`. Create a new superuser or reset the password if you lose access.

## Local Development (Alternative)

**Note:** Docker is recommended. Local development requires additional setup.

1. **Start Docker PostgreSQL** (for the database)
   ```bash
   docker compose up -d db
   ```

2. **Set up the local environment**
   ```bash
   uv sync
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

   `uv sync` creates and updates the project environment in `.venv`. If you prefer a manual virtual environment, activate it and run the same management commands without `uv run`.

4. **Configure environment for local development**
   
   Update `.env` to connect to Docker PostgreSQL from your host:
   ```bash
   POSTGRES_HOST=localhost  # Changed from 'db'
   POSTGRES_PORT=5433       # Docker exposes on 5433 to avoid conflicts
   ```

5. **Run migrations**
   ```bash
   uv run python manage.py migrate
   ```

6. **Create or recover the admin user**
   ```bash
   # Create a new admin user
   uv run python manage.py createsuperuser

   # Reset the password for an existing admin user
   uv run python manage.py changepassword <username>
   ```

   Note: Django admin credentials are not stored in `.env`. Use `createsuperuser` when no admin account exists, or `changepassword` when you only need to reset the password.

7. **Start development server**
   ```bash
   uv run python manage.py runserver
   ```

## Docker Commands

- **Start services**: `docker compose up`
- **Start in background**: `docker compose up -d`
- **Stop services**: `docker compose down`
- **View logs**: `docker compose logs -f`
- **Rebuild**: `docker compose up --build`
- **Run management commands**: `docker compose exec web python manage.py <command>`

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

The application uses environment variables for configuration, loaded from a `.env` file via `python-dotenv`.

### Configuration Options:
- `DEBUG`: Enable/disable debug mode (`True`/`False`)
- `SECRET_KEY`: Django secret key (generate new for production)
- `POSTGRES_NAME`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_HOST`: Database host
  - **Docker:** `db` (container name)
  - **Local development:** `localhost`
- `POSTGRES_PORT`: Database port
  - **Docker internal:** `5432`
  - **Host machine:** `5433`
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Example Configurations:

**For Docker (default):**
```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

**For Local Development:**
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

See `.env.example` for a complete template.

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
├── src/
│   ├── site_registry/   # Django project settings
│   │   ├── settings.py  # Main configuration
│   │   ├── urls.py      # URL routing
│   │   └── views.py     # Welcome API view
│   └── sites/          # Sites app
│       ├── models.py    # Site model (name, region, status, cpu_capacity, storage_tb)
│       ├── serializers.py
│       ├── views.py
│       └── tests/
├── scripts/             # Helper scripts
│   ├── setup-docker-env.sh
│   └── setup-local-env.sh
├── run-docker.sh        # One-command Docker startup
├── run-local.sh         # One-command local startup
├── test-api.sh          # API testing script
├── manage.py            # Django management script
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── pyproject.toml       # Python dependencies
└── .env                 # Environment variables (not in git)
```

## Site Model Fields

The Site model represents infrastructure/data center sites with the following fields:

- **name** (CharField): Unique site identifier (e.g., "us-east-1", "eu-west-1")
- **region** (CharField): Geographic region (e.g., "North America", "Europe", "Asia")
- **status** (CharField): Operational status - choices: `online`, `offline`, `degraded`
- **cpu_capacity** (IntegerField): CPU capacity in cores
- **storage_tb** (FloatField): Storage capacity in terabytes

### Example Site Creation

```bash
curl -X POST http://localhost:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "us-east-1",
    "region": "North America",
    "status": "online",
    "cpu_capacity": 256,
    "storage_tb": 100.5
  }'
```

See [docs/API.md](docs/API.md) for complete API documentation.

## Testing

### Run Tests in Docker (Recommended)

```bash
# Run all tests
docker compose exec web pytest

# Run with verbose output
docker compose exec web pytest -v

# Run specific test file
docker compose exec web pytest src/sites/tests/test_api.py

# Run with coverage
docker compose exec web pytest --cov
```

### Run Tests Locally

**Important:** Ensure Docker PostgreSQL is running first:
```bash
# Start database
docker compose up -d db

# Run tests
uv run pytest

# With verbose output
uv run pytest -v
```

The test suite uses:
- **pytest** - Test framework
- **pytest-django** - Django integration for pytest
- **PostgreSQL** - Same database as production for accurate testing

If you already activated `.venv`, `pytest` and `pytest -v` also work.

## Contributing

1. Create a new branch for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the project structure

3. Run tests to ensure everything works
   ```bash
   docker compose exec web pytest
   ```

4. Run linters (if configured)
   ```bash
   docker compose exec web black .
   docker compose exec web ruff check .
   ```

5. Commit your changes with a descriptive message
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. Push and create a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

## Troubleshooting

### Port 5432 already in use

If you get "port 5432 already in use" error, a local PostgreSQL is running on your machine. The Docker configuration already uses port 5433 externally to avoid this conflict.

```bash
# Check what's using port 5432
sudo lsof -i :5432

# If needed, stop local PostgreSQL
sudo systemctl stop postgresql
```

### "Cannot connect to database" when running locally

Make sure:
1. **Docker PostgreSQL is running**: `docker compose up -d db`
2. Check container status: `docker compose ps`
3. Your `.env` file has `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5433`
4. The `.env` file is in the project root directory

### Tests fail with "Connection refused"

This means the PostgreSQL database isn't running:
```bash
# Start the database
docker compose up -d db

# Verify it's running
docker compose ps

# Run tests
pytest
```

### "Module not found" errors

Reinstall dependencies:
```bash
# In Docker
docker compose down
docker compose up --build

# Locally
pip install -e .
```

### Tests failing with "import file mismatch"

Clear Python cache and rebuild:
```bash
docker compose down
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
docker compose up --build
```

### Old `docker-compose` command not working

Use `docker compose` (space, not hyphen) for Docker Compose V2:
```bash
# ❌ Old: docker-compose up
# ✅ New: docker compose up
```

## License

[Add your license here]
