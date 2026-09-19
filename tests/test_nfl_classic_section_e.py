"""ETR NFL Classic digest (9/12/26) Section E tool backlog — report-only reads
for nfl_classic: raw top-10 count column (only when a vendor ships it), the
ownership stress test on the framework's three checks, chalk-combo LINEUP
counts, the Grade-tab three-checks info line, and the IKB edit-count guard.
Plus Task B (9/14/26): the pool prompt on a synthetic 340-player board."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import analysis_runner as ar, grader, landscape, sim_link  # noqa: E402


def _nfl():
    rows = [
        # name, sal, own, proj, ceil, opp, team, pos
        ("Jared Goff", 6000, 19.0, 19.0, 30.0, "NO", "DET", "QB"),
        ("Jahmyr Gibbs", 8000, 59.5, 24.6, 40.6, "NO", "DET", "RB"),
        ("Amon-Ra St. Brown", 6500, 27.2, 20.5, 35.1, "NO", "DET", "WR"),
        ("Sam LaPorta", 5000, 9.0, 11.0, 21.0, "NO", "DET", "TE"),
        ("Chris Olave", 5500, 28.3, 15.0, 28.0, "@DET", "NO", "WR"),
        ("Tyler Shough", 5200, 12.7, 16.0, 26.0, "@DET", "NO", "QB"),
        ("Juwan Johnson", 3700, 16.8, 9.0, 18.0, "@DET", "NO", "TE"),
        ("Michael Mayer", 2900, 47.8, 8.0, 16.0, "@NE", "LV", "TE"),
        ("Josh Allen", 7000, 1.0, 19.7, 29.9, "@MIA", "BUF", "QB"),
        ("Tetairoa McMillan", 6100, 9.4, 14.8, 27.7, "CHI", "CAR", "WR"),
        ("Bijan Robinson", 7700, 10.2, 20.5, 33.9, "@PIT", "ATL", "RB"),
        ("Jets", 2500, 18.4, 7.3, 14.6, "@TEN", "NYJ", "DST"),
        ("Chase Brown", 7100, 8.3, 17.0, 29.9, "TB", "CIN", "RB"),
    ]
    return pd.DataFrame(rows, columns=["name", "salary", "ownership", "proj_points",
                                       "ceiling", "opponent", "team", "position"])


# ------------------------------------------------ item 1: raw top-10 count ----

def test_top10_column_absent_is_skipped_silently():
    df = _nfl()
    assert landscape.top10_count_column(df) is None
    assert "top10_count" not in landscape.leverage_table(df).columns
    assert "top10_count" not in landscape.chalk_summary(df).columns


def test_top10_column_present_rides_leverage_and_chalk_tables():
    df = _nfl().assign(**{"Top 10": 3})
    assert landscape.top10_count_column(df) == "Top 10"
    lev = landscape.leverage_table(df, top_n=5)
    assert "top10_count" in lev.columns and lev["top10_count"].iloc[0] == 3
    ch = landscape.chalk_summary(df)
    assert "top10_count" in ch.columns and ch["top10_count"].sum() == 3 * len(df)


# ------------------------------------------------ item 3: chalk-combo counts ----

def test_chalk_combo_counts_use_own_product_times_field():
    combos = landscape.chalk_combo_counts(_nfl(), 2450)
    top = combos[0]
    assert top["players"] == ["Jahmyr Gibbs", "Michael Mayer"]
    # same math the bundle prints: the rounded joint % × field (28.4% × 2,450 ≈ 696)
    assert top["expected_lineups"] == round(top["joint_pct"] / 100 * 2450) == 696
    assert top["field_size"] == 2450
    md = landscape.chalk_combo_counts_md(combos)
    assert "lineups** of the 2,450" in md
    # no declared field → count is None and the text says so
    none = landscape.chalk_combo_counts(_nfl(), None)
    assert none[0]["expected_lineups"] is None
    assert "declare a contest" in landscape.chalk_combo_counts_md(none)


# --------------------------------------------- item 2: ownership stress test ----

def test_stress_test_reports_threshold_flips_only():
    res = landscape.ownership_stress_test(_nfl(), 2450)
    assert res["scales"] == [0.8, 1.2]
    # stacks: top QBs by own (Goff 19, Shough 12.7) + their top-2 catchers
    assert res["stack"][0]["qb"] == "Jared Goff"
    assert [n for n, _ in res["stack"][0]["pieces"]] == ["Jared Goff", "Jahmyr Gibbs",
                                                          "Amon-Ra St. Brown"]
    # Shough 12.7 × 1.2 = 15.2 crosses the chalk line; Gibbs never changes tier
    flips = {(f["name"], f["scale"]) for f in res["stack_flips"]}
    assert ("Tyler Shough", 1.2) in flips
    assert not any(f["name"] == "Jahmyr Gibbs" for f in res["stack_flips"])
    # combo counts scale by k²
    top = res["combo"][0]
    assert top["expected_by_scale"][0.8] == round(0.595 * 0.8 * 0.478 * 0.8 * 2450)
    # differentiation: McMillan 9.4 leaves at ×1.2 (11.3); Bijan 10.2 joins at ×0.8 (8.2);
    # Chase Brown 8.3 stays under 10 at ×0.8 and must NOT read as a flip (ranking artifact)
    d = {(f["name"], f["scale"], f["change"]) for f in res["diff_flips"]}
    assert ("Tetairoa McMillan", 1.2, "leaves") in d
    assert ("Bijan Robinson", 0.8, "joins") in d
    assert not any(f["name"] == "Chase Brown" for f in res["diff_flips"])
    md = landscape.stress_test_md(res)
    assert "Check 1" in md and "Check 2" in md and "Check 3" in md
    assert "Tyler Shough" in md and "Tetairoa McMillan" in md
    assert "warn" not in md.lower() and "grade" not in md.lower()


def test_stress_test_without_positions_degrades_to_combo_and_diff():
    df = _nfl().drop(columns=["position", "team"])
    res = landscape.ownership_stress_test(df, 1000)
    assert res["stack"] == [] and res["stack_flips"] == []
    assert res["combo"] and res["diff_base"]
    assert landscape.ownership_stress_test(pd.DataFrame(), 1000)["combo"] == []


# --------------------------------------- item 4: Grade-tab three-checks line ----

def _cal(**over):
    base = {"slug": "nfl_classic", "sport": "nfl", "shark_own": None, "winners_own": None,
            "own_flag_above": None, "shark_leverage_pct": None, "fades": set(),
            "soft_fades": set(), "tiers": {}, "bottom_tier": None, "crowded": set(),
            "pairs": [], "field_size": 2450}
    base.update(over)
    return base


_LINEUP = ("QB Jared Goff, RB Jahmyr Gibbs, RB Chase Brown, WR Amon-Ra St. Brown, "
           "WR Chris Olave, WR Tetairoa McMillan, TE Michael Mayer, FLEX Sam LaPorta, DST Jets")


def test_parse_lineups_carries_position_team_opponent():
    lu = grader.parse_lineups(_LINEUP, _nfl())[0]
    assert not lu["unmatched"] and len(lu["players"]) == 9
    goff = next(p for p in lu["players"] if p["name"] == "Jared Goff")
    assert (goff["position"], goff["team"], goff["opponent"]) == ("QB", "DET", "NO")


def test_three_checks_pre_lock_line_is_info_and_never_costs_a_letter():
    lu = grader.parse_lineups(_LINEUP, _nfl())[0]
    g = grader.grade_lineup(lu, _cal())
    tc = g["three_checks"]
    assert tc["stack"][0] == {"name": "Jared Goff", "own": 19.0, "role": "QB"}
    roles = {s["name"]: s["role"] for s in tc["stack"]}
    assert roles == {"Jared Goff": "QB", "Jahmyr Gibbs": "stack", "Amon-Ra St. Brown": "stack",
                     "Sam LaPorta": "stack", "Chris Olave": "bring-back"}
    assert tc["combo"]["players"] == ["Jahmyr Gibbs", "Michael Mayer"]
    assert tc["combo"]["expected_lineups"] == 697  # 59.5% × 47.8% × 2,450, unrounded pair math
    assert tc["diff"] == {"name": "Chase Brown", "own": 8.3}
    flag = next(f for f in g["flags"] if f["code"] == "three_checks")
    assert flag["level"] == "info"
    assert "Three ownership checks (pre-lock" in flag["msg"]
    assert "never moves the grade" in flag["msg"]
    assert grader.letter_grade(g, _cal())["letter"] == "A"
    # slug-routed: NFL Showdown and golf never get the line
    g2 = grader.grade_lineup(lu, _cal(slug="nfl_sd"))
    assert not any(f["code"] == "three_checks" for f in g2["flags"])


def test_three_checks_post_lock_pass_fail():
    lu = grader.parse_lineups(_LINEUP, _nfl())[0]
    actual = {"jared goff": 15.0, "jahmyr gibbs": 50.0, "amon ra st brown": 20.0,
              "sam laporta": 5.0, "chris olave": 20.0,        # stack came in UNDER → pass
              "michael mayer": 60.0,                          # pair 50×60 > 59.5×47.8 → fail
              "chase brown": 14.8}                            # diff piece 8.3 → 14.8 → fail
    tc = grader.three_checks(lu["players"], 2450, actual_own=actual)
    assert tc["checked"] == 3 and tc["passed"] == 1
    assert tc["verdicts"]["stack"]["pass"] is True
    assert tc["verdicts"]["combo"]["pass"] is False
    assert tc["verdicts"]["diff"]["pass"] is False
    line = grader.three_checks_line(tc)
    assert "1 of 3 passed" in line and "PASS" in line and "FAIL" in line
    assert "Information only" in line


def test_three_checks_none_without_ownership():
    assert grader.three_checks([{"name": "X"}], 100) is None
    assert grader.three_checks_line(None) == ""


# ---------------------------------------------- item 5: IKB edit-count guard ----

def _sim_session(tmp_path, slug, work: pd.DataFrame, base: pd.DataFrame):
    d = tmp_path / "data" / "sessions"
    d.mkdir(parents=True)
    (d / f"{slug}.json").write_text(json.dumps({
        "schema": 3, "projections": work.to_csv(index=False),
        "proj_sources": [{"vendor": "ETR NFL Classic", "projections": base.to_csv(index=False)}],
    }))
    return tmp_path


def test_ikb_guard_counts_edits_against_the_vendor_file(tmp_path, monkeypatch):
    base = _nfl()
    work = base.copy()
    work.loc[work["name"] == "Jared Goff", "proj_points"] += 1.5
    work.loc[work["name"] == "Jahmyr Gibbs", "proj_points"] -= 3.0
    root = _sim_session(tmp_path, "nfl_classic", work, base)
    monkeypatch.setattr(sim_link, "sim_root", lambda: root)
    s = sim_link.ikb_edit_summary("nfl_classic")
    assert s["n_players"] == len(base) and s["n_edited"] == 2 and s["max_delta"] == 3.0
    assert s["edits"][0]["name"] == "Jahmyr Gibbs" and s["edits"][0]["delta"] == -3.0
    md = sim_link.ikb_md(s)
    assert "2 of 13 players changed" in md and "3.0 points" in md
    assert "over 2 points" in md and "10 players or fewer" in md
    assert "Information only" in md


def test_ikb_guard_no_edits_and_no_session(tmp_path, monkeypatch):
    base = _nfl()
    root = _sim_session(tmp_path, "nfl_classic", base.copy(), base)
    monkeypatch.setattr(sim_link, "sim_root", lambda: root)
    md = sim_link.ikb_md(sim_link.ikb_edit_summary("nfl_classic"))
    assert md.startswith("IKB check") and "none" in md
    assert sim_link.ikb_edit_summary("nfl_sd") is None       # no session for that slug
    assert sim_link.ikb_md(None) is None
    monkeypatch.setattr(sim_link, "sim_root", lambda: None)  # bridge absent
    assert sim_link.ikb_edit_summary("nfl_classic") is None


# ------------------------------------------- Task B: 340-player pool prompt ----

def _board_340():
    rows = []
    pos_cycle = ["QB", "RB", "RB", "WR", "WR", "WR", "TE", "DST"]
    for i in range(340):
        pos = pos_cycle[i % len(pos_cycle)]
        # 206 real projections (≥ 3.0), 134 under the line (mirrors Week 1's split)
        proj = 3.0 + (i % 25) if i < 206 else round((i % 30) / 10.0, 1)
        rows.append({"name": f"Player {i:03d}", "position": pos, "team": f"T{i % 28:02d}",
                     "opponent": f"T{(i + 1) % 28:02d}", "salary": 3000 + 20 * i,
                     "proj_points": proj, "ownership": round((i % 40) * 1.5, 1)})
    return pd.DataFrame(rows)


def test_task_b_prompt_auto_outs_134_and_asks_writeups_for_pooled_tiers_only(tmp_path):
    df = _board_340()
    ranked, out = ar.split_nfl_classic_pool(df, [])
    assert len(df) == 340 and len(ranked) == 206 and len(out) == 134
    assert (pd.to_numeric(out["proj_points"]) < ar.NFL_CLASSIC_POOL_MIN_PROJ).all()
    p = ar.build_player_pool_prompt(df, [], "note", "nfl_classic", "NFL Classic", "nfl",
                                    tmp_path / "pool.md", tmp_path / "bundle.md")
    assert "these 206 players, and ONLY these" in p
    assert "134 more players project under 3 DraftKings points" in p
    assert "134 auto-out players appear ONLY in the pasted out-of-the-pool tables" in p
    # write-ups for the pooled tiers only, capped at 35 words
    assert "Core / Good / Okay players ONLY" in p
    assert "Fade-tier players get NO numbered entry" in p
    assert "35 words TOTAL at most" in p
    assert "gets exactly one ranked entry" not in p
    # every ranked player is a line; no auto-out player is
    assert p.count("\n- Player ") == 206
    assert "- Player 300 —" not in p and "| out | Player 300 |" in p
    # the size that fits the 20-minute run (Week 1 real board: ~38k chars)
    assert 20_000 < len(p) < 80_000
