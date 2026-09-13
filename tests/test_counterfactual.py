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


def test_no_salary_map_degrades_to_points_only():
    parsed, analysis = _base()
    m = cf.near_miss(parsed, analysis)
    assert m["salary_checked"] is False
    assert m["blocked_swap"] is None
    assert m["best_swap"]["out"] == "D" and m["best_swap"]["in"] == "C"


def test_over_cap_swap_is_blocked_not_recommended():
    # The Ventura→James shape: the points-best swap costs more than the cap
    # room left, so it must move to blocked_swap and best_swap must be None.
    parsed, analysis = _base()
    analysis["salary_map"] = {"a": 20000, "b": 20000, "d": 9800, "c": 11500}
    m = cf.near_miss(parsed, analysis)
    assert m["salary_checked"] is True
    assert m["best_swap"] is None
    assert m["blocked_swap"]["out"] == "D" and m["blocked_swap"]["in"] == "C"
    assert m["blocked_swap"]["over_cap_by"] == 1500  # 49800 - 9800 + 11500 - 50000
    assert m["swaps_needed"] is None
    md = cf.counterfactual_md(None, m)
    assert "did NOT fit under the $50K salary cap" in md
    assert "No single swap fits under the cap" in md


def test_feasible_swap_still_recommended_with_salaries():
    parsed, analysis = _base()
    analysis["salary_map"] = {"a": 20000, "b": 20000, "d": 9800, "c": 10000}
    m = cf.near_miss(parsed, analysis)
    assert m["salary_checked"] is True
    assert m["blocked_swap"] is None
    assert m["best_swap"]["out"] == "D" and m["best_swap"]["in"] == "C"
    md = cf.counterfactual_md(None, m)
    assert "that fits the cap" in md


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


def _classic_base(winner: str = "dst_swap"):
    """NFL Classic: your lineup vs the winner differs by DST (yours) → WR
    (theirs) and RB → RB. Only the RB swap keeps a legal roster."""
    mine = ["QB1", "RB1", "RB2", "WR1", "WR2", "WR3", "TE1", "RB3", "DST1"]
    theirs = ["QB1", "RB1", "RB2", "WR1", "WR2", "WR3", "TE1", "RB4", "DST1"]
    theirs_dst_swap = ["QB1", "RB1", "RB2", "WR1", "WR2", "WR3", "TE1", "RB3", "WR4"]
    win_roster = theirs_dst_swap if winner == "dst_swap" else theirs
    lineups = [
        {"Rank": 1, "EntryName": "shark (1/1)", "Points": 200.0,
         "Lineup_parsed": win_roster},
        {"Rank": 2, "EntryName": "me", "Points": 180.0, "Lineup_parsed": mine},
    ]
    pos = {"QB1": "QB", "RB1": "RB", "RB2": "RB", "RB3": "RB", "RB4": "RB",
           "WR1": "WR", "WR2": "WR", "WR3": "WR", "WR4": "WR", "TE1": "TE",
           "DST1": "DST"}
    fp = {"QB1": 25, "RB1": 20, "RB2": 18, "RB3": 5, "RB4": 30, "WR1": 20,
          "WR2": 15, "WR3": 12, "WR4": 40, "TE1": 10, "DST1": 8}
    players = [{"name": n, "actual_own": 10.0, "actual_fpts": float(v)}
               for n, v in fp.items()]
    analysis = {
        "user_lineups_df": pd.DataFrame([
            {"rank": 2, "entry_name": "me", "points": 180.0, "players": mine}]),
        "salary_map": {n.lower(): 5000 for n in pos},
        "position_map": {n.lower(): p for n, p in pos.items()},
    }
    return _parsed(lineups, players), analysis


def test_classic_roster_legal():
    assert cf.classic_roster_legal(
        ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "RB", "DST"])
    assert cf.classic_roster_legal(
        ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "TE", "DST"])
    assert not cf.classic_roster_legal(
        ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "WR", "WR"])   # no DST
    assert not cf.classic_roster_legal(
        ["QB", "QB", "RB", "WR", "WR", "WR", "TE", "RB", "DST"])  # two QB
    assert not cf.classic_roster_legal(["QB"] * 9)


def test_classic_illegal_position_swap_is_never_suggested():
    """The winner's only unique piece is a WR replacing your DST — a roster
    with no DST is not a swap. Even though it out-gains everything, it must
    not appear as best_swap, blocked_swap, or a swaps_needed count."""
    parsed, analysis = _classic_base()
    m = cf.near_miss(parsed, analysis)
    assert m["position_checked"] is True
    assert m["best_swap"] is None
    assert m["blocked_swap"] is None
    assert m["swaps_needed"] is None


def test_classic_legal_same_position_swap_still_found():
    # The RB4 lineup is the winner: RB3 → RB4 is legal.
    parsed, analysis = _classic_base(winner="rb_swap")
    m = cf.near_miss(parsed, analysis)
    assert m["position_checked"] is True
    assert m["best_swap"]["out"] == "RB3" and m["best_swap"]["in"] == "RB4"
    assert m["best_swap"]["would_have_won"] is True
    assert m["swaps_needed"] == 1
    assert "keeps a legal roster" in cf.counterfactual_md(None, m)


def test_no_position_map_means_no_position_gate():
    parsed, analysis = _classic_base()
    analysis.pop("position_map")
    m = cf.near_miss(parsed, analysis)
    assert m["position_checked"] is False
    assert m["best_swap"]["out"] == "DST1" and m["best_swap"]["in"] == "WR4"
