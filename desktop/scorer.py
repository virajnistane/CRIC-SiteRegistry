from __future__ import annotations

"""
Thin Python wrapper around the C++ site_scorer extension module.

Provides a fallback pure-Python implementation so the desktop client
degrades gracefully when the extension has not been compiled yet.
This is important for CI environments where the C++ build is a
separate job from the Qt desktop tests.
"""

from desktop.models import SiteDTO


def rank_sites(sites: list[SiteDTO]) -> list[tuple[str, float]]:
    """
    Return (name, score) pairs sorted by score descending.

    Tries the C++ extension first; falls back to pure Python if unavailable.
    """
    try:
        import site_scorer as _scorer

        scores = _scorer.rank_sites(
            [s.name       for s in sites],
            [s.region     for s in sites],
            [s.status     for s in sites],
            [s.cpu_capacity for s in sites],
            [s.storage_tb  for s in sites],
        )
        return [(sc.name, sc.score) for sc in scores]

    except ImportError:
        # Fallback: pure Python scoring — same formula, no C++ required
        def _score(s: SiteDTO) -> float:
            raw = 0.4 * (s.cpu_capacity / 10_000.0) + 0.6 * (s.storage_tb / 1_000.0)
            if s.status == "offline":
                return -1.0
            if s.status == "degraded":
                return raw * 0.5
            return raw

        ranked = sorted(sites, key=_score, reverse=True)
        return [(s.name, _score(s)) for s in ranked]