"""Field / Fish autopsy analysis + cumulative tendencies store."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402

from src.field_analysis import field_profile  # noqa: E402
from src import field_tendencies as ft  # noqa: E402


def _standings():
    """Synthetic standings: 'Chalky' is field chalk (in most lineups). Winners
    (low Rank) ride it; fish (high Rank) over-play 'Trap'."""
    rows = []
    # 4 winners: Chalky + Sharp (Sharp = the leverage that hit)
    for r in range(1, 5):
        rows.append((r, f"win{r}", 300 - r, ["Chalky", "Sharp", "B", "C", "D", "E"]))
    # 6 fish: Chalky + Trap (Trap = fish-only)
    for r in range(5, 11):
        rows.append((r, f"fish{r}", 100 - r, ["Chalky", "Trap", "B", "C", "F", "G"]))
    lineups = pd.DataFrame({
        "Rank": [x[0] for x in rows],
        "EntryId": range(len(rows)),
        "EntryName": [x[1] for x in rows],
        "Points": [float(x[2]) for x in rows],
        "Lineup_parsed": [x[3] for x in rows],
    })
    names = ["Chalky", "Sharp", "Trap", "B", "C", "D", "E", "F", "G"]
    own = {"Chalky": 90.0, "Sharp": 3.0, "Trap": 40.0, "B": 30.0, "C": 25.0,
           "D": 8.0, "E": 6.0, "F": 20.0, "G": 15.0}
    players = pd.DataFrame({"name": names,
                            "actual_own": [own[n] for n in names],
                            "actual_fpts": [50.0 if n in ("Chalky", "Sharp") else 10.0 for n in names]})
    return {"lineups": lineups, "players": players}


def test_crowd_and_fish_signals():
    fp = field_profile(_standings(), "nascar", contest_type="Test SE")
    assert fp["gradable"] and fp["field_size"] == 10
    # Chalky is the most field-owned → top crowded player.
    assert fp["crowded_players"][0]["name"] == "Chalky"
    _traps = [t["name"] for t in fp["fish_traps"]]
    # Trap (fish-only) is flagged; Sharp (winner-only leverage) and Chalky
    # (played by BOTH → gap 0) are NOT fish traps.
    assert "Trap" in _traps
    assert "Sharp" not in _traps
    assert "Chalky" not in _traps
    assert all(t["winner_pct"] == 0.0 for t in fp["fish_traps"] if t["name"] == "Trap")
    assert fp["read"]  # produced an auto read


def test_json_serializable():
    json.dumps(field_profile(_standings(), "nascar"))  # must not raise


def test_tendencies_record_and_summarize(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    prof = field_profile(_standings(), "nascar", contest_type="Test SE")
    # Two contests of the same type → Chalky/Trap recur → "reliably crowded".
    assert ft.record("nascar", "Test SE", 10, prof, "2026-07-11") is True
    assert ft.summarize("nascar", "Test SE") is None       # 1 contest: not yet
    ft.record("nascar", "Test SE", 10, prof, "2026-07-12")
    summ = ft.summarize("nascar", "Test SE")
    assert summ["n_contests"] == 2
    assert "Chalky" in [d["name"] for d in summ["reliably_crowded"]]
    assert "Trap" in [d["name"] for d in summ["recurring_traps"]]


def test_record_skips_ungradable(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    assert ft.record("nascar", "T", 0, {"gradable": False}, "2026-07-11") is False
