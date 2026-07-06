# Testing Guide

This guide shows you how to test the application both locally and with Docker.

## Quick Reference

### Testing with Docker (Recommended)
```bash
# Start containers
docker compose up -d

# Run all tests
docker compose exec web pytest

# Run tests with verbose output
docker compose exec web pytest -v

# Run specific test file
docker compose exec web pytest src/sites/tests/test_api.py

# Run tests with coverage
docker compose exec web pytest --cov

# View logs
docker compose logs -f web

# Stop containers
docker compose down
```

### Testing Locally
```bash
# 1. Start Docker PostgreSQL (needed for database)
docker compose up -d db

# 2. Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Run tests
pytest
pytest -v                              # Verbose
pytest src/sites/tests/test_api.py    # Specific file
pytest --cov                           # With coverage

# 4. Run development server
python manage.py runserver

# 5. Run Django management commands
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

## Switching Between Environments

### Current Setup
Your `.env` is currently configured for: **LOCAL DEVELOPMENT**

### To Switch to Docker
```bash
./scripts/setup-docker-env.sh
docker compose up
```

### To Switch to Local
```bash
./scripts/setup-local-env.sh
docker compose up -d db  # Keep database running
python manage.py runserver
```

## Environment Differences

| Setting | Docker | Local |
|---------|--------|-------|
| POSTGRES_HOST | `db` | `localhost` |
| POSTGRES_PORT | `5432` | `5433` |
| Database access | From container | From host machine |

## Test Results

Both environments are working! ✅

**Docker Test Output:**
```
src/sites/tests/test_api.py::test_create_and_list_sites PASSED [100%]
1 passed in 0.61s
```

**Local Test Output:**
```
src/sites/tests/test_api.py::test_create_and_list_sites PASSED [100%]
1 passed in 0.41s
```

## Desktop Client Tests

The desktop client has its own test suite under `desktop/tests/`:

```bash
# Run all desktop tests (requires Qt offscreen mode)
QT_QPA_PLATFORM=offscreen uv run pytest desktop/tests/ -v

# Widget tests (site table, RSE table, main window)
uv run pytest desktop/tests/test_site_table.py
uv run pytest desktop/tests/test_rse_table.py
uv run pytest desktop/tests/test_main_window.py
uv run pytest desktop/tests/test_widgets.py

# Python scorer tests
uv run pytest desktop/tests/test_scorer.py

# C++ scorer tests (requires built extension)
uv run pytest desktop/tests/test_cpp_scorer.py
```

Note: `pyproject.toml` includes `desktop/tests` in `testpaths`, so `uv run pytest` runs both backend and desktop tests together.

## CI Workflows

Two GitHub Actions workflows run tests automatically:

- **tests.yml** — Django API tests (PostgreSQL service) + desktop widget tests (`QT_QPA_PLATFORM=offscreen`)
- **cpp-binding.yml** — Builds the C++ extension and runs `test_cpp_scorer.py` (triggered on `cpp/`, `CMakeLists.txt`, or scorer file changes)

---

## Common Commands

### Database Management
```bash
# Docker
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec db psql -U postgres -d site_registry

# Local
python manage.py makemigrations
python manage.py migrate
psql -h localhost -p 5433 -U postgres -d site_registry
```

### Creating Test Database
Both pytest and Django automatically create test databases when running tests. No manual setup needed!

## Troubleshooting

### Tests fail with "connection refused"
- Make sure Docker PostgreSQL is running: `docker compose ps`
- Check your `.env` POSTGRES_HOST and POSTGRES_PORT match your environment

### "ModuleNotFoundError: No module named 'dotenv'"
```bash
# Local
uv sync

# Docker
docker compose up --build
```

### Port 5432 already in use
This is normal if you have local PostgreSQL running. The Docker setup uses port 5433 externally to avoid conflicts.

### Stale Python cache
```bash
# Clear cache and rebuild
docker compose down
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
docker compose up --build
```

## Tips

1. **Use Docker for consistency** - Matches production environment
2. **Use local for faster iteration** - No container restart needed
3. **Both share the same database** - Data persists in Docker volume
4. **Run tests before committing** - `pytest` should pass in both environments
