"""Unit tests for the structural shark-gap profiler."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402

from src import shark_gap  # noqa: E402


def _parsed(lineups, players):
    """Build a parse_dk_results-shaped dict from simple inputs.
    lineups: list of (entry_name, rank, roster[list of names]).
    players: dict name -> own%.
    """
    L = pd.DataFrame([
        {"Rank": rk, "EntryName": en, "Points": 0.0, "Lineup": " ".join(r),
         "Lineup_parsed": r}
        for en, rk, r in lineups
    ])
    P = pd.DataFrame([{"name": n, "roster_position": "F",
                       "actual_own": o, "actual_fpts": 0.0}
                      for n, o in players.items()])
    return {"lineups": L, "players": P}


def test_chalk_anchors_are_highest_owned():
    parsed = _parsed(
        [("x", 1, ["A", "B", "C"])],
        {"A": 40.0, "B": 20.0, "C": 5.0, "D": 1.0},
    )
    from src.autopsy import _norm_name
    assert shark_gap.chalk_anchors(parsed, n=2) == [_norm_name("A"), _norm_name("B")]


def test_profile_envelope_leverage_and_anchor_exposure():
    # Shark: 2 lineups; both carry chalk anchor A; one carries sub-5% dart D.
    players = {"A": 30.0, "B": 12.0, "C": 10.0, "D": 2.0, "E": 8.0}
    parsed = _parsed([
        ("shark", 10, ["A", "B", "C"]),
        ("shark", 20, ["A", "D", "E"]),
    ], players)
    prof = shark_gap.structural_profile(parsed, ["shark"])
    assert prof["n_entries"] == 2
    assert prof["leverage_pct"] == 50.0          # D (<5%) in 1 of 2
    # anchor A is in both -> exposure to top anchor = 1.0 (averaged over anchors)
    assert prof["anchor_exposure_by_player"][list(prof["anchor_exposure_by_player"])[0]] == 1.0
    # own_per_slot = mean of (30+12+10)/3 and (30+2+8)/3
    assert prof["own_per_slot"] == round(((52/3) + (40/3)) / 2, 1)


def test_gap_flags_user_under_owning_the_anchor():
    # The recurring leak: user zeroes the chalk anchor the shark keeps.
    players = {"Anchor": 35.0, "B": 12.0, "C": 10.0, "D": 4.0, "E": 9.0, "F": 7.0}
    parsed = _parsed([
        ("shark", 5, ["Anchor", "B", "C"]),
        ("shark", 6, ["Anchor", "D", "E"]),
        ("me", 500, ["B", "C", "F"]),      # no Anchor
        ("me", 600, ["D", "E", "F"]),      # no Anchor
    ], players)
    gap = shark_gap.shark_gap(parsed, ["shark"], ["me"])
    assert gap["sharks_in_field"]
    ae = next(d for d in gap["deltas"] if d["dim"] == "anchor_exposure")
    assert ae["shark"] > ae["user"], "shark should out-expose user on the anchor"
    assert ae["delta"] < 0, "negative delta = user under-owns the anchors"


def test_gap_handles_no_sharks_in_field():
    parsed = _parsed([("me", 1, ["A", "B", "C"])], {"A": 20.0, "B": 10.0, "C": 5.0})
    gap = shark_gap.shark_gap(parsed, ["nobody"], ["me"])
    assert gap["sharks_in_field"] is False
    assert "No tracked sharks" in shark_gap.gap_md(gap)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
