# Development Server Guide

This guide shows you how to run the Django development server in both Docker and local modes.

## Quick Start

### Option 1: Docker (Recommended) 🐳

**One command to start everything:**
```bash
./run-docker.sh
```

This will:
- Configure `.env` for Docker
- Start PostgreSQL database
- Start Django web server with Gunicorn
- Run migrations automatically
- Collect static files

**Access:**
- Application: http://localhost:8000
- Admin: http://localhost:8000/admin
- Uses Gunicorn (production-like server)

**To stop:**
Press `Ctrl+C` or run:
```bash
docker compose down
```

---

### Option 2: Local Development 💻

**One command to start:**
```bash
./run-local.sh
```

This will:
- Configure `.env` for local development
- Start PostgreSQL database (in Docker)
- Run migrations
- Start Django development server

**Access:**
- Application: http://localhost:8000
- Admin: http://localhost:8000/admin
- Uses Django's runserver (with auto-reload)

**To stop:**
Press `Ctrl+C`

---

## Manual Commands

### Docker Mode

```bash
# Start in foreground (see logs)
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f web

# Stop
docker compose down

# Rebuild and start
docker compose up --build
```

### Local Mode

```bash
# 1. Start database
docker compose up -d db

# 2. Activate virtual environment (if not already active)
source .venv/bin/activate

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver

# Optional: Run on different port
python manage.py runserver 8080
```

---

## Comparison

| Feature | Docker 🐳 | Local 💻 |
|---------|-----------|---------|
| Setup | One command | One command |
| Server | Gunicorn | Django runserver |
| Auto-reload | Yes (with --reload) | Yes (built-in) |
| Matches production | ✅ Yes | ⚠️ Partially |
| Speed | Slightly slower | Faster |
| Isolation | Complete | Uses shared database |
| Best for | Testing prod-like setup | Quick development |

---

## Creating an Admin User

### Docker:
```bash
docker compose exec web python manage.py createsuperuser
```

### Local:
```bash
python manage.py createsuperuser
```

Follow the prompts to create username, email, and password.

---

## Common Tasks

### Apply Migrations

**Docker:**
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations
```

**Local:**
```bash
python manage.py migrate
python manage.py makemigrations
```

### Access Django Shell

**Docker:**
```bash
docker compose exec web python manage.py shell
```

**Local:**
```bash
python manage.py shell
```

### Access Database

**Docker (inside container):**
```bash
docker compose exec db psql -U postgres -d site_registry
```

**From host machine:**
```bash
psql -h localhost -p 5433 -U postgres -d site_registry
```

### Collect Static Files

**Docker:**
```bash
docker compose exec web python manage.py collectstatic
```

**Local:**
```bash
python manage.py collectstatic
```

---

## Switching Between Modes

You can easily switch between Docker and local development:

### Switch to Docker:
```bash
./scripts/setup-docker-env.sh
docker compose up
```

### Switch to Local:
```bash
./scripts/setup-local-env.sh
./run-local.sh
```

The main difference is the `.env` configuration:
- **Docker:** `POSTGRES_HOST=db` and `POSTGRES_PORT=5432`
- **Local:** `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5433`

---

## Troubleshooting

### "Port 8000 already in use"

Stop any running server:
```bash
# Stop Docker
docker compose down

# Kill local server
lsof -ti:8000 | xargs kill -9
```

### "Database connection refused"

Make sure the database is running:
```bash
docker compose up -d db
docker compose ps  # Check status
```

### Changes not reflecting

**Docker:** Restart the container
```bash
docker compose restart web
```

**Local:** Server auto-reloads, but if needed:
```bash
# Press Ctrl+C and restart
python manage.py runserver
```

### Can't access admin (404 error)

Make sure migrations are applied:
```bash
# Docker
docker compose exec web python manage.py migrate

# Local
python manage.py migrate
```

### Static files not loading

**Docker:**
```bash
docker compose exec web python manage.py collectstatic --noinput
```

**Local:**
```bash
python manage.py collectstatic --noinput
```

---

## Development Workflow Recommendations

### For Daily Development:
1. **Start:** `./run-local.sh` (faster feedback loop)
2. **Code:** Make changes, see immediate results
3. **Test:** `pytest` (runs quickly)
4. **Verify:** `./run-docker.sh` (ensure it works in prod-like env)

### For Testing Deployment:
1. **Build:** `docker compose up --build`
2. **Test:** `docker compose exec web pytest`
3. **Verify:** Access http://localhost:8000

### For Production-like Testing:
Always use Docker mode to ensure consistency with production environment.

---

## Quick Tips

- 🚀 **Fastest:** Local mode with `./run-local.sh`
- 🎯 **Most accurate:** Docker mode with `./run-docker.sh`
- 🔄 **Auto-reload:** Both modes support it!
- 📊 **Debugging:** Both modes show logs in real-time
- 🗄️ **Shared database:** Both use the same PostgreSQL instance (data persists)

---

## Next Steps

1. Create a superuser: `docker compose exec web python manage.py createsuperuser`
2. Visit http://localhost:8000/admin
3. Start developing!

For testing, see [TESTING.md](TESTING.md).
