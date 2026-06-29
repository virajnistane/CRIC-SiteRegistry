from __future__ import annotations

import pytest

from desktop.models import SiteDTO
from desktop.scorer import rank_sites


SITES = [
    SiteDTO(1, "CERN-T0", "Geneva",  "online",   25000, 8200.0),
    SiteDTO(2, "PIC",     "Spain",   "offline",   9000, 2800.0),
    SiteDTO(3, "GRIF",    "France",  "degraded", 12000, 3100.0),
    SiteDTO(4, "RAL",     "UK",      "online",   18000, 5100.0),
]


def test_rank_sites_returns_correct_length():
    scores = rank_sites(SITES)
    assert len(scores) == len(SITES)


def test_rank_sites_offline_is_last():
    scores = rank_sites(SITES)
    # PIC is offline — must be at the bottom
    assert scores[-1][0] == "PIC"


def test_rank_sites_online_beats_degraded():
    scores = rank_sites(SITES)
    names = [name for name, _ in scores]
    # CERN-T0 and RAL are both online; GRIF is degraded
    grif_idx = names.index("GRIF")
    cern_idx = names.index("CERN-T0")
    ral_idx  = names.index("RAL")
    assert cern_idx < grif_idx
    assert ral_idx  < grif_idx


def test_rank_sites_scores_are_sorted_descending():
    scores = rank_sites(SITES)
    values = [sc for _, sc in scores]
    assert values == sorted(values, reverse=True)


def test_rank_sites_offline_score_is_negative():
    scores = rank_sites(SITES)
    pic_score = next(sc for name, sc in scores if name == "PIC")
    assert pic_score < 0


def test_rank_sites_empty_input():
    assert rank_sites([]) == []