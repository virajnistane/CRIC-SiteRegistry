# desktop/rse_models.py
from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class RseDTO:
    id:            int
    name:          str
    site:          int          # FK integer
    site_name:     str          # read-only from API
    protocol:      str
    deterministic: bool
    free_tb:       float
    used_tb:       float
    total_tb:      float
    utilisation_pct: float
    enabled:       bool

    @classmethod
    def from_api(cls, payload: dict) -> "RseDTO":
        return cls(
            id              = payload["id"],
            name            = payload["name"],
            site            = payload["site"],
            site_name       = payload.get("site_name", ""),
            protocol        = payload["protocol"],
            deterministic   = payload["deterministic"],
            free_tb         = payload["free_tb"],
            used_tb         = payload["used_tb"],
            total_tb        = payload.get("total_tb", 0.0),
            utilisation_pct = payload.get("utilisation_pct", 0.0),
            enabled         = payload["enabled"],
        )