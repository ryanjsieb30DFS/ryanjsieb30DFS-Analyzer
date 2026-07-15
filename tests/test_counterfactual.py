"""Unit tests for the near-miss counterfactual + winner build story."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import counterfactual as cf  # noqa: E402


def _parsed(lineups, players):
    return {
        "lineups": pd.DataFrame(lineups),
        "players": pd.DataFrame(players),
    }


def _base():
    lineups = [
        {"Rank": 1, "EntryName": "shark (1/1)", "Points": 100.0,
         "Lineup_parsed": ["A", "B", "C"]},
        {"Rank": 2, "EntryName": "me", "Points": 90.0,
         "Lineup_parsed": ["A", "B", "D"]},
        {"Rank": 3, "EntryName": "fish", "Points": 50.0,
         "Lineup_parsed": ["D", "E", "F"]},
    ]
    players = [
        {"name": "A", "actual_own": 50.0, "actual_fpts": 40.0},
        {"name": "B", "actual_own": 30.0, "actual_fpts": 35.0},
        {"name": "C", "actual_own": 5.0, "actual_fpts": 25.0},   # winner's dart
        {"name": "D", "actual_own": 20.0, "actual_fpts": 15.0},
        {"name": "E", "actual_own": 8.0, "actual_fpts": 20.0},
        {"name": "F", "actual_own": 15.0, "actual_fpts": 15.0},
    ]
    analysis = {"user_lineups_df": pd.DataFrame([
        {"rank": 2, "entry_name": "me", "points": 90.0, "players": ["A", "B", "D"]},
    ])}
    return _parsed(lineups, players), analysis


def test_winner_story_carrier_and_dupes():
    parsed, _ = _base()
    s = cf.winner_story(parsed)
    assert s["gradable"] and s["winner_points"] == 100.0
    assert s["carrier"]["name"] == "C"  # the sub-10% piece that carried it
    assert s["n_low_own"] == 1
    # dupe risk: 0.5*0.3*0.05 * field(3) = 0.0225
    assert abs(s["expected_dupes"] - 0.02) < 0.01


def test_near_miss_single_swap_wins():
    parsed, analysis = _base()
    m = cf.near_miss(parsed, analysis)
    assert m["gradable"] and not m["won"]
    assert m["gap"] == 10.0 and m["n_shared"] == 2
    # only delta: your D (15) -> winner's C (25) = +10, NOT > gap (ties don't win)
    assert m["best_swap"]["out"] == "D" and m["best_swap"]["in"] == "C"
    assert m["best_swap"]["gain"] == 10.0
    assert m["best_swap"]["would_have_won"] is False  # +10 only ties
    assert m["swaps_needed"] is None  # even the full delta doesn't BEAT it


def test_near_miss_won():
    parsed, analysis = _base()
    analysis["user_lineups_df"].loc[0, "points"] = 100.0
    m = cf.near_miss(parsed, analysis)
    assert m["won"] is True


def test_not_gradable_without_user_lineups():
    parsed, _ = _base()
    assert cf.near_miss(parsed, {"user_lineups_df": None})["gradable"] is False


def test_md_renders():
    parsed, analysis = _base()
    md = cf.counterfactual_md(cf.winner_story(parsed), cf.near_miss(parsed, analysis))
    assert "How the winner was built" in md and "Near-miss" in md


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
