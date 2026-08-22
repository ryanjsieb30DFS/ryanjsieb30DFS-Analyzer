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
    assert 0 < len(a) <= 100
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


def test_pick_flow_is_sport_agnostic():
    """User directive 8/15/26: the per-contest pick flow must work for EVERY
    sport slug, not just golf. Slice -> digest -> parse_pick for each."""
    for slug in ("pga_classic", "pga_rd4_sd", "mma_se", "nascar"):
        pool = _pool()
        c = pool["contests"][0]
        rows = ls.candidate_slice(pool, c)
        assert rows, slug
        md = ls.slice_digest_md(slug, c["label"], c, None, rows, pool["ownership"])
        assert f"| {rows[0]['index']} |" in md, slug
        pick_md = (
            "## Picks — x\n\n| pick | id | players | why |\n|---|---|---|---|\n"
            f"| 1 | {rows[0]['index']} | {', '.join(rows[0]['roster'])} | t |"
        )
        parsed = ls.parse_pick(pick_md, rows, 1)
        assert len(parsed["picks"]) == 1, slug


def test_strategy_angle_seats_leverage_but_never_underweight():
    """A lineup carrying the strategy's named leverage candidates must make the
    slice even when it sims mid-pack. An UNDERWEIGHT name earns NO seat —
    8/15/26: seating them (and labelling them like an endorsement) is what put
    Van Gisbergen and Austin Dillon into both NASCAR picks."""
    pool = _pool()
    c = pool["contests"][0]
    # LevGuy (leverage) sits in lineup 60; UwGuy (underweight) sits alone in
    # lineup 61. Both are mid-pack, so only the strategy angle can seat them.
    pool["rosters"][60] = ["LevGuy", "UwGuy", "P0", "P1", "P2", "P3"]
    pool["rosters"][61] = ["UwGuy", "P4", "P5", "P6", "P7", "P8"]
    baseline = {r["index"] for r in ls.candidate_slice(pool, c)}
    assert 60 not in baseline and 61 not in baseline
    strat = {"leverage": ["LevGuy"], "underweight": ["UwGuy"]}
    rows = ls.candidate_slice(pool, c, strategy=strat)
    by_id = {r["index"]: r for r in rows}
    assert 60 in by_id                      # seated for its leverage name
    assert 61 not in by_id                  # underweight alone earns nothing
    # ...and where an underweight name rides along it is marked as a COST.
    assert "LevGuy" in by_id[60]["strategy"]
    assert "⚠ UwGuy (UNDERWEIGHT)" in by_id[60]["strategy"]
    md = ls.slice_digest_md("mma_se", c["label"], c, None, rows, pool["ownership"])
    assert "⚠ UwGuy (UNDERWEIGHT)" in md and "| strategy |" in md


def test_strategy_names_normalization():
    assert ls._strat_norm("J.T. Poston") == ls._strat_norm("JT Poston")
    assert ls._strat_norm("Robert Macintyre") == ls._strat_norm("Robert MacIntyre")


# ---------------------------------------------------------------------------
# One lineup, one contest (user directive 8/15/26, all sports)
# ---------------------------------------------------------------------------

def test_taken_roster_keys_excludes_own_contest_and_stale_pools(tmp_path,
                                                                monkeypatch):
    monkeypatch.setattr(ls, "_SELECTION_DIR", tmp_path)
    pool = _pool()
    rows = ls.candidate_slice(pool, pool["contests"][0])
    ls.save_contest_pick("nascar", pool, "Big SE ($12)", None,
                         [{"index": rows[0]["index"],
                           "roster_key": rows[0]["roster_key"]}], None)
    # Seen from the OTHER contest: that roster is taken.
    taken = ls.taken_roster_keys("nascar", pool, exclude_label="Flat 3max ($5)")
    assert taken == {rows[0]["roster_key"]: "Big SE ($12)"}
    # Seen from its OWN contest: re-picking it is always allowed.
    assert ls.taken_roster_keys("nascar", pool,
                                exclude_label="Big SE ($12)") == {}
    # A re-sent pool makes the old picks stale — they block nothing.
    assert ls.taken_roster_keys("nascar", dict(pool, pool_fp="fp999"),
                                exclude_label="Flat 3max ($5)") == {}


def test_taken_roster_keys_rebuilds_missing_key_from_pool(tmp_path, monkeypatch):
    """A pick row saved without roster_key still blocks — the roster is
    rebuilt from the pool at that index."""
    monkeypatch.setattr(ls, "_SELECTION_DIR", tmp_path)
    pool = _pool()
    ls.save_contest_pick("nascar", pool, "Big SE ($12)", None,
                         [{"index": 7}], None)
    taken = ls.taken_roster_keys("nascar", pool, exclude_label="Flat 3max ($5)")
    assert taken == {"|".join(sorted(pool["rosters"][7])): "Big SE ($12)"}


def test_candidate_slice_drops_taken_lineups_by_roster():
    """The slice never offers a lineup already picked elsewhere — and drops
    every pool index holding those SAME players, not just the picked one."""
    pool = _pool()
    c = pool["contests"][0]
    base = ls.candidate_slice(pool, c)
    victim = base[0]
    twins = {i for i, r in enumerate(pool["rosters"])
             if "|".join(sorted(map(str, r))) == victim["roster_key"]}
    assert len(twins) > 1                      # the synthetic pool repeats rosters
    cut = ls.candidate_slice(pool, c, taken={victim["roster_key"]: "Other SE"})
    idxs = {r["index"] for r in cut}
    assert not (idxs & twins)
    # Still a full, usable slice — the freed seats backfill from the next-best
    # eligible rows rather than leaving holes.
    assert len(cut) >= len(base) - 1
    assert len(cut) > 50


def test_parse_pick_rejects_lineup_taken_by_another_contest():
    pool = _pool()
    rows, picked, md = _slice_and_table(pool, pool["contests"][0])
    out = ls.parse_pick(md, rows, my_entries=1,
                        taken={picked["roster_key"]: "Flat 3max ($5)"})
    assert out["picks"] == []
    assert any("only be picked once" in e and "Flat 3max ($5)" in e
               for e in out["errors"])


def test_parse_pick_rejects_same_roster_at_two_ids():
    """Different ids, identical players — one lineup picked twice."""
    pool = _pool()
    rows = ls.candidate_slice(pool, pool["contests"][0])
    by_key: dict = {}
    for r in rows:
        by_key.setdefault(r["roster_key"], []).append(r)
    twins = next(v for v in by_key.values() if len(v) > 1)
    a, b = twins[0], twins[1]
    md = "\n".join([
        "| pick | id | players | why |",
        "|---|---|---|---|",
        f"| 1 | {a['index']} | {', '.join(a['roster'])} | one |",
        f"| 2 | {b['index']} | {', '.join(b['roster'])} | same six players |",
    ])
    out = ls.parse_pick(md, rows, my_entries=2)
    assert out["picks"] == []
    assert any("same players as id" in e for e in out["errors"])


# ---------------------------------------------------------------------------
# The strategy gate — picks must FOLLOW the slate strategy (8/15/26)
# ---------------------------------------------------------------------------

def _contract(tmp_path, monkeypatch, **over):
    """Write a strategy contract and point the module at it."""
    monkeypatch.setattr(ls, "_CONTRACT_DIR", tmp_path)
    tmp_path.mkdir(parents=True, exist_ok=True)
    payload = {
        "calls": [{"name": "FadeGuy", "verdict": "fade"},
                  {"name": "LeanGuy", "verdict": "lean_fade"},
                  {"name": "UwGuy", "verdict": "underweight"}],
        "leverage_candidates": [{"name": "LevGuy"}],
        "board": [{"name": "CoreA", "tier": "Core"}, {"name": "CoreB", "tier": "Core"},
                  {"name": "CoreC", "tier": "Core"}, {"name": "MidGuy", "tier": "Good"}],
        "chalk_pairs": [{"players": ["ChalkA", "ChalkB"], "joint_pct": 21.5}],
    }
    payload.update(over)
    (tmp_path / "nascar.json").write_text(json.dumps(payload))
    return ls.strategy_gate("nascar")


def test_strategy_gate_reads_every_rule(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    assert gate["has_contract"]
    assert sorted(n for n, _v in gate["fade"].values()) == ["FadeGuy", "LeanGuy"]
    assert list(gate["underweight"].values()) == ["UwGuy"]
    assert list(gate["leverage"].values()) == ["LevGuy"]
    assert sorted(gate["core"].values()) == ["CoreA", "CoreB", "CoreC"]
    assert gate["chalk_pair"] == ["ChalkA", "ChalkB"]


def test_compliance_names_each_broken_rule(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    ok = ["CoreA", "CoreB", "LevGuy", "MidGuy", "X1", "X2"]
    assert ls.compliance(ok, gate) == []
    # A fade call.
    assert any("FADE" in v for v in ls.compliance(
        ["CoreA", "CoreB", "LevGuy", "FadeGuy", "X1", "X2"], gate))
    # A lean fade reads as LEAN FADE, not FADE.
    assert any("LEAN FADE" in v for v in ls.compliance(
        ["CoreA", "CoreB", "LevGuy", "LeanGuy", "X1", "X2"], gate))
    # An underweight call.
    assert any("UNDERWEIGHT" in v for v in ls.compliance(
        ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"], gate))
    # No leverage piece.
    assert any("leverage list" in v for v in ls.compliance(
        ["CoreA", "CoreB", "MidGuy", "X1", "X2", "X3"], gate))
    # Only one Core anchor — the exact miss in the 8/15 Rainbow Warrior pick.
    assert any("Core-tier" in v for v in ls.compliance(
        ["CoreA", "MidGuy", "LevGuy", "X1", "X2", "X3"], gate))
    # Both halves of the most-duplicated pair.
    assert any("duplicated pair" in v for v in ls.compliance(
        ["CoreA", "CoreB", "LevGuy", "ChalkA", "ChalkB", "X2"], gate))


def test_compliance_respects_relaxations(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    uw = ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"]
    assert ls.compliance(uw, gate) != []
    assert ls.compliance(uw, gate, relaxed=("underweight",)) == []
    # A FADE never relaxes, whatever is passed.
    fade = ["CoreA", "CoreB", "LevGuy", "FadeGuy", "X1", "X2"]
    assert ls.compliance(fade, gate, relaxed=ls._RELAX_ORDER) != []


def test_eligible_indexes_filters_and_relaxes_in_order(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    good = ["CoreA", "CoreB", "LevGuy", "MidGuy", "X1", "X2"]
    uw = ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"]
    bad = ["MidGuy", "FadeGuy", "X1", "X2", "X3", "X4"]
    pool = {"rosters": [good] * 30 + [uw] * 30 + [bad] * 30}
    elig = ls.eligible_indexes(pool, gate)
    assert elig["relaxed"] == [] and elig["full"] == 30
    assert elig["allowed"] == set(range(30))
    # Too few clean rows -> underweight is dropped FIRST, and reported.
    pool2 = {"rosters": [good] * 3 + [uw] * 40 + [bad] * 10}
    elig2 = ls.eligible_indexes(pool2, gate)
    assert elig2["relaxed"] == ["underweight"]
    assert len(elig2["allowed"]) == 43
    # The fade rows stay out even then.
    assert not (elig2["allowed"] & set(range(43, 53)))


def test_no_contract_gates_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(ls, "_CONTRACT_DIR", tmp_path / "missing")
    gate = ls.strategy_gate("nascar")
    assert gate["has_contract"] is False
    assert ls.compliance(["Anyone"], gate) == []
    elig = ls.eligible_indexes({"rosters": [["a"], ["b"]]}, gate)
    assert elig["allowed"] == {0, 1} and elig["relaxed"] == []


def test_candidate_slice_only_offers_compliant_rows(tmp_path, monkeypatch):
    """The gate is upstream of every angle: no sim score can promote a lineup
    the strategy ruled out, and the slice still fills up."""
    gate = _contract(tmp_path, monkeypatch)
    pool = _pool()
    c = pool["contests"][0]
    # Make the pool's very BEST sim rows strategy-illegal, the rest legal.
    for i in range(len(pool["rosters"])):
        if i >= 180:                      # top of contest 1's rising metrics
            pool["rosters"][i] = ["CoreA", "CoreB", "LevGuy", "FadeGuy", "X1", "X2"]
        else:
            pool["rosters"][i] = ["CoreA", "CoreB", "LevGuy", f"M{i}", "X1", "X2"]
    elig = ls.eligible_indexes(pool, gate)
    rows = ls.candidate_slice(pool, c, allowed=elig["allowed"])
    assert rows and all(r["index"] < 180 for r in rows)
    assert all(ls.compliance(r["roster"], gate) == [] for r in rows)
    assert len(rows) > 50                 # a real choice, not a rump table


def test_parse_pick_rejects_a_pick_that_breaks_the_strategy(tmp_path, monkeypatch):
    """Defense in depth: even handed a slice row, a non-compliant pick saves
    nothing and the broken rule is named."""
    gate = _contract(tmp_path, monkeypatch)
    row = {"index": 42, "roster": ["CoreA", "MidGuy", "UwGuy", "X1", "X2", "X3"],
           "roster_key": "|".join(sorted(["CoreA", "MidGuy", "UwGuy",
                                          "X1", "X2", "X3"]))}
    md = "\n".join(["| pick | id | players | why |", "|---|---|---|---|",
                    "| 1 | 42 | " + ", ".join(row["roster"]) + " | best sim row |"])
    out = ls.parse_pick(md, [row], my_entries=1, gate=gate)
    assert out["picks"] == []
    assert any("does not follow the slate strategy" in e for e in out["errors"])
    assert any("UNDERWEIGHT" in e and "Core-tier" in e for e in out["errors"])


def test_gate_summary_is_plain_language(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    elig = {"allowed": set(range(5)), "relaxed": ["underweight"],
            "full": 3, "total": 100}
    md = ls.gate_summary(gate, elig)
    assert "FADE or LEAN FADE" in md and "FadeGuy" in md
    assert "Core-tier" in md and "ChalkA" in md
    assert "3 of 100" in md
    assert "⚠️" in md and "underweight" in md      # the relaxation is announced
    # A dropped rule is not advertised as enforced.
    assert "no player the strategy called UNDERWEIGHT" not in md


# ---------------------------------------------------------------------------
# Two opinions per contest (8/22/26): how much the Sim's diversified set and
# this repo's own pick agree. Agreement is a signal, never a conflict.
# ---------------------------------------------------------------------------

def test_roster_key_is_order_insensitive_and_raw():
    assert ls.roster_key(["B", "A", "C"]) == "A|B|C"
    # RAW on purpose — this key is persisted and read back, so it must NOT
    # normalize (that would orphan every pick already on disk).
    assert ls.roster_key(["José Aldo Jr."]) == "José Aldo Jr."


def test_compare_sets_counts_the_overlap():
    sim = [["A", "B"], ["C", "D"], ["E", "F"]]
    claude = [["B", "A"], ["G", "H"]]           # 1 shared, order shuffled
    r = ls.compare_sets(sim, claude)
    assert r["n_sim"] == 3 and r["n_claude"] == 2
    assert r["n_match"] == 1 and r["matched"] == {ls.match_key(["A", "B"])}


def test_compare_sets_full_and_zero_overlap():
    same = [["A", "B"], ["C", "D"]]
    assert ls.compare_sets(same, list(reversed(same)))["n_match"] == 2
    assert ls.compare_sets(same, [["X", "Y"]])["n_match"] == 0
    # One side empty (nothing picked yet / nothing sent yet).
    assert ls.compare_sets(same, [])["n_match"] == 0
    assert ls.compare_sets([], [])["n_sim"] == 0


def test_compare_sets_survives_a_spelling_difference():
    """The two sides come from the same pool, but a name that reaches the
    Analyzer differently spelled must not fake a disagreement."""
    r = ls.compare_sets([["José Aldo Jr.", "Song Yadong"]],
                        [["Jose Aldo", "Song Yadong"]])
    assert r["n_match"] == 1
