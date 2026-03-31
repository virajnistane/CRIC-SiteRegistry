import pytest # type: ignore
from django.urls import reverse # type: ignore
from rest_framework.test import APIClient # type: ignore
from sites.models import Site

@pytest.mark.django_db
def test_create_and_list_sites():
    client = APIClient()

    url = reverse("site-list")
    payload = {
        "name": "CERN-PROD",
        "region": "EU",
        "status": "online",
        "cpu_capacity": 1024,
        "storage_tb": 500.0,
    }
    response = client.post(url, payload, format="json")
    assert response.status_code == 201
    assert Site.objects.count() == 1

    list_resp = client.get(url)
    assert list_resp.status_code == 200
    assert list_resp.data[0]["name"] == "CERN-PROD"
