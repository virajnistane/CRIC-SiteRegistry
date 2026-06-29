from __future__ import annotations

import pytest

# Skip the entire module if the C++ extension was not compiled.
# This way `pytest desktop/tests/` never fails on a machine where only
# Python deps are installed (e.g. the Qt CI job).
site_scorer = pytest.importorskip("site_scorer", reason="C++ extension not built")


def test_cpp_rank_sites_basic():
    scores = site_scorer.rank_sites(
        ["CERN-T0", "PIC"],
        ["Geneva", "Spain"],
        ["online", "offline"],
        [25000, 9000],
        [8200.0, 2800.0],
    )
    assert len(scores) == 2
    assert scores[0].name == "CERN-T0"
    assert scores[1].name == "PIC"


def test_cpp_rank_sites_offline_score():
    scores = site_scorer.rank_sites(
        ["OFFLINE-SITE"],
        ["Nowhere"],
        ["offline"],
        [10000],
        [1000.0],
    )
    assert scores[0].score == pytest.approx(-1.0)


def test_cpp_rank_sites_mismatched_lengths_raises():
    with pytest.raises(Exception):
        site_scorer.rank_sites(
            ["A", "B"],
            ["R1"],          # too short — should raise
            ["online"],
            [1000],
            [100.0],
        )


def test_cpp_sitescore_repr():
    scores = site_scorer.rank_sites(
        ["TEST"], ["R"], ["online"], [5000], [500.0]
    )
    r = repr(scores[0])
    assert "TEST" in r
    assert "score=" in r