"""Tests for the Projections-tab breakdown helpers in src/landscape.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402

from src import landscape  # noqa: E402


def _pool():
    # name, salary, proj, own, ceiling, tee_time
    rows = [
        ("Stud Chalk",   11000, 70, 28, 95, "8:10"),   # high own, high ceiling
        ("Chalk Twin",   10800, 69, 26, 92, "8:20"),   # anchor-equivalence peer
        ("Hidden Gem",    7200, 52,  4, 90, "13:40"),  # low own, high ceiling -> underowned edge
        ("Public Trap",   8500, 50, 30, 58, "8:30"),   # high own, low ceiling -> overowned / fragile chalk
        ("PM Punt",       5800, 38,  2, 72, "14:05"),  # cheap PM leverage
        ("Mid Bal",       7000, 47, 12, 66, "13:10"),
    ]
    return pd.DataFrame(rows, columns=["name", "salary", "proj_points", "ownership", "ceiling", "tee_time"])


def test_leverage_table_orders_high_ceiling_low_own_first():
    lev = landscape.leverage_table(_pool(), top_n=3)
    # Hidden Gem (ceil 90, own 4) and PM Punt (ceil 72, own 2) should top the board.
    assert lev.iloc[0]["name"] in {"Hidden Gem", "PM Punt"}
    assert "Stud Chalk" not in list(lev["name"])[:2]


def test_mispricing_flags_underowned_and_overowned():
    out = landscape.mispricing_table(_pool(), top_n=6)
    under_names = list(out["underowned"]["name"])
    over_names = list(out["overowned"]["name"])
    assert "Hidden Gem" in under_names[:2]          # high ceiling, tiny own
    assert out["underowned"].iloc[0]["edge"] > 0
    assert "Public Trap" in over_names[:2]          # high own, low ceiling
    assert out["overowned"].iloc[0]["edge"] < 0


def test_tee_wave_split_buckets_am_pm():
    w = landscape.tee_wave_split(_pool())
    assert set(w["wave"]) == {"AM", "PM"}
    am = w[w["wave"] == "AM"].iloc[0]
    assert am["players"] == 3            # 8:10, 8:20, 8:30
    pm = w[w["wave"] == "PM"].iloc[0]
    assert pm["sub-5%"] if "sub-5%" in w.columns else pm["sub-5% leverage"] >= 1  # PM Punt @2%


def test_value_by_tier_returns_a_leader_per_present_tier():
    vbt = landscape.value_by_tier(_pool())
    assert not vbt.empty
    assert "best ceiling/$1k" in vbt.columns
    assert vbt["n"].sum() == 6


def test_anchor_equivalence_groups_two_chalk_anchors():
    groups = landscape.anchor_equivalence_check(_pool(), own_window=5.0)
    assert any(set(["Stud Chalk", "Chalk Twin"]).issubset(set(g["players"])) for g in groups)


def test_breakdown_flags_nonempty_and_mentions_edges():
    flags = landscape.breakdown_flags(_pool())
    assert flags and isinstance(flags, list)
    blob = " ".join(flags).lower()
    assert "underowned" in blob or "anchor" in blob


def test_volatility_table_boom_and_fragile():
    out = landscape.volatility_table(_pool())
    assert "Public Trap" in list(out["fragile_chalk"]["name"])  # high own, capped ceiling
    assert out["boom"].iloc[0]["boom_pct"] >= out["boom"].iloc[-1]["boom_pct"]


def test_upside_fallback_without_ceiling():
    df = _pool().drop(columns=["ceiling"])
    df["stddev"] = 12.0
    up = landscape._upside(df)
    assert (up == df["proj_points"]).all()  # no real ceiling → passthrough, no fabricated upside


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
