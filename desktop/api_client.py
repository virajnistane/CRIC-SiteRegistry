from __future__ import annotations

from typing import Any

import httpx

from desktop.config import API_BASE_URL, REQUEST_TIMEOUT_SECONDS
from desktop.models import SiteDTO


class SiteApiClient:
    def __init__(self, base_url: str = API_BASE_URL) -> None:
        self.base_url = base_url
        self.timeout = REQUEST_TIMEOUT_SECONDS

    async def list_sites(self) -> list[SiteDTO]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.base_url)
            response.raise_for_status()
            payload = response.json()
            return [SiteDTO.from_api(item) for item in payload]

    async def get_site(self, site_id: int) -> SiteDTO:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}{site_id}/")
            response.raise_for_status()
            return SiteDTO.from_api(response.json())

    async def update_site(self, site_id: int, data: dict[str, Any]) -> SiteDTO:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.patch(f"{self.base_url}{site_id}/", json=data)
            response.raise_for_status()
            return SiteDTO.from_api(response.json())

    async def create_site(self, data: dict[str, Any]) -> SiteDTO:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.base_url, json=data)
            response.raise_for_status()
            return SiteDTO.from_api(response.json())

    async def delete_site(self, site_id: int) -> None:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(f"{self.base_url}{site_id}/")
            response.raise_for_status()