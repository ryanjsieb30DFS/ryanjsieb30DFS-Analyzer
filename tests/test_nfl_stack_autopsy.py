"""NFL Classic stack-centric autopsy (Phase 4, 9/14/26).

Synthetic DK Classic standings + a synthetic projections frame carrying
team / opponent / position. Pins: the per-lineup read, the field / top 1% /
top 20 / user distributions, the winner's shape in words, the not-gradable
path (no projections → no crash), the autopsy record + markdown block, the
archive file + results.jsonl summary, the shark-gap stack dimensions, the
process-trend line, and the review prompt's one-line pointer.
"""
import io
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import analysis_runner, history, shark_gap  # noqa: E402
from src import nfl_stack_autopsy as S  # noqa: E402
from src.autopsy import (analyze_contest, build_autopsy_record, parse_dk_results,  # noqa: E402
                         proj_frame_for_autopsy, record_md_summary)

# Two games: DET (Goff) vs NO, and BAL (Jackson) vs IND.
_PLAYERS = [
    # name, position, team, opponent
    ("Jared Goff", "QB", "DET", "NO"),
    ("Jahmyr Gibbs", "RB", "DET", "NO"),
    ("Amon-Ra St. Brown", "WR", "DET", "NO"),
    ("Sam LaPorta", "TE", "DET", "NO"),
    ("Chris Olave", "WR", "NO", "@DET"),
    ("Alvin Kamara", "RB", "NO", "@DET"),
    ("Lamar Jackson", "QB", "BAL", "IND"),
    ("Zay Flowers", "WR", "BAL", "IND"),
    ("Derrick Henry", "RB", "BAL", "IND"),
    ("Jonathan Taylor", "RB", "IND", "@BAL"),
    ("Michael Pittman Jr.", "WR", "IND", "@BAL"),
    ("Bills", "DST", "BUF", "NYJ"),
    ("Jets", "DST", "NYJ", "@BUF"),
    ("Garrett Wilson", "WR", "NYJ", "@BUF"),
    ("James Cook", "RB", "BUF", "NYJ"),
]


def _proj_df():
    df = pd.DataFrame(_PLAYERS, columns=["name", "position", "team", "opponent"])
    df["salary"] = 5000
    df["proj_points"] = 10.0
    return proj_frame_for_autopsy([df])


# Lineups as (slot, name) in DK's string order. FLEX positions are only
# knowable through the projections (the standings table lists them as FLEX).
_DOUBLE_BB = ("QB Jared Goff RB Jahmyr Gibbs RB Derrick Henry WR Amon-Ra St. Brown "
              "WR Chris Olave WR Zay Flowers TE Sam LaPorta FLEX Alvin Kamara DST Bills")
_SINGLE = ("QB Lamar Jackson RB James Cook RB Jonathan Taylor WR Zay Flowers "
           "WR Chris Olave WR Garrett Wilson TE Sam LaPorta FLEX Amon-Ra St. Brown DST Jets")
_NAKED_3RB = ("QB Lamar Jackson RB Jahmyr Gibbs RB Alvin Kamara WR Amon-Ra St. Brown "
              "WR Chris Olave WR Garrett Wilson TE Sam LaPorta FLEX James Cook DST Bills")


def _standings(rows):
    """rows: (rank, entry_name, lineup_str). Right half lists each player once."""
    lines = ["Rank,EntryId,EntryName,TimeRemaining,Points,Lineup,,Player,Roster Position,%Drafted,FPTS"]
    right = [(n, p) for n, p, _, _ in _PLAYERS]
    for i in range(max(len(rows), len(right))):
        left = ""
        if i < len(rows):
            rk, en, lu = rows[i]
            left = f"{rk},{1000+i},{en},0,{300-rk},{lu}"
        else:
            left = ",,,,,"
        r = f"{right[i][0]},{right[i][1]},10.0%,15.0" if i < len(right) else ",,,"
        lines.append(f"{left},,{r}")
    return io.BytesIO("\n".join(lines).encode())


def _rows(n_field=30):
    rows = [(1, "shark1", _DOUBLE_BB), (2, "shark1", _SINGLE),
            (3, "RyvlesGaming30 (1/3)", _NAKED_3RB), (4, "RyvlesGaming30 (2/3)", _DOUBLE_BB)]
    for rk in range(5, n_field + 1):
        rows.append((rk, f"opp{rk}", _SINGLE if rk % 2 else _NAKED_3RB))
    return rows


def test_read_lineup_counts_every_non_dst_teammate():
    lookup = S.build_lookup(None, _proj_df())
    rd = S.read_lineup(_DOUBLE_BB, lookup)
    assert rd["mates"] == 3 and rd["shape"] == "stack3plus"
    assert rd["bringback"] == 2                                   # Olave + Kamara (FLEX resolved via projections)
    assert rd["rb_count"] == 3                                    # Gibbs, Henry, Kamara (FLEX)
    assert rd["one_game_max"] == 6 and rd["one_game_key"] == "DET-NO"
    assert rd["dst_vs_qb"] is False
    words = S.shape_words(rd)
    assert words.startswith("Goff triple-plus stack (Gibbs, Brown, LaPorta)")
    assert "Olave, Kamara bring-backs" in words and "3 RBs" in words and "6 from DET-NO" in words


def test_read_lineup_single_and_naked_and_suffix_names():
    lookup = S.build_lookup(None, _proj_df())
    single = S.read_lineup(_SINGLE, lookup)
    assert single["shape"] == "stack1" and single["mates_names"] == ["Zay Flowers"]
    assert single["bringback_names"] == ["Jonathan Taylor"]
    assert "Taylor bring-back" in S.shape_words(single)
    naked = S.read_lineup(_NAKED_3RB, lookup)
    assert naked["shape"] == "naked" and naked["bringback"] == 0 and naked["rb_count"] == 3
    assert "no stack" in S.shape_words(naked) and "no bring-back" in S.shape_words(naked)
    # A FLEX player the projections do not know → the lineup is NOT guessed.
    assert S.read_lineup(_SINGLE.replace("FLEX Amon-Ra St. Brown", "FLEX Nobody Known"), lookup) is None


def test_stack_report_groups_winner_and_user():
    parsed = parse_dk_results(_standings(_rows()))
    rep = S.stack_report(parsed, _proj_df())
    assert rep["gradable"] and rep["n_graded"] == 30 and rep["n_field"] == 30
    g = rep["groups"]
    assert g["field"]["n"] == 30
    assert g["top1pct"]["n"] == 1 and g["top1pct"]["bringback_pct"] == 100.0
    assert g["top20"]["n"] == 20
    assert g["user"]["n"] == 2 and g["user"]["naked_pct"] == 50.0 and g["user"]["triple_plus_pct"] == 50.0
    assert g["user"]["three_rb_pct"] == 100.0
    assert rep["winner"]["entry_name"] == "shark1" and rep["winner"]["rank"] == 1
    assert rep["winner"]["words"].startswith("Goff triple-plus stack")
    assert [u["rank"] for u in rep["user_lineups"]] == [3, 4]
    summary = S.stack_summary(rep)
    assert "top 1%" in summary and "winner: Goff" in summary and "you:" in summary


def test_stack_report_not_gradable_without_projections():
    parsed = parse_dk_results(_standings(_rows(8)))
    rep = S.stack_report(parsed, None)
    assert rep["gradable"] is False and "projections" in rep["reason"]
    md = S.stack_md(rep, "x.csv")
    assert "Not gradable" in md and S.stack_summary(rep) is None
    # A frame with no team column is the same as none.
    no_team = pd.DataFrame({"name": ["Jared Goff"], "salary": [5000], "proj_points": [10.0]})
    assert S.stack_report(parsed, proj_frame_for_autopsy([no_team]))["gradable"] is False


def test_stack_md_defines_the_terms_and_lists_every_group():
    parsed = parse_dk_results(_standings(_rows()))
    md = S.stack_md(S.stack_report(parsed, _proj_df()), "c.csv")
    assert md.startswith("### Stack shapes — c.csv")
    assert "A bring-back is a player from the team the quarterback is playing against" in md
    for label in ("Whole field", "Top 1%", "Top 20", "Your entries"):
        assert label in md
    assert "rank 3:" in md and "rank 4:" in md
    assert "never a rule" in md


def test_analyze_contest_routes_by_slug_and_record_carries_the_block():
    parsed = parse_dk_results(_standings(_rows()))
    a = analyze_contest(parsed, _proj_df(), "nfl", slug="nfl_classic")
    assert a["stack_report"]["gradable"] and a["stack_lookup"]["jared goff"]["team"] == "DET"
    # NFL Showdown is a different game — never a stack read.
    sd = analyze_contest(parsed, _proj_df(), "nfl", slug="nfl_sd")
    assert sd["stack_report"] is None and sd["stack_lookup"] is None
    # No projections: the report exists, says not gradable, nothing crashes.
    bare = analyze_contest(parsed, None, "nfl", slug="nfl_classic")
    assert bare["stack_report"]["gradable"] is False

    rec = build_autopsy_record(
        ts="2026-09-14 10:00", contest_label="NFL Classic", slug="nfl_classic",
        sport="nfl", source_file="c.csv", parsed=parsed, analysis=a,
        proj_source=None, notes="", contest_id="1")
    json.dumps(rec)  # JSON-safe
    assert rec["stack_report"]["winner"]["words"].startswith("Goff")
    md = record_md_summary(rec)
    assert "### Stack shapes" in md and "bring-back" in md


def test_archive_writes_stack_report_json_and_results_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "_REPO_ROOT", tmp_path)
    (tmp_path / "rules" / "nfl_classic").mkdir(parents=True)
    parsed = parse_dk_results(_standings(_rows()))
    a = analyze_contest(parsed, _proj_df(), "nfl", slug="nfl_classic")
    rec = build_autopsy_record(
        ts="2026-09-14 10:00", contest_label="NFL Classic", slug="nfl_classic",
        sport="nfl", source_file="c.csv", parsed=parsed, analysis=a,
        proj_source=None, notes="", contest_id="1")
    hist = history.archive_slate(
        slug="nfl_classic", sport="nfl", contest_label="NFL Classic",
        slate_label="stack test", autopsy_records=[rec],
        roi_contests=[{"name": "C1", "type": "SE", "field_size": 30, "my_entries": 2,
                       "entry_fee": 5, "best_rank": 3, "best_percentile": 10.0}],
        proj_source=None)
    data = json.loads((hist / "stack_report.json").read_text())
    assert data[0]["source_file"] == "c.csv" and data[0]["gradable"]
    row = json.loads((hist / "results.json").read_text())
    assert row["stack_summary"].startswith("top 1%: double stack")
    ledger = history.load_results("nfl_classic")
    assert ledger[-1]["stack_summary"] == row["stack_summary"]
    # Every other sport: no file, None in the row.
    (tmp_path / "rules" / "mma_se").mkdir(parents=True)
    hist2 = history.archive_slate(
        slug="mma_se", sport="mma", contest_label="MMA", slate_label="plain",
        autopsy_records=[{"contest_id": "9"}],
        roi_contests=[{"name": "C", "type": "SE", "field_size": 5, "my_entries": 1,
                       "entry_fee": 1, "best_rank": 1, "best_percentile": 1.0}],
        proj_source=None)
    assert not (hist2 / "stack_report.json").exists()
    assert json.loads((hist2 / "results.json").read_text())["stack_summary"] is None


def test_process_trend_reads_the_stack_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "_REPO_ROOT", tmp_path)
    for i, s in enumerate(("top 1%: double stack 60.0% (n=5)", None)):
        history.append_results("nfl_classic", {
            "date": f"2026-09-{13 + i}", "best_percentile": 20.0,
            "stack_summary": s})
    block = history.process_trend_block("nfl_classic")
    assert "**Stack shapes**" in block and "2026-09-13: top 1%: double stack 60.0%" in block
    assert "2026-09-14" not in block.split("Stack shapes")[1]


def test_shark_gap_adds_stack_dimensions_for_classic_only():
    parsed = parse_dk_results(_standings(_rows()))
    a = analyze_contest(parsed, _proj_df(), "nfl", slug="nfl_classic")
    gap = shark_gap.shark_gap(parsed, ["shark1"], ["RyvlesGaming30"],
                              stack_lookup=a["stack_lookup"])
    assert gap["sharks"]["double_stack_pct"] == 50.0 and gap["sharks"]["bringback_pct"] == 100.0
    assert gap["user"]["double_stack_pct"] == 50.0 and gap["user"]["bringback_pct"] == 50.0
    dims = {d["dim"]: d for d in gap["deltas"]}
    assert dims["bringback_pct"]["delta"] == -50.0
    assert "bring-back" in dims["bringback_pct"]["label"]
    md = shark_gap.gap_md(gap)
    assert "double stack" in md
    # Without the lookup (every other sport) the keys never appear.
    plain = shark_gap.shark_gap(parsed, ["shark1"], ["RyvlesGaming30"])
    assert "double_stack_pct" not in plain["sharks"]
    assert not any(d["dim"] == "bringback_pct" for d in plain["deltas"])
    # gap_for_slug only forwards the lookup for nfl_classic.
    g_sd = shark_gap.gap_for_slug("nfl_sd", parsed, stack_lookup=a["stack_lookup"])
    assert "double_stack_pct" not in (g_sd.get("user") or {})


def test_review_prompt_points_at_the_stack_report_for_classic_only(tmp_path, monkeypatch):
    seen = {}

    def _fake_run(prompt, out_path, collateral=None, **kwargs):
        seen["prompt"] = prompt
        return {"ok": True, "error": None, "duration_s": 0.0, "cost_usd": None}

    monkeypatch.setattr(analysis_runner, "_run_claude", _fake_run)
    hist = tmp_path / "2026-09-13__wk1"
    hist.mkdir()
    analysis_runner.run_autopsy_review("nfl_classic", "NFL Classic", "nfl", hist_dir=hist)
    assert "stack_report.json" in seen["prompt"]
    assert "never as a rule" in seen["prompt"]
    analysis_runner.run_autopsy_review("nfl_sd", "NFL Showdown", "nfl", hist_dir=hist)
    assert "stack_report.json" not in seen["prompt"]
