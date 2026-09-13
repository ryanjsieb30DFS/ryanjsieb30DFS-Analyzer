"""Preliminary vs final ETR file (NFL Classic stage 2, 9/12/26)."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import projections_snapshot as ps  # noqa: E402


def _prev():
    return pd.DataFrame([
        {"name": "Patrick Mahomes", "position": "QB", "team": "KC", "salary": 8000,
         "proj_points": 22.0, "ownership": 18.0},
        {"name": "Hurt Receiver", "position": "WR", "team": "KC", "salary": 6000,
         "proj_points": 14.0, "ownership": 12.0},
        {"name": "Steady Back", "position": "RB", "team": "DEN", "salary": 6500,
         "proj_points": 15.0, "ownership": 20.0},
        {"name": "Cheap Tight End", "position": "TE", "team": "NYJ", "salary": 3000,
         "proj_points": 6.0, "ownership": 2.0},
    ])


def _cur():
    return pd.DataFrame([
        {"name": "Patrick Mahomes", "position": "QB", "team": "KC", "salary": 8000,
         "proj_points": 22.3, "ownership": 21.5},           # own +3.5 → flagged
        {"name": "Steady Back", "position": "RB", "team": "DEN", "salary": 6500,
         "proj_points": 15.4, "ownership": 21.0},           # tiny moves → not flagged
        {"name": "Cheap Tight End", "position": "TE", "team": "NYJ", "salary": 3000,
         "proj_points": 7.5, "ownership": 2.0},             # +1.5 = 25% → flagged
        {"name": "Backup Receiver", "position": "WR", "team": "KC", "salary": 4000,
         "proj_points": 9.0, "ownership": 5.0},             # new
    ])


def test_diff_flags_gone_new_and_swings():
    d = ps.diff_prelim_vs_final(_prev(), _cur(), pool_names=["Hurt Receiver", "Patrick Mahomes"])
    assert [g["name"] for g in d["gone"]] == ["Hurt Receiver"]
    assert d["gone"][0]["in_pool"] is True
    assert [n["name"] for n in d["new"]] == ["Backup Receiver"]
    flagged = {f["name"]: f["reasons"] for f in d["flagged"]}
    assert "Patrick Mahomes" in flagged and any(r.startswith("own") for r in flagged["Patrick Mahomes"])
    assert "Cheap Tight End" in flagged and any(r.startswith("proj") for r in flagged["Cheap Tight End"])
    assert "Steady Back" not in flagged
    hits = [h["name"] for h in d["pool_hits"]]
    assert hits == ["Hurt Receiver", "Patrick Mahomes"]
    md = ps.diff_md(d)
    assert "Hurt Receiver" in md and "IN YOUR POOL" in md and "Backup Receiver" in md


def test_snapshot_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(ps, "_SNAP_DIR", tmp_path)
    assert ps.load_prelim("nfl_classic") is None
    ps.save_prelim("nfl_classic", "Main Slate (42).csv", "ETR", _prev())
    blob = ps.load_prelim("nfl_classic")
    assert blob["source_name"] == "Main Slate (42).csv" and len(blob["df"]) == 4
    ps.clear_prelim("nfl_classic")
    assert ps.load_prelim("nfl_classic") is None
