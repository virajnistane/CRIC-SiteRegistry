# API Endpoints Guide

## Available URLs

Your application has the following endpoints:

### 🏠 Welcome Page
**URL:** http://localhost:8000/  
**Method:** GET  
**Description:** API information and available endpoints

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Welcome to CRIC (Computing Resource Information Catalogue) API",
  "version": "0.1.0",
  "endpoints": {
    "admin": "/admin/",
    "api_root": "/api/",
    "sites_list": "/api/sites/",
    "site_detail": "/api/sites/{id}/"
  }
}
```

---

### 🔐 Admin Panel
**URL:** http://localhost:8000/admin/  
**Description:** Django admin interface  
**Authentication:** Required (superuser)

To create a superuser:
```bash
# Docker
docker compose exec web python manage.py createsuperuser

# Local
python manage.py createsuperuser
```

---

### 📡 API Root
**URL:** http://localhost:8000/api/  
**Method:** GET  
**Description:** DRF API root showing all available endpoints

**Example:**
```bash
curl http://localhost:8000/api/
```

---

### 🖥️ Sites API

#### List All Sites
**URL:** http://localhost:8000/api/sites/  
**Method:** GET  
**Description:** Get all infrastructure sites

**Example:**
```bash
curl http://localhost:8000/api/sites/
```

#### Create Site
**URL:** http://localhost:8000/api/sites/  
**Method:** POST  
**Description:** Create a new infrastructure site

**Example:**
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

#### Get Site Detail
**URL:** http://localhost:8000/api/sites/{id}/  
**Method:** GET  
**Description:** Get details of a specific site

**Example:**
```bash
curl http://localhost:8000/api/sites/1/
```

#### Update Site
**URL:** http://localhost:8000/api/sites/{id}/  
**Method:** PUT/PATCH  
**Description:** Update an infrastructure site

**Example:**
```bash
curl -X PATCH http://localhost:8000/api/sites/1/ \
  -H "Content-Type: application/json" \
  -d '{"cpu_capacity": 512, "status": "degraded"}'
```

#### Delete Site
**URL:** http://localhost:8000/api/sites/{id}/  
**Method:** DELETE  
**Description:** Delete an infrastructure site

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/sites/1/
```

---

### 📦 RSEs API (Rucio Storage Elements)

#### List All RSEs
**URL:** http://localhost:8000/api/rses/  
**Method:** GET  
**Description:** Get all Rucio Storage Elements

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `site` | integer | Filter by site ID |
| `protocol` | string | Filter by protocol (`davs`, `srm`, `gsiftp`, `xrootd`, `posix`) |
| `enabled` | boolean | Filter by enabled state (`true`/`false`) |

**Examples:**
```bash
# List all RSEs
curl http://localhost:8000/api/rses/

# Filter by site
curl http://localhost:8000/api/rses/?site=1

# Filter by protocol
curl http://localhost:8000/api/rses/?protocol=xrootd

# Filter by enabled state
curl http://localhost:8000/api/rses/?enabled=true

# Combine filters
curl "http://localhost:8000/api/rses/?site=1&protocol=davs"
```

#### Create RSE
**URL:** http://localhost:8000/api/rses/  
**Method:** POST  
**Description:** Create a new RSE

**Example:**
```bash
curl -X POST http://localhost:8000/api/rses/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CERN-PROD_DATADISK",
    "site": 1,
    "protocol": "xrootd",
    "deterministic": true,
    "free_tb": 500.0,
    "used_tb": 300.0,
    "enabled": true
  }'
```

#### Get RSE Detail
**URL:** http://localhost:8000/api/rses/{id}/  
**Method:** GET

```bash
curl http://localhost:8000/api/rses/1/
```

#### Update RSE
**URL:** http://localhost:8000/api/rses/{id}/  
**Method:** PUT/PATCH

```bash
curl -X PATCH http://localhost:8000/api/rses/1/ \
  -H "Content-Type: application/json" \
  -d '{"free_tb": 450.0, "used_tb": 350.0}'
```

#### Delete RSE
**URL:** http://localhost:8000/api/rses/{id}/  
**Method:** DELETE

```bash
curl -X DELETE http://localhost:8000/api/rses/1/
```

#### Get RSEs by Site
**URL:** http://localhost:8000/api/rses/by-site/{site_id}/  
**Method:** GET  
**Description:** Convenience endpoint returning all RSEs for a given site

```bash
curl http://localhost:8000/api/rses/by-site/3/
```

---

## Testing the API

### Using curl

```bash
# Create a site
curl -X POST http://localhost:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{"name": "eu-west-1", "region": "Europe", "status": "online", "cpu_capacity": 512, "storage_tb": 250.0}'

# List all sites
curl http://localhost:8000/api/sites/

# Get specific site
curl http://localhost:8000/api/sites/1/

# Update site
curl -X PATCH http://localhost:8000/api/sites/1/ \
  -H "Content-Type: application/json" \
  -d '{"cpu_capacity": 1024, "status": "degraded"}'

# Delete site
curl -X DELETE http://localhost:8000/api/sites/1/
```

### Using HTTPie (if installed)

```bash
# Install httpie
pip install httpie

# Create site
http POST localhost:8000/api/sites/ name="ap-south-1" region="Asia" status="online" cpu_capacity:=256 storage_tb:=150.5

# List sites
http GET localhost:8000/api/sites/

# Get site
http GET localhost:8000/api/sites/1/

# Update site
http PATCH localhost:8000/api/sites/1/ cpu_capacity:=512 status="degraded"

# Delete site
http DELETE localhost:8000/api/sites/1/
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create site
response = requests.post(
    f"{BASE_URL}/api/sites/",
    json={
        "name": "us-west-2",
        "region": "North America",
        "status": "online",
        "cpu_capacity": 384,
        "storage_tb": 200.0
    }
)
print(response.json())

# List sites
response = requests.get(f"{BASE_URL}/api/sites/")
print(response.json())

# Get site
response = requests.get(f"{BASE_URL}/api/sites/1/")
print(response.json())

# Update site
response = requests.patch(
    f"{BASE_URL}/api/sites/1/",
    json={"cpu_capacity": 768, "status": "degraded"}
)
print(response.json())

# Delete site
response = requests.delete(f"{BASE_URL}/api/sites/1/")
print(response.status_code)
```

### Using the Browser

Visit these URLs in your browser:
- http://localhost:8000/ - Welcome page
- http://localhost:8000/admin/ - Admin interface
- http://localhost:8000/api/ - API root (browsable API)
- http://localhost:8000/api/sites/ - Sites list (browsable API)

The browsable API allows you to:
- View all endpoints
- Test POST/PUT/PATCH requests with forms
- See response formatting
- Explore the API interactively

---

## Quick Testing

### Create Sample Data

```bash
# Create site 1
curl -X POST http://localhost:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{"name": "us-east-1", "region": "North America", "status": "online", "cpu_capacity": 256, "storage_tb": 100.5}'

# Create site 2
curl -X POST http://localhost:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{"name": "eu-west-1", "region": "Europe", "status": "online", "cpu_capacity": 512, "storage_tb": 250.0}'

# Create site 3
curl -X POST http://localhost:8000/api/sites/ \
  -H "Content-Type: application/json" \
  -d '{"name": "ap-south-1", "region": "Asia", "status": "degraded", "cpu_capacity": 128, "storage_tb": 75.0}'

# List all
curl http://localhost:8000/api/sites/
```

---

## URL Patterns Summary

| URL | Method | Description |
|-----|--------|-------------|
| `/` | GET | Welcome page |
| `/admin/` | GET | Admin panel |
| `/api/` | GET | API root |
| `/api/sites/` | GET | List all sites |
| `/api/sites/` | POST | Create site |
| `/api/sites/{id}/` | GET | Get site detail |
| `/api/sites/{id}/` | PUT | Update site (full) |
| `/api/sites/{id}/` | PATCH | Update site (partial) |
| `/api/sites/{id}/` | DELETE | Delete site |
| `/api/rses/` | GET | List all RSEs (filterable) |
| `/api/rses/` | POST | Create RSE |
| `/api/rses/{id}/` | GET | Get RSE detail |
| `/api/rses/{id}/` | PUT | Update RSE (full) |
| `/api/rses/{id}/` | PATCH | Update RSE (partial) |
| `/api/rses/{id}/` | DELETE | Delete RSE |
| `/api/rses/by-site/{site_id}/` | GET | List RSEs for a site |

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Deleted successfully |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Something went wrong |

---

## Next Steps

1. **Create a superuser** to access admin:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

2. **Visit the browsable API** at http://localhost:8000/api/

3. **Create some test data** using the examples above

4. **Explore the admin panel** at http://localhost:8000/admin/

---

## Troubleshooting

### 404 on root URL
✅ Fixed! The welcome page now shows available endpoints.

### 404 on API endpoints
Make sure the server is running:
```bash
docker compose ps  # Check Docker
curl http://localhost:8000/  # Test welcome page
```

### CSRF errors
For testing, you can disable CSRF for API endpoints or use the browsable API which handles CSRF automatically.

### Empty response
This is normal if no data has been created yet. Use POST to create some sites first.
