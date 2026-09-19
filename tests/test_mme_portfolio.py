"""MMA 150-max portfolio read (9/19/26) — shared verbatim with the Sim."""
from __future__ import annotations

import json
import random

from src import mme_portfolio as mp

FIGHTERS = [f"F{i}" for i in range(24)]
# Fight pairs: (F0,F1), (F2,F3) ... — ownership skewed toward even indexes.
OWN = {f: (40.0 if i % 2 == 0 else 8.0) for i, f in enumerate(FIGHTERS)}


def _field(n_users_big=12, n_small=300, seed=7):
    rng = random.Random(seed)
    entries = []

    def lineup():
        picks = []
        for pair in range(0, 24, 2):
            if len(picks) == 6:
                break
            if rng.random() < 0.6:
                picks.append(FIGHTERS[pair] if rng.random() < 0.8 else FIGHTERS[pair + 1])
        while len(picks) < 6:
            f = rng.choice(FIGHTERS)
            if f not in picks and FIGHTERS[FIGHTERS.index(f) ^ 1] not in picks:
                picks.append(f)
        return picks

    for u in range(n_users_big):
        for k in range(150):
            entries.append({"entry_name": f"big{u} ({k + 1}/150)", "players": lineup()})
    for u in range(n_small):
        for k in range(rng.randint(1, 20)):
            entries.append({"entry_name": f"small{u} ({k + 1}/20)", "players": lineup()})
    for k in range(6):
        entries.append({"entry_name": f"RyvlesGaming30 ({k + 1}/6)", "players": lineup()})
    # Score = sum of a hidden per-fighter score; rank by it.
    score = {f: rng.uniform(20, 120) for f in FIGHTERS}
    for e in entries:
        e["points"] = round(sum(score[p] for p in e["players"]), 2)
    entries.sort(key=lambda e: -e["points"])
    for i, e in enumerate(entries, 1):
        e["rank"] = i
    return entries


def _is_me(name):
    return mp.strip_entry_suffix(name) == "RyvlesGaming30"


def test_small_field_not_gradable():
    rep = mp.portfolio_report(_field(n_users_big=1, n_small=20), OWN, is_user=_is_me)
    assert rep["gradable"] is False and "below the MME cut" in rep["reason"]
    assert mp.portfolio_summary(rep) is None
    assert "Not graded" in mp.portfolio_md(rep)


def test_big_field_report_shape_and_json_safe():
    entries = _field()
    rep = mp.portfolio_report(entries, OWN, is_user=_is_me, places_paid=len(entries) // 5)
    assert rep["gradable"] and rep["n_field"] == len(entries)
    assert not rep["cash_cut_estimated"]
    # Entrant mix covers the whole field exactly once.
    assert sum(m["entries"] for m in rep["entrant_mix"]) == rep["n_field"]
    assert sum(m["top1_entries"] for m in rep["entrant_mix"]) == len(
        [e for e in entries if e["rank"] <= rep["top1_cut"]])
    full = next(m for m in rep["entrant_mix"] if m["bucket"].startswith("150"))
    assert full["users"] == 12 and full["entries"] == 1800
    # Shapes and dupes are populated.
    for key in ("winner", "top1", "top10", "field"):
        assert rep["shape"][key]["sum_own_med"] is not None
    assert rep["dupes"]["unique_lineups"] <= rep["n_field"]
    assert rep["winner"]["copies"] >= 1 and len(rep["winner"]["players"]) == 6
    # Big players: 12 people at 150, with correlations + thirds.
    b = rep["big_players"]
    assert b["n"] == 12 and b["top1_median"] is not None
    assert set(b["corr_with_top1"]) == {"own_med", "max_exposure_pct", "hhi",
                                        "field_copies_mean", "fighters_used"}
    assert len(b["thirds_by_own"]) == 3 and len(b["best"]) == 5
    # The user's stack + the head-to-head deltas.
    u = rep["user"]
    assert u["n"] == 6 and u["fighters_used"] <= 24 and 0 <= u["top1_pct"] <= 100
    assert "top1_pct" in u["vs_big_median"]
    json.dumps(rep)  # archive-safe
    line = mp.portfolio_summary(rep)
    assert "you: 6 entries" in line and "big-stack median" in line
    md = mp.portfolio_md(rep, "contest-standings-1.csv")
    for needle in ("150-max portfolio read", "Who is in the field", "Lineup shape",
                   "Duplication", "big stacks", "**You:**", "not a rule"):
        assert needle in md, needle


def test_no_user_entries_reports_it():
    rep = mp.portfolio_report(_field(), OWN, is_user=lambda n: False)
    assert rep["gradable"] and rep["user"] is None
    assert "None of your entries were found" in mp.portfolio_md(rep)


def test_entry_suffix_strip():
    assert mp.strip_entry_suffix("mayamaya (111/150)") == "mayamaya"
    assert mp.strip_entry_suffix("solo") == "solo"
    assert mp.strip_entry_suffix(None) == ""
