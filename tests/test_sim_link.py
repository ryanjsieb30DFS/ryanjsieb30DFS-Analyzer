"""Tests for the Sim → Analyzer bridge (entry-set hand-off + dupe correction)."""
import json

import src.sim_link as sl


def test_load_and_format_sim_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "_SIM_ENTRIES_DIR", tmp_path)
    payload = {
        "generated_at": "2026-07-26 10:00", "slug": "mma_se",
        "entries": [
            {"contest": "UFC $5K SE", "players": ["A Aa", "B Bb"], "salary": 49800,
             "win_pct": 0.8, "top1_pct": 3.2, "cash_pct": 24.0, "roi_pct": 12.0},
            {"contest": "UFC $2K 3-Max", "players": ["C Cc", "D Dd"], "salary": 50000},
        ],
    }
    (tmp_path / "mma_se.json").write_text(json.dumps(payload))
    loaded = sl.load_sim_entries("mma_se")
    assert loaded["entries"][0]["win_pct"] == 0.8
    text = sl.entries_as_grade_text(loaded)
    assert text == "A Aa, B Bb\nC Cc, D Dd"
    md = sl.sim_metrics_md(loaded)
    assert "UFC $5K SE" in md and "3.2%" in md
    assert sl.load_sim_entries("nascar") is None
    sl.clear_sim_entries("mma_se")
    assert sl.load_sim_entries("mma_se") is None


def test_dupe_correction_from_corpus(tmp_path, monkeypatch):
    sim_root = tmp_path / "simrepo"
    corpus_dir = sim_root / "data" / "field_corpus"
    corpus_dir.mkdir(parents=True)
    rows = []
    # Naive prediction = own_product * n_entries; observed = count.
    # ratio 0.05 in every evidence row -> correction 0.05.
    for cid in range(3):
        rows.append({"source_file": f"c{cid}.csv", "contest_id": str(cid),
                     "sport": "mma", "n_entries": 1000,
                     "top_dupe_evidence": [
                         {"count": 5, "own_product": 0.1},     # naive 100 -> 0.05
                         {"count": 2, "own_product": 0.04},    # naive 40  -> 0.05
                     ]})
    (corpus_dir / "field_concentration.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    monkeypatch.setattr(sl, "_dupe_cache", {})
    assert sl.dupe_correction("mma_se", 1000) == 0.05
    # Different band with no rows -> None (grader keeps the naive number).
    assert sl.dupe_correction("mma_se", 50_000) is None
    # Absent repo -> None.
    monkeypatch.setattr(sl, "_SIM_ROOT", tmp_path / "nope")
    monkeypatch.setattr(sl, "_dupe_cache", {})
    assert sl.dupe_correction("mma_se", 1000) is None
