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


def test_dupe_correction_skips_golf_and_separates_showdown(tmp_path, monkeypatch):
    """Golf's corpus ratio spans three orders of magnitude (median ~70x at small
    field sizes, p90 ~5,760x), so a single median is not a usable multiplier for
    a pre-lock number — golf must fall back to the naive estimate. And RD4
    Showdown (6 golfers, tiny field) must never inherit a full-field PGA Classic
    factor, which it did until 7/25/26 via a shared "golf" key."""
    sim_root = tmp_path / "simrepo"
    corpus_dir = sim_root / "data" / "field_corpus"
    corpus_dir.mkdir(parents=True)
    rows = []
    for cid in range(3):
        # Golf rows with a WILDLY dispersed ratio — the real corpus shape.
        rows.append({"source_file": f"g{cid}.csv", "contest_id": f"g{cid}",
                     "sport": "golf", "n_entries": 1000,
                     "top_dupe_evidence": [
                         {"count": 500, "own_product": 0.001},   # naive 1 -> 500x
                         {"count": 3, "own_product": 0.1},       # naive 100 -> 0.03x
                     ]})
        rows.append({"source_file": f"n{cid}.csv", "contest_id": f"n{cid}",
                     "sport": "nascar", "n_entries": 1000,
                     "top_dupe_evidence": [{"count": 12, "own_product": 0.004}]})
    (corpus_dir / "field_concentration.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    monkeypatch.setattr(sl, "_dupe_cache", {})
    # Golf: corpus rows EXIST and are plentiful, and it still declines.
    assert sl.dupe_correction("pga_classic", 1000) is None
    assert sl.dupe_correction("pga_rd4_sd", 1000) is None
    # The two golf slugs no longer share a cache key with each other's sport.
    assert sl._SLUG_SPORT["pga_rd4_sd"] != sl._SLUG_SPORT["pga_classic"]
    # NASCAR still corrects: naive 4 -> observed 12 -> 3.0.
    assert sl.dupe_correction("nascar", 1000) == 3.0


def test_grade_labels_corrected_vs_naive_dupes():
    """A corpus-corrected dupe estimate and a raw independence one can differ
    several-fold; the pre-lock screen has to say which it is showing."""
    from src.grader import grade_md
    base = {"names": ["A", "B"], "flags": [], "avg_own": 20.0,
            "n_sub10": 1, "n_sub5": 0, "expected_dupes": 12.5}
    corrected = grade_md([{**base, "dupes_corrected": True, "dupes_factor": 3.1}], [], {})
    assert "corpus-corrected" in corrected and "3.1×" in corrected
    naive = grade_md([{**base, "dupes_corrected": False, "dupes_factor": None}], [], {})
    assert "raw independence estimate" in naive
    assert "corpus-corrected" not in naive


def test_capture_field_stats_and_dead_structure(tmp_path, monkeypatch):
    sim_root = tmp_path / "simrepo"
    d = sim_root / "rules" / "mma_se" / "slate_data"
    d.mkdir(parents=True)
    cap = {
        "slate_name": "UFC test", "slug": "mma_se",
        "players": [
            {"name": "A Aa", "opponent": "B Bb"},
            {"name": "B Bb", "opponent": "A Aa"},
            {"name": "C Cc", "opponent": "D Dd"},
            {"name": "D Dd", "opponent": "C Cc"},
        ],
        "field": {
            "player_index": ["A Aa", "B Bb", "C Cc", "D Dd"],
            # roster 0 = A+C (clean), roster 1 = A+B (DEAD: opponents)
            "rosters": [[0, 2], [0, 1]],
            "counts": [3, 1],
            "summary": {"n_entries": 4, "n_unique": 2, "unique_pct": 50.0,
                        "max_dupe": 3, "top_dupes": [3, 1],
                        "entries_per_user": {"pct_single": 100.0, "mean": 1.0},
                        "chalk_share": {"top3_lineup_pct": 25.0}},
        },
    }
    (d / "UFC_test.json").write_text(json.dumps(cap))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    stats = sl.capture_field_stats("mma_se", 4)
    assert stats["unique_pct"] == 50.0 and stats["max_dupe"] == 3
    # 1 of 4 entries rosters an opponent pair -> 25% dead structure.
    assert stats["dead_structure_pct"] == 25.0
    md = sl.capture_stats_md(stats)
    assert "dead structure" in md and "50%" in md
    # No capture with that entry count -> None.
    assert sl.capture_field_stats("mma_se", 999) is None


def test_capture_schema_drift_is_reported_not_misread(tmp_path, monkeypatch):
    """Captures carry schema_version but nothing read it: a newer capture whose
    block semantics changed would be parsed as v1 and produce quietly wrong
    numbers. Skip it AND say so — a degraded bridge must not look like a clean
    one."""
    sim_root = tmp_path / "simrepo"
    d = sim_root / "rules" / "mma_se" / "slate_data"
    d.mkdir(parents=True)
    (d / "future.json").write_text(json.dumps({
        "schema_version": 99, "slate_name": "future",
        "field": {"summary": {"n_entries": 500, "unique_pct": 50.0, "max_dupe": 9}},
    }))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    sl.capture_warnings.clear()
    assert sl.find_sim_capture("mma_se", 500) is None
    assert "newer build" in sl.capture_warnings["mma_se"]


def test_capture_matched_by_contest_id_over_entry_count(tmp_path, monkeypatch):
    """Two contests on one slate can have equal entry counts. contest_id wins;
    the count fallback fires only when UNAMBIGUOUS and never joins a capture
    known to belong to a different contest — a mis-join appends wrong capture_*
    fields to field_tendencies.jsonl permanently."""
    sim_root = tmp_path / "simrepo"
    d = sim_root / "rules" / "nascar" / "slate_data"
    d.mkdir(parents=True)
    for nm, cid in (("aaa_wrong", "111"), ("zzz_right", "222")):
        (d / f"{nm}.json").write_text(json.dumps({
            "schema_version": 1, "slate_name": nm, "contest_id": cid,
            "field": {"summary": {"n_entries": 490, "unique_pct": 60.0, "max_dupe": 4}},
        }))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    # With the id, the right one — tagged as an id match.
    got = sl.find_sim_capture("nascar", 490, contest_id="222")
    assert got["slate_name"] == "zzz_right"
    assert got["_match_method"] == "contest_id"
    # Count alone is AMBIGUOUS here (two 490-entry captures): None + warning,
    # never the alphabetically-first file.
    sl.capture_warnings.clear()
    assert sl.find_sim_capture("nascar", 490) is None
    assert "no contest id to disambiguate" in sl.capture_warnings["nascar"]
    # An id that matches nothing does NOT fall back onto captures that carry a
    # DIFFERENT id — those are known to be other contests.
    assert sl.find_sim_capture("nascar", 490, contest_id="999") is None


def test_capture_count_fallback_fires_when_unique_and_idless(tmp_path, monkeypatch):
    """A single id-less capture with the right entry count is still matched —
    the fallback exists for captures written before contest ids were stamped."""
    sim_root = tmp_path / "simrepo"
    d = sim_root / "rules" / "nascar" / "slate_data"
    d.mkdir(parents=True)
    (d / "legacy.json").write_text(json.dumps({
        "schema_version": 1, "slate_name": "legacy",
        "field": {"summary": {"n_entries": 490, "unique_pct": 60.0, "max_dupe": 4}},
    }))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    got = sl.find_sim_capture("nascar", 490, contest_id="999")
    assert got["slate_name"] == "legacy"
    assert got["_match_method"] == "entry_count"
    # And capture_field_stats surfaces the join quality.
    stats = sl.capture_field_stats("nascar", 490, contest_id="999")
    assert stats["match_method"] == "entry_count"


def test_dead_structure_absence_is_explained(tmp_path, monkeypatch):
    """`except: pass` made 'this capture is too old to carry opponents'
    indistinguishable from 'nothing to report'."""
    sim_root = tmp_path / "simrepo"
    d = sim_root / "rules" / "mma_se" / "slate_data"
    d.mkdir(parents=True)
    (d / "old.json").write_text(json.dumps({
        "schema_version": 1, "slate_name": "old",
        "players": [{"name": "A Fighter"}],          # no `opponent`
        "field": {"summary": {"n_entries": 500, "unique_pct": 55.0, "max_dupe": 7},
                  "player_index": ["A Fighter"], "rosters": [[0]], "counts": [3]},
    }))
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    sl.capture_warnings.clear()
    stats = sl.capture_field_stats("mma_se", 500)
    assert "dead_structure_pct" not in stats
    assert "opponent" in stats["dead_structure_note"]
    assert "can't be computed" in sl.capture_stats_md(stats)


def test_field_tendencies_reads_back_the_capture_keys(tmp_path, monkeypatch):
    """log_contest wrote capture_* keys that NOTHING read, so the capture
    bridge's stated goal — roster-level evidence in the field reads — was never
    actually implemented."""
    import src.field_tendencies as ft
    monkeypatch.setattr(ft, "_path", lambda slug: tmp_path / f"{slug}.jsonl")
    prof = {"gradable": True, "crowded_players": [{"name": "Chalk Guy"}],
            "crowded_combos": [], "fish_traps": [], "top_opponents": [],
            "winners_profile": {"avg_own_per_slot": 20.0, "unique_pct": 90.0},
            "fish_profile": {"avg_own_per_slot": 30.0}}
    for i, (cid, uniq) in enumerate([("c1", 22.0), ("c2", 26.0)]):
        ft.record("mma_se", "se", 31708, prof, f"2026-07-0{i+1}",
                  contest_name="UFC Milly", contest_id=cid,
                  sim_capture={"unique_pct": uniq, "max_dupe": 218,
                               "mean_entries_per_user": 20.4,
                               "dead_structure_pct": 12.5})
    s = ft.summarize_contest("mma_se", "UFC Milly")
    cap = s["capture_structure"]
    assert cap["unique_pct"] in (22.0, 26.0) and cap["unique_pct_n"] == 2
    assert cap["max_dupe"] == 218.0
    text = ft._crowd_traps_str(s)
    assert "unique rosters" in text and "218 times" in text
    assert "dead" in text
    # No captures at all -> silent, not a fabricated claim.
    ft.record("nascar", "se", 500, prof, "2026-07-01",
              contest_name="Cup Race", contest_id="n1")
    ft.record("nascar", "se", 500, prof, "2026-07-02",
              contest_name="Cup Race", contest_id="n2")
    s2 = ft.summarize_contest("nascar", "Cup Race")
    assert s2["capture_structure"] is None
    assert "unique rosters" not in ft._crowd_traps_str(s2)


def test_sim_metrics_md_survives_schema_drift():
    """A string/None metric from a drifted Sim schema renders as an em dash
    instead of raising TypeError inside the Grade tab."""
    payload = {"entries": [
        {"contest": "SE", "win_pct": "not-a-number", "top1_pct": None,
         "cash_pct": 40.0, "roi_pct": 12.0, "players": ["A"]},
    ]}
    md = sl.sim_metrics_md(payload)
    assert "—" in md and "40.0%" in md


def test_dupe_correction_tolerates_one_bad_corpus_line(tmp_path, monkeypatch):
    """One truncated line in the Sim's append-mode corpus must skip that line,
    not silently disable the correction for every contest."""
    sim_root = tmp_path / "simrepo"
    corpus = sim_root / "data" / "field_corpus" / "field_concentration.jsonl"
    corpus.parent.mkdir(parents=True)
    rows = [json.dumps({
        "sport": "mma", "n_entries": 1000,
        "top_dupe_evidence": [{"own_product": 0.001, "count": 4}],
    }) for _ in range(3)]
    corpus.write_text("\n".join(rows) + '\n{"sport": "mma", "n_entr')  # truncated tail
    monkeypatch.setattr(sl, "_SIM_ROOT", sim_root)
    sl._dupe_cache.clear()
    # naive = 0.001 * 1000 = 1; observed 4 -> factor 4.0 from the 3 good lines.
    assert sl.dupe_correction("mma_se", 1000) == 4.0


# ---------------------------------------------------------------------------
# Sim autopsy hand-off (standings copies + pool-vs-picking payloads, 8/3/26)
# ---------------------------------------------------------------------------

def test_list_sim_standings_reads_manifest_and_skips_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "_SIM_STANDINGS_DIR", tmp_path / "sim_standings")
    d = tmp_path / "sim_standings" / "pga_classic"
    d.mkdir(parents=True)
    (d / "contest-standings-1.csv").write_bytes(b"Rank\n1")
    (d / "manifest.json").write_text(json.dumps({"slug": "pga_classic", "files": [
        {"filename": "contest-standings-1.csv", "contest_id": "1",
         "slate_name": "S1", "scored_at": "2026-08-03 19:00"},
        {"filename": "gone.csv", "contest_id": "2",
         "slate_name": "S2", "scored_at": "2026-08-03 19:00"},
    ]}))
    rows = sl.list_sim_standings("pga_classic")
    assert len(rows) == 1                      # the missing file is dropped
    assert rows[0]["contest_id"] == "1"
    assert rows[0]["path"].endswith("contest-standings-1.csv")
    assert sl.list_sim_standings("nascar") == []


def test_load_sim_autopsy_and_md_and_clear(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "_SIM_STANDINGS_DIR", tmp_path / "sim_standings")
    monkeypatch.setattr(sl, "_SIM_AUTOPSY_DIR", tmp_path / "sim_autopsy")
    d = tmp_path / "sim_autopsy"
    d.mkdir()
    payload = {
        "slug": "pga_classic", "slate_name": "Rocket", "contest_id": "192834905",
        "user": {"n_entries": 21, "best_points": 507.5},
        "pool": {"n": 5000, "avg_actual": 391.0, "median_actual": 392.5,
                 "max_actual": 621.0, "n_beating_best_entry": 206,
                 "pct_beating_best_entry": 4.1, "picking_edge_points": 25.4},
        "rank_signal": [{"metric": "pre_sim_top1_pct", "label": "Top 1%", "n": 5000,
                         "spearman_vs_actual": -0.054, "top100_avg_actual": 365.1,
                         "pool_avg_actual": 391.0}],
    }
    (d / "pga_classic__192834905.json").write_text(json.dumps(payload))
    (d / "pga_classic__bad.json").write_text("{not json")   # tolerated, skipped
    loaded = sl.load_sim_autopsy("pga_classic")
    assert list(loaded) == ["192834905"]
    md = sl.sim_autopsy_md(loaded["192834905"])
    assert "5,000 lineups" in md and "621.0" in md
    assert "206" in md and "-0.054" in md
    assert "picking added points" in md          # positive edge phrasing
    assert sl.sim_autopsy_md({}) == ""
    # Clear removes both directions of the hand-off.
    sd = tmp_path / "sim_standings" / "pga_classic"
    sd.mkdir(parents=True)
    (sd / "x.csv").write_bytes(b"a")
    (sd / "manifest.json").write_text("{}")
    sl.clear_sim_handoff("pga_classic")
    assert sl.load_sim_autopsy("pga_classic") == {}
    assert sl.list_sim_standings("pga_classic") == []
