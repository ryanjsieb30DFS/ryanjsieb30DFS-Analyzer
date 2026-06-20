"""Unit tests for the deterministic portfolio selection layer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import portfolio  # noqa: E402


def _cand(row, ids, names=None, ceil=100.0):
    """Minimal candidate matching resolve_pool_candidates' shape."""
    names = names or [f"P{i}" for i in ids]
    return {
        "row": row,
        "source": "pool.csv",
        "ids": [str(i) for i in ids],
        "players": [{"name": nm, "ownership": 10.0} for nm in names],
        "salary": 49000,
        "avg_own": 12.0,
        "ceil_sum": ceil,
        "sub5_skill": 1,
    }


def test_overlap_counts_shared_ids():
    a = _cand(1, [1, 2, 3, 4, 5, 6])
    b = _cand(2, [1, 2, 3, 9, 10, 11])
    assert portfolio.overlap(a, b) == 3


def test_select_prunes_near_duplicates():
    params = portfolio.default_params(6)  # max_overlap = 3
    base = [1, 2, 3, 4, 5, 6]
    cands = [
        _cand(1, base, ceil=200),
        _cand(2, [1, 2, 3, 4, 5, 7], ceil=199),   # 5 shared -> dropped
        _cand(3, [1, 2, 3, 9, 10, 11], ceil=198),  # 3 shared -> ok
        _cand(4, [20, 21, 22, 23, 24, 25], ceil=197),  # disjoint -> ok
    ]
    menu, rejected, report = portfolio.select_portfolio(cands, n_target=3, params=params)
    rows = {c["row"] for c in menu}
    assert 2 not in rows, "near-duplicate (5 shared) should be pruned"
    assert {1, 3, 4}.issubset(rows)
    assert report["n_rejected_dupe"] == 1


def test_select_always_meets_count_even_if_homogeneous():
    params = portfolio.default_params(6)
    # Every lineup shares 5 of 6 with the first -> strict diversity yields 1.
    cands = [_cand(i, [1, 2, 3, 4, 5, 5 + i], ceil=100 - i) for i in range(1, 6)]
    menu, _, report = portfolio.select_portfolio(cands, n_target=3, params=params)
    assert len(menu) >= 3, "must top up to n_target even when overlap-relaxed"
    assert report["n_overlap_relaxed"] >= 1


def test_validate_flags_overlap():
    params = portfolio.default_params(6)  # max_overlap 3
    a = _cand(1, [1, 2, 3, 4, 5, 6])
    b = _cand(2, [1, 2, 3, 4, 7, 8])  # 4 shared > 3
    v = portfolio.validate_portfolio([a, b], params)
    assert any("share 4 players" in x for x in v)


def test_validate_flags_exposure():
    params = portfolio.default_params(6)  # exposure_cap 0.6 -> 3 lineups allow 2
    # Player 1 in all 3 lineups (3/3) > ceil(0.6*3)=2, but pairwise overlap stays <=3.
    a = _cand(1, [1, 10, 11, 12, 13, 14])
    b = _cand(2, [1, 20, 21, 22, 23, 24])
    c = _cand(3, [1, 30, 31, 32, 33, 34])
    v = portfolio.validate_portfolio([a, b, c], params)
    assert any("over the 60% cap" in x for x in v)


def test_validate_clean_set_passes():
    params = portfolio.default_params(6)
    a = _cand(1, [1, 2, 3, 4, 5, 6])
    b = _cand(2, [1, 2, 3, 30, 31, 32])   # 3 shared == cap, ok
    c = _cand(3, [40, 41, 42, 43, 44, 45])
    assert portfolio.validate_portfolio([a, b, c], params) == []


def test_anchor_equivalence_violation_detected():
    params = portfolio.default_params(6)
    groups = [{"players": ["Chalk", "Alt"], "own_range": (20, 22)}]
    a = _cand(1, [1, 2, 3, 4, 5, 6], names=["Chalk", "x", "y", "z", "w", "v"])
    b = _cand(2, [1, 7, 8, 9, 10, 11], names=["Chalk", "a", "b", "c", "d", "e"])
    v = portfolio.validate_portfolio([a, b], params, anchor_groups=groups)
    assert any("Anchor-Equivalence" in x for x in v)
    # Add a lineup that avoids Chalk -> satisfied.
    c = _cand(3, [50, 51, 52, 53, 54, 55], names=["Alt", "a", "b", "c", "d", "e"])
    assert not any("Anchor-Equivalence" in x
                   for x in portfolio.validate_portfolio([a, b, c], params, anchor_groups=groups))


def test_exposure_report_renders():
    params = portfolio.default_params(6)
    a = _cand(1, [1, 2, 3, 4, 5, 6])
    b = _cand(2, [1, 2, 3, 30, 31, 32])
    md = portfolio.exposure_report_md([a, b], params)
    assert "Portfolio audit (computed)" in md
    assert "Max pairwise overlap:** 3" in md


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
