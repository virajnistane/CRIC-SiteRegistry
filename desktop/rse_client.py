# desktop/rse_client.py
from __future__ import annotations
from typing import Any

import httpx

from desktop.config import API_BASE_URL, REQUEST_TIMEOUT_SECONDS
from desktop.rse_models import RseDTO

RSE_URL = API_BASE_URL.replace("/sites/", "/rses/")   # e.g. http://127.0.0.1:8000/api/rses/


class RseApiClient:
    def __init__(self, base_url: str = RSE_URL) -> None:
        self.base_url = base_url
        self.timeout  = REQUEST_TIMEOUT_SECONDS

    async def list_rses(self, site_id: int | None = None) -> list[RseDTO]:
        params: dict[str, Any] = {}
        if site_id is not None:
            params["site"] = site_id
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return [RseDTO.from_api(item) for item in response.json()]

    async def get_rse(self, rse_id: int) -> RseDTO:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}{rse_id}/")
            response.raise_for_status()
            return RseDTO.from_api(response.json())

    async def create_rse(self, data: dict[str, Any]) -> RseDTO:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.base_url, json=data)
            response.raise_for_status()
            return RseDTO.from_api(response.json())

    async def update_rse(self, rse_id: int, data: dict[str, Any]) -> RseDTO:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.patch(f"{self.base_url}{rse_id}/", json=data)
            response.raise_for_status()
            return RseDTO.from_api(response.json())

    async def delete_rse(self, rse_id: int) -> None:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(f"{self.base_url}{rse_id}/")
            response.raise_for_status()