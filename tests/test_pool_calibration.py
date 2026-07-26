"""Unit tests for player-pool tier calibration + ownership drift + crowded pairs."""
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import pool_calibration as pc  # noqa: E402
from src import drift, field_tendencies as ft  # noqa: E402


_MD = """# Pool
| Rank | Player | Tier | Own | How it wins |
|---|---|---|---|---|
| 1 | Alpha Guy | Core | 40% | anchor |
| 2 | Beta Guy | Core · Leverage | 8% | dart anchor |
| 3 | Gamma Guy | Okay | 12% | pivot |
| 4 | Delta Guy | Fade | 30% | trap |
"""


def _players(fpts):
    return pd.DataFrame({"name": list(fpts), "actual_fpts": list(fpts.values())})


def test_parse_tiers_strips_leverage_label():
    rows = pc.parse_pool_tiers(_MD)
    assert [r["tier"] for r in rows] == ["Core", "Core", "Okay", "Fade"]
    assert rows[0]["name"] == "Alpha Guy"


def test_ordering_held_and_broke():
    ok = pc.grade_tiers(_MD, _players(
        {"Alpha Guy": 50, "Beta Guy": 40, "Gamma Guy": 30, "Delta Guy": 10}))
    assert ok["gradable"] and ok["tiers_ordered"] is True and not ok["leakage"]

    broke = pc.grade_tiers(_MD, _players(
        {"Alpha Guy": 20, "Beta Guy": 20, "Gamma Guy": 45, "Delta Guy": 60}))
    assert broke["tiers_ordered"] is False
    assert broke["leakage"] and broke["leakage"][0]["name"] == "Delta Guy"
    assert "OUT OF ORDER" in broke["summary"]


def test_not_gradable_without_table():
    assert pc.grade_tiers("no table here", _players({"A": 1}))["gradable"] is False


def test_ownership_drift_flags_crossers():
    with tempfile.TemporaryDirectory() as td:
        prior = drift._CONTRACT_DIR
        drift._CONTRACT_DIR = Path(td)
        try:
            (Path(td) / "nascar.json").write_text(json.dumps({
                "generated_at": "2026-07-14 10:00",
                "leverage_candidates": [
                    {"name": "Dart One", "own": 6.0},   # will cross 10%
                    {"name": "Dart Two", "own": 8.0},   # small move only
                    {"name": "Dart Three", "own": 9.0}, # collapses (still flagged, delta)
                ],
            }))
            pool = pd.DataFrame({
                "name": ["Dart One", "Dart Two", "Dart Three"],
                "ownership": [12.0, 8.5, 4.0],
            })
            d = drift.ownership_drift("nascar", pool)
            assert d["n_checked"] == 3
            names = {r["name"]: r for r in d["drifted"]}
            assert names["Dart One"]["crossed_leverage_line"] is True
            assert "Dart Two" not in names  # +0.5 is noise
            assert names["Dart Three"]["delta"] == -5.0
            assert "crossed the 10% line" in drift.drift_md(d)
        finally:
            drift._CONTRACT_DIR = prior


def test_recurring_pairs_rollup():
    with tempfile.TemporaryDirectory() as td:
        prior = ft._REPO_ROOT
        ft._REPO_ROOT = Path(td)
        try:
            d = Path(td) / "rules" / "nascar"
            d.mkdir(parents=True)
            rows = [
                {"contest_type": "SE", "crowded_players": ["A"], "fish_traps": [],
                 "crowded_combos": [["A", "B"], ["A", "C"]]},
                {"contest_type": "SE", "crowded_players": ["A"], "fish_traps": [],
                 "crowded_combos": [{"players": ["B", "A"]}]},  # dict form, reversed
            ]
            (d / "field_tendencies.jsonl").write_text(
                "\n".join(json.dumps(r) for r in rows) + "\n")
            s = ft.summarize("nascar", "SE")
            assert s["recurring_pairs"] == [
                {"players": ["A", "B"], "in_n": 2, "of": 2}]
            assert "PAIRS" in ft._crowd_traps_str(s)
        finally:
            ft._REPO_ROOT = prior


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


def test_scratched_player_excluded_from_tier_averages():
    """An exact-0.0 FPTS means the player didn't compete (scratched fight).
    Counting it as a real zero falsely breaks tier ordering — the 7/26
    Ankalaev slate's Dulatov (cancelled fight) dragged Core under Good."""
    cal = pc.grade_tiers(_MD, _players(
        {"Alpha Guy": 96.2, "Beta Guy": 0.0, "Gamma Guy": 45, "Delta Guy": 10}))
    # Beta Guy's 0.0 is excluded: Core avg is Alpha's 96.2, ordering holds.
    core = next(t for t in cal["tiers"] if t["tier"] == "Core")
    assert core["n"] == 1 and core["avg_fpts"] == 96.2
    assert cal["tiers_ordered"] is True
    assert cal["excluded_scratches"] == [{"name": "Beta Guy", "tier": "Core"}]
    assert cal["n_matched"] == 3
    md = pc.calibration_md(cal)
    assert "Excluded as likely scratches" in md and "Beta Guy" in md


def test_near_zero_score_is_not_a_scratch():
    """0.1 FPTS is a real (terrible) result — only exact 0.0 is excluded."""
    cal = pc.grade_tiers(_MD, _players(
        {"Alpha Guy": 96.2, "Beta Guy": 0.2, "Gamma Guy": 45, "Delta Guy": 10}))
    core = next(t for t in cal["tiers"] if t["tier"] == "Core")
    assert core["n"] == 2 and core["avg_fpts"] == 48.2
    assert cal["excluded_scratches"] == []
