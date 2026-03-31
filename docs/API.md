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
  "message": "Welcome to Cricket Site Registry API",
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
