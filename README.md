# CRIC Site Registry

A Django REST Framework application for managing computing resource site registrations and Rucio Storage Elements (RSEs).

**CRIC** = **Computing Resource Information Catalogue**

> A toy project demonstrating hands-on experience with Django REST Framework, Docker, PostgreSQL, PyQt6 desktop clients, and optional C++ extensions via pybind11. Inspired by CERN's CRIC system for cataloging distributed computing resources.

## Quick Start

**Docker (Recommended):**
```bash
./run-docker.sh
```
Then visit http://localhost:8000

**Local Development:**
```bash
docker compose up -d db
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```
Then visit http://localhost:8000

**Documentation:**
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Server setup & development guide
- [docs/API.md](docs/API.md) - API endpoints & usage examples
- [docs/TESTING.md](docs/TESTING.md) - Testing guide

---

## Desktop Client

The project includes a PyQt6 desktop client with a tabbed interface for managing Sites and RSEs.

1. **Start backend API** (Docker or local):
   ```bash
   docker compose up -d db
   uv run python manage.py migrate
   uv run python manage.py runserver 127.0.0.1:8000
   ```

2. **Run desktop client**:
   ```bash
   uv run python -m desktop.main
   ```

Desktop client features:
- **Sites tab** — Refresh, Create, Delete buttons; search/filter by name, region, status; double-click to edit; status/alerts panel; optional C++ scoring column
- **RSEs tab** — Refresh, Create RSE, Delete RSE buttons; double-click to edit RSE details (protocol, capacity, enabled state)

### Optional C++ Site Scorer

The desktop client can use the optional `site_scorer` C++ extension to rank sites and show a **Score** column.

1. **Install the C++ dependency group and system prerequisites**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y cmake g++ python3-dev
   uv sync --group cpp
   ```

2. **Configure CMake from the repository root**:
   ```bash
   cmake -S . -B build/cpp \
     -DCMAKE_BUILD_TYPE=Release \
     -DPython_EXECUTABLE="$(uv run which python)"
   ```

3. **Build the extension**:
   ```bash
   cmake --build build/cpp --config Release
   ```

4. **Install the compiled module where Python can import it**:
   ```bash
   cmake --install build/cpp --prefix .
   ```

5. **Verify the module imports**:
   ```bash
   uv run python -c "import site_scorer; print(site_scorer.__doc__)"
   ```

If the extension is not built, the desktop client falls back to the pure-Python scorer so the UI still works.

---

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)

## Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cric-site-registry
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

5. **Run migrations and create superuser**
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

## Local Development (Alternative)

1. **Start Docker PostgreSQL** (for the database)
   ```bash
   docker compose up -d db
   ```

2. **Set up the local environment**
   ```bash
   uv sync
   ```

3. **Configure environment for local development**

   Update `.env` to connect to Docker PostgreSQL from your host:
   ```bash
   POSTGRES_HOST=localhost  # Changed from 'db'
   POSTGRES_PORT=5433       # Docker exposes on 5433 to avoid conflicts
   ```

4. **Run migrations**
   ```bash
   uv run python manage.py migrate
   ```

5. **Start development server**
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

---

## Data Models

### Site

Represents an infrastructure/data center site:

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField (unique) | Site identifier, e.g. "us-east-1" |
| `region` | CharField | Geographic region, e.g. "North America" |
| `status` | CharField | `online`, `offline`, or `degraded` |
| `cpu_capacity` | IntegerField | CPU capacity in cores |
| `storage_tb` | FloatField | Storage capacity in TB |

### RSE (Rucio Storage Element)

Represents a named storage resource attached to a Site:

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField (unique) | RSE name, e.g. "CERN-PROD_DATADISK" |
| `site` | ForeignKey → Site | Parent computing site (cascade delete) |
| `protocol` | CharField | `davs`, `srm`, `gsiftp`, `xrootd`, or `posix` |
| `deterministic` | BooleanField | Whether LFN→PFN mapping is deterministic |
| `free_tb` | FloatField | Free space in TB |
| `used_tb` | FloatField | Used space in TB |
| `enabled` | BooleanField | Whether the RSE is active |

Computed properties: `total_tb`, `utilisation_pct`

### Example API Calls

```bash
# Create a site
curl -X POST http://127.0.0.1:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{"name":"us-east-1","region":"North America","status":"online","cpu_capacity":256,"storage_tb":100.5}'

# Create an RSE for that site
curl -X POST http://127.0.0.1:8000/api/rses/ \
  -H "Content-Type: application/json" \
  -d '{"name":"US-EAST-1_DATADISK","site":1,"protocol":"xrootd","free_tb":50.0,"used_tb":30.0}'

# List RSEs for a site
curl http://127.0.0.1:8000/api/rses/?site=1

# Filter by protocol
curl http://127.0.0.1:8000/api/rses/?protocol=xrootd
```

See [docs/API.md](docs/API.md) for complete API documentation.

---

## CI/CD

Two GitHub Actions workflows run on push/PR:

- **tests.yml** — Runs Django API tests against PostgreSQL + desktop widget tests (Qt offscreen mode)
- **cpp-binding.yml** — Builds the C++ scorer extension and runs scorer-specific tests (triggered on changes to `cpp/`, `CMakeLists.txt`, or scorer files)

---

## Testing

```bash
# Run all tests (Docker)
docker compose exec web pytest

# Run all tests (local — needs PostgreSQL running)
docker compose up -d db
uv run pytest

# Backend API tests only
uv run pytest src/

# Desktop client tests only
uv run pytest desktop/tests/

# C++ scorer tests
uv run pytest desktop/tests/test_cpp_scorer.py

# With coverage
uv run pytest --cov
```

See [docs/TESTING.md](docs/TESTING.md) for full details.

---

## Project Structure

```
cric-site-registry/
├── cpp/                    # Optional C++ scorer extension (CMake + pybind11)
│   ├── site_scorer.cpp
│   └── CMakeLists.txt
├── desktop/                # PyQt6 desktop client
│   ├── main.py             # Entry point
│   ├── config.py           # API base URL config
│   ├── models.py           # SiteDTO
│   ├── rse_models.py       # RseDTO
│   ├── api_client.py       # Site API client (httpx)
│   ├── rse_client.py       # RSE API client (httpx)
│   ├── scorer.py           # Python wrapper around optional C++ scorer
│   ├── widgets/
│   │   ├── main_window.py  # Tabbed main window (Sites + RSEs)
│   │   ├── site_table.py   # Site table model/view
│   │   ├── site_detail.py  # Site create/edit dialog
│   │   ├── rse_table.py    # RSE table model/view
│   │   ├── rse_detail.py   # RSE create/edit dialog
│   │   └── status_panel.py # Alerts and status display
│   └── tests/              # Desktop widget & scorer tests
├── src/
│   ├── site_registry/      # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── views.py        # Welcome API view
│   ├── sites/              # Sites app (CRUD API)
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   └── rucio/              # RSE app (CRUD + filtering + by-site endpoint)
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── tests/
├── dev_guides/             # Internal development guides
├── scripts/                # Helper scripts (setup-docker-env, setup-local-env)
├── .github/workflows/      # CI: tests.yml, cpp-binding.yml
├── run-docker.sh           # One-command Docker startup
├── run-local.sh            # One-command local startup
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env                    # Environment variables (not in git)
```

---

## Environment Variables

| Variable | Docker | Local | Description |
|----------|--------|-------|-------------|
| `DEBUG` | `True` | `True` | Enable debug mode |
| `SECRET_KEY` | (generated) | (generated) | Django secret key |
| `POSTGRES_HOST` | `db` | `localhost` | Database host |
| `POSTGRES_PORT` | `5432` | `5433` | Database port |
| `POSTGRES_NAME` | `site_registry` | `site_registry` | Database name |
| `POSTGRES_USER` | `postgres` | `postgres` | Database user |
| `POSTGRES_PASSWORD` | (in .env) | (in .env) | Database password |
| `ALLOWED_HOSTS` | `*` | `*` | Allowed host headers |

See `.env.example` for a complete template.

---

## Database

PostgreSQL, persisted in a Docker volume (`postgres_data`). Exposed on port **5433** on the host to avoid conflicts with local PostgreSQL instances.

```bash
# Access from container
docker compose exec db psql -U postgres -d site_registry

# Access from host
psql -h localhost -p 5433 -U postgres -d site_registry
```

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make changes following the project structure
3. Run tests: `uv run pytest`
4. Run linters: `uv run ruff check .`
5. Commit and push: `git push origin feature/your-feature-name`
6. Open a pull request

---

## Troubleshooting

### Port 5432 already in use
A local PostgreSQL is running. The Docker setup uses port 5433 externally to avoid this conflict.

### "Cannot connect to database" when running locally
1. Ensure Docker PostgreSQL is running: `docker compose up -d db`
2. Check `.env` has `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5433`

### Tests fail with "Connection refused"
Start the database first: `docker compose up -d db`

### POST returns 400 Bad Request
- Duplicate `name` (unique constraint)
- Invalid `status` (must be `online`, `offline`, or `degraded`)
- Invalid `protocol` for RSEs (must be `davs`, `srm`, `gsiftp`, `xrootd`, or `posix`)

### "Module not found" errors
```bash
uv sync          # local
docker compose up --build  # Docker
```

---

## License

[Add your license here]
