"""Salary/proj enrichment of the autopsy from still-loaded projections.

The autopsy never REQUIRES projections — these tests pin both sides:
proj_frame_for_autopsy builds a valid join frame, and analyze_contest's
all-players-matched guard keeps partial matches at None.
"""
import io

import pandas as pd

from src.autopsy import analyze_contest, parse_dk_results, proj_frame_for_autopsy


def _proj_df(rows):
    return pd.DataFrame(rows, columns=["name", "salary", "proj_points"])


def test_proj_frame_builds_norm_drops_zero_salary_and_dedupes():
    etr = _proj_df([
        ("Benjamin James", 7400, 62.5),
        ("Withdrawn Guy", 0, 0.0),          # ETR WD row — must drop
        ("Nicolai Højgaard", 8000, 70.0),   # accent — norm must fold
    ])
    other = _proj_df([
        ("Benjamin James", 7400, 60.0),     # dup across vendors — first wins
        ("Harry Hall", 7000, 56.0),
    ])
    out = proj_frame_for_autopsy([etr, other])
    assert out is not None
    assert "_norm" in out.columns
    norms = set(out["_norm"])
    assert "withdrawn guy" not in norms
    assert "nicolai hojgaard" in norms
    bj = out[out["_norm"] == "benjamin james"]
    assert len(bj) == 1 and float(bj.iloc[0]["proj_points"]) == 62.5


def test_proj_frame_none_when_nothing_usable():
    assert proj_frame_for_autopsy([]) is None
    assert proj_frame_for_autopsy([None, pd.DataFrame()]) is None
    assert proj_frame_for_autopsy([_proj_df([("A", 0, 1.0)])]) is None


def _standings_csv(players):
    lineup = " ".join(f"G {p}" for p in players)
    lines = ["Rank,EntryId,EntryName,TimeRemaining,Points,Lineup,,Player,Roster Position,%Drafted,FPTS"]
    for i, p in enumerate(players):
        entry = f"{i+1},{100+i},Opponent{i},0,{300-i},{lineup},,{p},G,10.0%,{80-i}"
        lines.append(entry)
    return io.BytesIO("\n".join(lines).encode())


def test_salary_used_fills_when_all_match_and_nulls_when_one_missing():
    players = ["Aaa Bbb", "Ccc Ddd", "Eee Fff", "Ggg Hhh", "Iii Jjj", "Kkk Lll"]
    parsed = parse_dk_results(_standings_csv(players))

    full = proj_frame_for_autopsy([_proj_df([(p, 7000, 60.0) for p in players])])
    analysis = analyze_contest(parsed, full, "golf")
    top = analysis["winners_df"].iloc[0]
    assert top["salary_used"] == 42000
    assert top["proj_total"] == 360.0
    assert analysis["winners_summary"]["salary_used_mean"] == 42000

    partial = proj_frame_for_autopsy([_proj_df([(p, 7000, 60.0) for p in players[:-1]])])
    analysis = analyze_contest(parsed, partial, "golf")
    assert analysis["winners_df"].iloc[0]["salary_used"] is None

    analysis = analyze_contest(parsed, None, "golf")
    assert analysis["winners_df"].iloc[0]["salary_used"] is None


def test_slate_defining_requires_a_real_score():
    """9/14/26 NFL SD: Emari Demercado (0.7 pts, 14.7% owned) sat in the top-20
    as a salary dump and rendered as 'slate-defining'. A definer must score at
    least the field's median player score."""
    # 12 entries; every winner holds Filler (low own, ~0 pts) and Definer
    # (low own, big score); the rest of the roster is chalk.
    chalk = ["Chalk One", "Chalk Two", "Chalk Three", "Chalk Four"]
    lineup = " ".join(f"G {p}" for p in chalk + ["Definer Guy", "Filler Guy"])
    lines = ["Rank,EntryId,EntryName,TimeRemaining,Points,Lineup,,Player,Roster Position,%Drafted,FPTS"]
    player_rows = [(p, "60.0%", 20.0) for p in chalk] + [
        ("Definer Guy", "5.0%", 30.0), ("Filler Guy", "5.0%", 0.7)]
    for i in range(12):
        p, own, fpts = player_rows[i] if i < len(player_rows) else ("", "", "")
        tail = f",,{p},G,{own},{fpts}" if p else ",,,,,"
        lines.append(f"{i+1},{100+i},Opp{i},0,{200-i},{lineup}{tail}")
    parsed = parse_dk_results(io.BytesIO("\n".join(lines).encode()))
    analysis = analyze_contest(parsed, None, "nfl")
    names = {d["name"] for d in analysis["slate_defining"]}
    assert "Definer Guy" in names
    assert "Filler Guy" not in names
