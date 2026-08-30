"""picker_report separates the three chain links: POOL / SLICE / PICK."""
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.picker_check import check_history_dir, check_md, slate_rows  # noqa: E402


def _fake_slate(tmp_path):
    """One archived contest + its Sim scored pool. The pool's best lineup
    (699) beats the winning score (650); the slice holds it; the pick (500)
    does not. So: POOL yes, SLICE yes, PICK no, one table row above the pick."""
    hist = tmp_path / "analyzer" / "rules" / "mma_se" / "history" / "2026-08-29__ufc"
    hist.mkdir(parents=True)
    (hist / "lineup_selection.json").write_text(json.dumps({
        "schema_version": 2, "slug": "mma_se", "contests": {
            "UFC $4K SE (SE)": {
                "picked": [{"index": 7, "roster_key": "A|B|C|D|E|F"}],
                "declared_contest_id": "802d3167"}}}))
    (hist / "results.json").write_text(json.dumps({
        "date": "2026-08-29", "slate_label": "UFC X", "contests": [
            {"name": "UFC $4K SE", "best_percentile": 40.0,
             "source_file": "contest-standings-194357539.csv"}]}))
    (hist / "autopsy.json").write_text(json.dumps([
        {"contest_id": "194357539", "winning_score": "650.0"}]))
    (hist / "mma_se__802d3167_slice.md").write_text("\n".join([
        "# Candidate lineups",
        "| id | tie | salary | proj | cost | players |",
        "|---|---|---|---|---|---|",
        "| 7 |  | 50000 | 300 | — | A (10%), B (20%), C, D, E, F |",
        "| 9 |  | 49800 | 310 | — | G (5%), H, I, J, K, L |",
    ]))
    pools = tmp_path / "sim" / "rules" / "mma_se" / "scored_pools"
    pools.mkdir(parents=True)
    rows = [
        {"players": "A, B, C, D, E, F", "actual_score": 500.0},
        {"players": "G, H, I, J, K, L", "actual_score": 699.0},
        {"players": "M, N, O, P, Q, R", "actual_score": 300.0},
        {"players": "S, T, U, V, W, X", "actual_score": None},  # unmatched
    ]
    with gzip.open(pools / "MMA_contest_standings_194357539_2026_08_29__ff.json.gz",
                   "wt") as f:
        f.write(json.dumps(rows))
    return hist, tmp_path / "sim"


def test_slate_rows_separates_pool_slice_and_pick(tmp_path):
    hist, sim_root = _fake_slate(tmp_path)
    rows = slate_rows(hist, "mma_se", sim_root)
    assert len(rows) == 1
    r = rows[0]
    assert r["winning_score"] == 650.0
    assert r["pool_n"] == 3                      # the None-score row is out
    assert r["pool_held_winner"] and r["pool_max"] == 699.0
    assert r["pick_actual"] == 500.0 and not r["pick_won"]
    assert r["pick_pool_pctile"] == round(100 * 1 / 3, 1)   # beat only the 300
    # The shown table held the winner, one row above the pick — the 8/29
    # failure shape, now a counted number instead of an anecdote.
    assert r["slice_n"] == 2 and r["slice_held_winner"]
    assert r["n_slice_above_pick"] == 1


def test_slate_rows_skips_contests_missing_a_join_leg(tmp_path):
    """No scored pool, no autopsy winning score, or no logged result — the
    contest is silently unmeasurable, never a crash or a guessed number."""
    hist, sim_root = _fake_slate(tmp_path)
    (hist / "autopsy.json").write_text(json.dumps([]))   # winning score gone
    assert slate_rows(hist, "mma_se", sim_root) == []


def test_check_history_dir_persists_and_renders(tmp_path):
    """The autopsy-flow entry point: measurable slate -> rows + readable md
    naming the failure link; missing Sim repo -> empty with a note, never a
    crash inside Log Autopsy."""
    hist, sim_root = _fake_slate(tmp_path)
    data = check_history_dir(hist, "mma_se", sim_root=sim_root)
    assert data["schema_version"] == 1 and len(data["contests"]) == 1
    md = check_md(data)
    assert "was on the table" in md.lower()
    assert "outscored the pick" in md.lower()      # the 8/29 shape, counted
    missing = check_history_dir(hist, "mma_se", sim_root=tmp_path / "nowhere")
    assert missing["contests"] == [] and "not found" in (missing["note"] or "")
    assert "not measurable" in check_md(missing).lower()
