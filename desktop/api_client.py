# desktop/api_client.py
import httpx
from qasync import asyncSlot

BASE = "http://localhost:8000/api/sites/"

class SiteApiClient:
    async def list_sites(self):
        async with httpx.AsyncClient() as c:
            return (await c.get(BASE)).json()

    async def update_site(self, pk: int, data: dict):
        async with httpx.AsyncClient() as c:
            return (await c.patch(f"{BASE}{pk}/", json=data)).json()

    async def delete_site(self, pk: int):
        async with httpx.AsyncClient() as c:
            await c.delete(f"{BASE}{pk}/")