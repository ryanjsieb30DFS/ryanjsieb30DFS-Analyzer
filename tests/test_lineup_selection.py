"""Per-contest Claude picks: candidate slice, pick validation, schema v2."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import src.lineup_selection as ls  # noqa: E402


def _pool(n=200):
    """Synthetic columnar Sim pool with two contests whose metric orderings
    DISAGREE, so per-contest slices must differ."""
    players = [f"P{j}" for j in range(20)]
    rosters = [[players[(i + k) % 20] for k in range(6)] for i in range(n)]
    up = [float(i) for i in range(n)]           # rises with index
    down = [float(n - i) for i in range(n)]     # falls with index
    mid = [float(n - abs(i - n // 2)) for i in range(n)]
    c1 = {"label": "Big SE ($12)", "name": "Big SE", "contest_type": "se",
          "field_size": 588, "entry_fee": 12.0, "prize_pool": 5000.0,
          "my_entries": 1,
          "metrics": {"win_pct": up, "top1_pct": mid, "top10_pct": up,
                      "cash_pct": up, "roi_pct": up},
          "exp_dupes": [float(i % 9) for i in range(n)]}
    c2 = {"label": "Flat 3max ($5)", "name": "Flat 3max", "contest_type": "3max",
          "field_size": 30000, "entry_fee": 5.0, "prize_pool": 9000.0,
          "my_entries": 3,
          "metrics": {"win_pct": down, "top1_pct": down, "top10_pct": down,
                      "cash_pct": down, "roi_pct": down},
          "exp_dupes": None}
    return {
        "schema_version": 1, "slug": "nascar", "sport": "nascar",
        "pool_fp": "fp111", "pool_len": n, "lineup_size": 6,
        "rosters": rosters,
        "salary": [49000 + i for i in range(n)],
        "proj": [200.0 + i for i in range(n)],
        "avg_own": [5.0 + (i % 40) for i in range(n)],
        "ownership": {p: 10.0 + j for j, p in enumerate(players)},
        "contests": [c1, c2],
    }


def test_candidate_slice_deterministic_and_capped():
    pool = _pool()
    a = ls.candidate_slice(pool, pool["contests"][0])
    b = ls.candidate_slice(pool, pool["contests"][0])
    assert a == b
    assert 0 < len(a) <= 50
    for r in a:
        assert set(r) >= {"index", "roster", "roster_key", "salary", "proj",
                          "avg_own", "win_pct", "top1_pct", "cash_pct"}


def test_candidate_slice_uses_this_contests_metrics():
    pool = _pool()
    s1 = {r["index"] for r in ls.candidate_slice(pool, pool["contests"][0])}
    s2 = {r["index"] for r in ls.candidate_slice(pool, pool["contests"][1])}
    assert s1 != s2                      # opposite orderings -> different slices
    # Contest 2's metrics all FALL with index -> its slice lives at low indexes.
    assert min(s2) == 0


def test_candidate_slice_includes_top_metric_rows():
    pool = _pool()
    c1 = pool["contests"][0]
    idxs = {r["index"] for r in ls.candidate_slice(pool, c1)}
    assert 199 in idxs                   # top win_pct (rises with index)
    top1_best = max(range(200), key=lambda i: c1["metrics"]["top1_pct"][i])
    assert top1_best in idxs


def _slice_and_table(pool, contest):
    rows = ls.candidate_slice(pool, contest)
    picked = rows[0]
    players = ", ".join(picked["roster"])
    md = "\n".join([
        f"## Picks — {contest['label']}",
        "",
        "| pick | id | players | why |",
        "|---|---|---|---|",
        f"| 1 | {picked['index']} | {players} | steadiest ceiling |",
        "",
        "**Why these picks:** Best blend of first-place chance and floor.",
    ])
    return rows, picked, md


def test_parse_pick_valid():
    pool = _pool()
    rows, picked, md = _slice_and_table(pool, pool["contests"][0])
    out = ls.parse_pick(md, rows, my_entries=1)
    assert out["errors"] == []
    assert out["picks"] == [{"index": picked["index"],
                             "roster_key": picked["roster_key"]}]
    assert "Best blend" in out["why"]


def test_parse_pick_rejects_fabricated_id():
    pool = _pool()
    rows, picked, md = _slice_and_table(pool, pool["contests"][0])
    bad = md.replace(f"| 1 | {picked['index']} |", "| 1 | 99999 |")
    out = ls.parse_pick(bad, rows, my_entries=1)
    assert out["picks"] == [] and any("not in the candidate table" in e
                                      for e in out["errors"])


def test_parse_pick_rejects_modified_roster():
    pool = _pool()
    rows, picked, md = _slice_and_table(pool, pool["contests"][0])
    swapped = md.replace(picked["roster"][0], "Fabricated Guy", 1)
    out = ls.parse_pick(swapped, rows, my_entries=1)
    assert out["picks"] == [] and any("never modify a roster" in e
                                      for e in out["errors"])


def test_parse_pick_rejects_wrong_count_and_duplicates():
    pool = _pool()
    rows, picked, md = _slice_and_table(pool, pool["contests"][0])
    out = ls.parse_pick(md, rows, my_entries=3)     # table has 1, contest takes 3
    assert out["picks"] == [] and any("exactly 3" in e for e in out["errors"])
    # Duplicate id in the same table (row appended INSIDE the table).
    players = ", ".join(picked["roster"])
    dup_md = md.replace(
        f"| 1 | {picked['index']} | {players} | steadiest ceiling |",
        f"| 1 | {picked['index']} | {players} | steadiest ceiling |\n"
        f"| 2 | {picked['index']} | {players} | again |")
    out2 = ls.parse_pick(dup_md, rows, my_entries=2)
    assert any("picked twice" in e for e in out2["errors"])


def test_parse_pick_tolerates_column_reorder():
    pool = _pool()
    rows, picked, _ = _slice_and_table(pool, pool["contests"][0])
    players = ", ".join(f"{n} (12%)" for n in picked["roster"])  # own annotations ok
    md = "\n".join([
        "| players | why | id |",
        "|---|---|---|",
        f"| {players} | fine | {picked['index']} |",
    ])
    out = ls.parse_pick(md, rows, my_entries=1)
    assert out["errors"] == [] and out["picks"][0]["index"] == picked["index"]


def test_save_and_load_schema_v2(tmp_path, monkeypatch):
    monkeypatch.setattr(ls, "_SELECTION_DIR", tmp_path)
    pool = _pool()
    rows = ls.candidate_slice(pool, pool["contests"][0])
    data = ls.save_contest_pick("nascar", pool, "Big SE ($12)",
                                {"id": "ab12cd34"},
                                [{"index": rows[0]["index"],
                                  "roster_key": rows[0]["roster_key"]}],
                                "why text")
    assert data["schema_version"] == 2
    loaded = ls.load_selection("nascar")
    assert loaded["contests"]["Big SE ($12)"]["declared_contest_id"] == "ab12cd34"
    # A re-sent pool (new fingerprint) invalidates old picks on the next save.
    pool2 = dict(pool, pool_fp="fp222")
    data2 = ls.save_contest_pick("nascar", pool2, "Flat 3max ($5)", None,
                                 [{"index": 1, "roster_key": "x"}], None)
    assert list(data2["contests"]) == ["Flat 3max ($5)"]
    ls.clear_selection("nascar")
    assert ls.load_selection("nascar") is None


def test_load_selection_rejects_v1(tmp_path, monkeypatch):
    monkeypatch.setattr(ls, "_SELECTION_DIR", tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "nascar.json").write_text(json.dumps(
        {"schema_version": 1, "selections": {"X": {}}}))
    assert ls.load_selection("nascar") is None


def test_contest_file_key():
    assert ls.contest_file_key("Whatever", {"id": "ab12cd34"}) == "ab12cd34"
    k = ls.contest_file_key("NAS $6K Engine Block [Single Entry] (SE)", None)
    assert k == "nas-6k-engine-block-single-entry-se"
    assert ls.contest_file_key("", None) == "contest"


def test_match_contests_type_and_field_one_to_one():
    pool_contests = [
        {"label": "A (SE)", "contest_type": "se", "field_size": 1000},
        {"label": "B (20-Max)", "contest_type": "20max", "field_size": 50000},
    ]
    declared = [
        {"id": "d1", "name": "Big", "type": "20-Max", "field_size": 52000},
        {"id": "d2", "name": "Small", "type": "SE", "field_size": 950},
        {"id": "d3", "name": "Other", "type": "SE", "field_size": 990},
    ]
    m = ls.match_contests(pool_contests, declared)
    assert m["A (SE)"]["id"] in ("d2", "d3")
    assert m["B (20-Max)"]["id"] == "d1"
    assert m["A (SE)"]["id"] != m["B (20-Max)"]["id"]


def test_match_contests_field_size_tolerance():
    m = ls.match_contests(
        [{"label": "X", "contest_type": "se", "field_size": 1000}],
        [{"id": "d1", "name": "Far", "type": "SE", "field_size": 5000}])
    assert m["X"] is None


def test_as_declared_maps_sim_vocab():
    d = ls.as_declared({"label": "L (SE)", "contest_type": "se",
                        "field_size": 500, "my_entries": 1, "entry_fee": 5.0})
    assert d["type"] == "SE" and d["field_size"] == 500 and d["id"] is None


def test_slice_digest_contains_ids_and_context():
    pool = _pool()
    c = pool["contests"][0]
    rows = ls.candidate_slice(pool, c)
    md = ls.slice_digest_md("nascar", c["label"], c, {"payout_shape": "Top-heavy"},
                            rows, pool["ownership"])
    assert f"# Candidate lineups — {c['label']}" in md
    assert "payout shape Top-heavy" in md
    assert f"| {rows[0]['index']} |" in md
    assert "Pick ONLY from this table" in md
