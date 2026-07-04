# src/rucio/tests/test_rse_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from sites.models import Site
from rucio.models import RSE


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def site(db):
    return Site.objects.create(
        name="CERN-PROD",
        region="EU",
        status="online",
        cpu_capacity=4096,
        storage_tb=1000.0,
    )


@pytest.fixture
def rse(site):
    return RSE.objects.create(
        name="CERN-PROD_DATADISK",
        site=site,
        protocol="davs",
        deterministic=True,
        free_tb=400.0,
        used_tb=600.0,
        enabled=True,
    )


@pytest.fixture
def client():
    return APIClient()


# ---------------------------------------------------------------------------
# CRUD tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_create_rse(client, site):
    url = reverse("rse-list")
    payload = {
        "name":          "CERN-PROD_TAPE",
        "site":          site.id,
        "protocol":      "srm",
        "deterministic": False,
        "free_tb":       800.0,
        "used_tb":       200.0,
        "enabled":       True,
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "CERN-PROD_TAPE"
    assert data["site_name"] == "CERN-PROD"       # read-only convenience field
    assert data["total_tb"] == 1000.0
    assert data["utilisation_pct"] == 20.0
    assert RSE.objects.count() == 1


@pytest.mark.django_db
def test_list_rses(client, rse):
    url = reverse("rse-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_retrieve_rse(client, rse):
    url = reverse("rse-detail", args=[rse.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["name"] == "CERN-PROD_DATADISK"


@pytest.mark.django_db
def test_partial_update_rse(client, rse):
    url = reverse("rse-detail", args=[rse.id])
    response = client.patch(url, {"free_tb": 300.0}, format="json")
    assert response.status_code == 200
    rse.refresh_from_db()
    assert rse.free_tb == 300.0


@pytest.mark.django_db
def test_delete_rse(client, rse):
    url = reverse("rse-detail", args=[rse.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert RSE.objects.count() == 0


# ---------------------------------------------------------------------------
# Filtering tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_filter_by_site(client, site, rse):
    url = reverse("rse-list") + f"?site={site.id}"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_filter_by_protocol(client, site, rse):
    url = reverse("rse-list") + "?protocol=xrootd"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 0   # rse uses davs, not xrootd


@pytest.mark.django_db
def test_by_site_action(client, site, rse):
    url = reverse("rse-by-site", args=[site.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()[0]["name"] == "CERN-PROD_DATADISK"


# ---------------------------------------------------------------------------
# Cascade delete test
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_rse_deleted_when_site_deleted(site, rse):
    assert RSE.objects.count() == 1
    site.delete()
    assert RSE.objects.count() == 0


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
def test_duplicate_rse_name_rejected(client, site, rse):
    url = reverse("rse-list")
    payload = {
        "name": "CERN-PROD_DATADISK",  # already exists
        "site": site.id,
        "protocol": "srm",
        "free_tb": 0.0,
        "used_tb": 0.0,
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_invalid_protocol_rejected(client, site):
    url = reverse("rse-list")
    payload = {
        "name": "CERN-PROD_TAPE",
        "site": site.id,
        "protocol": "ftp",   # not in PROTOCOL_CHOICES
        "free_tb": 0.0,
        "used_tb": 0.0,
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == 400