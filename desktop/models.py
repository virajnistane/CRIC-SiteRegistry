from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SiteDTO:
    id: int
    name: str
    region: str
    status: str
    cpu_capacity: int
    storage_tb: float

    @classmethod
    def from_api(cls, payload: dict) -> "SiteDTO":
        return cls(
            id=payload["id"],
            name=payload["name"],
            region=payload["region"],
            status=payload["status"],
            cpu_capacity=payload["cpu_capacity"],
            storage_tb=payload["storage_tb"],
        )