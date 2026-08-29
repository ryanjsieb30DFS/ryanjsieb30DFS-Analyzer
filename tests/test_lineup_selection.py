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
    assert 0 < len(a) <= ls._SLICE_CAP == 500
    for r in a:
        assert set(r) >= {"index", "roster", "roster_key", "salary", "proj",
                          "avg_own", "win_pct", "top1_pct", "cash_pct"}


def test_candidate_slice_uses_this_contests_metrics():
    # Explicit k: the 200-row fixture is smaller than _SLICE_CAP (500), so an
    # uncapped slice is the whole pool and the two contests cannot differ.
    pool = _pool()
    s1 = {r["index"] for r in ls.candidate_slice(pool, pool["contests"][0], k=50)}
    s2 = {r["index"] for r in ls.candidate_slice(pool, pool["contests"][1], k=50)}
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
    # Explicit k so the cap binds — otherwise every row is seated anyway and
    # the strategy angle proves nothing.
    baseline = {r["index"] for r in ls.candidate_slice(pool, c, k=40)}
    assert 60 not in baseline and 61 not in baseline
    strat = {"leverage": ["LevGuy"], "underweight": ["UwGuy"]}
    rows = ls.candidate_slice(pool, c, k=40, strategy=strat)
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
    base = ls.candidate_slice(pool, c, k=100)
    victim = base[0]
    twins = {i for i, r in enumerate(pool["rosters"])
             if "|".join(sorted(map(str, r))) == victim["roster_key"]}
    assert len(twins) > 1                      # the synthetic pool repeats rosters
    cut = ls.candidate_slice(pool, c, k=100,
                             taken={victim["roster_key"]: "Other SE"})
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
    # An underweight call is NOT a break (8/28/26 — soft rule): it lands in
    # soft_notes, never in compliance, so it can no longer reject a pick or
    # delete a pool branch (the 8/23 Clinch-winner bug).
    uw_roster = ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"]
    assert ls.compliance(uw_roster, gate) == []
    assert any("UNDERWEIGHT" in v for v in ls.soft_notes(uw_roster, gate))
    assert ls.soft_notes(["CoreA", "CoreB", "LevGuy", "X1", "X2", "X3"],
                         gate) == []
    # Carrying no leverage-list player is NOTHING — not a break, and not
    # even a soft cost (8/28/26, user directive). The list is an ownership
    # screen, not a call the strategy made, so the gate must be silent.
    no_lev = ["CoreA", "CoreB", "MidGuy", "X1", "X2", "X3"]
    assert ls.compliance(no_lev, gate) == []
    assert ls.soft_notes(no_lev, gate) == []
    # Only one Core anchor — the exact miss in the 8/15 Rainbow Warrior pick.
    assert any("Core-tier" in v for v in ls.compliance(
        ["CoreA", "MidGuy", "LevGuy", "X1", "X2", "X3"], gate))
    # Both halves of the most-duplicated pair.
    assert any("duplicated pair" in v for v in ls.compliance(
        ["CoreA", "CoreB", "LevGuy", "ChalkA", "ChalkB", "X2"], gate))


def test_compliance_respects_relaxations(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    # A FADE never relaxes, whatever is passed.
    fade = ["CoreA", "CoreB", "LevGuy", "FadeGuy", "X1", "X2"]
    assert ls.compliance(fade, gate, relaxed=ls._RELAX_ORDER) != []
    # "underweight" and "leverage" are not in the relax order at all — they
    # are not hard rules (both demoted to soft, 8/28/26).
    assert "underweight" not in ls._RELAX_ORDER
    assert "leverage" not in ls._RELAX_ORDER


def test_eligible_indexes_prices_instead_of_filtering(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    good = ["CoreA", "CoreB", "LevGuy", "MidGuy", "X1", "X2"]
    uw = ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"]
    bad = ["MidGuy", "FadeGuy", "X1", "X2", "X3", "X4"]
    # UNDERWEIGHT rows pass the gate from the start (8/28/26 soft rule) — the
    # 8/23 bug was exactly this pool shape: the winner sat in the uw branch.
    pool = {"rosters": [good] * 30 + [uw] * 30 + [bad] * 30}
    elig = ls.eligible_indexes(pool, gate)
    # 8/29/26 — THE STRATEGY IS A GUIDE, NOT A GATE. Nothing is filtered out.
    assert elig["allowed"] == set(range(90))
    assert elig["relaxed"] == []
    # `full`/`clean` still report who breaks NO rule — the honest headline and
    # the denominator the override log is read against.
    assert elig["full"] == 60 and elig["clean"] == set(range(60))
    # The fade rows are PRESENT and PRICED, not deleted.
    assert set(range(60, 90)) <= elig["allowed"]
    assert "\u203c" in ls.cost_tag(bad, gate)
    assert ls.cost_tag(good, gate) is None
    assert ls.cost_tag(uw, gate).startswith("\u26a0")
    # A pool where every row breaks a rule is fully pickable — the old code
    # relaxed rules here, which read as "thin pool" and hid the real cost.
    thin = {"rosters": [["CoreA", "MidGuy", "LevGuy", "X1", "X2", "X3"]] * 30}
    elig3 = ls.eligible_indexes(thin, gate)
    assert elig3["relaxed"] == [] and len(elig3["allowed"]) == 30
    assert elig3["full"] == 0


def test_no_contract_gates_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(ls, "_CONTRACT_DIR", tmp_path / "missing")
    gate = ls.strategy_gate("nascar")
    assert gate["has_contract"] is False
    assert ls.compliance(["Anyone"], gate) == []
    elig = ls.eligible_indexes({"rosters": [["a"], ["b"]]}, gate)
    assert elig["allowed"] == {0, 1} and elig["relaxed"] == []


def test_candidate_slice_offers_rule_breakers_with_a_price(tmp_path, monkeypatch):
    """8/29/26 reversal: a lineup that breaks the strategy REACHES the table
    carrying its cost. The old hard gate deleted both 8/29 MMA contest winners
    over one LEAN FADE call before anyone could look at them."""
    gate = _contract(tmp_path, monkeypatch)
    pool = _pool()
    c = pool["contests"][0]
    for i in range(len(pool["rosters"])):
        if i >= 180:                      # top of contest 1's rising metrics
            pool["rosters"][i] = ["CoreA", "CoreB", "LevGuy", "FadeGuy", "X1", "X2"]
        else:
            pool["rosters"][i] = ["CoreA", "CoreB", "LevGuy", f"M{i}", "X1", "X2"]
    elig = ls.eligible_indexes(pool, gate)
    rows = ls.candidate_slice(pool, c, allowed=elig["allowed"], gate=gate)
    idxs = {r["index"] for r in rows}
    assert any(i >= 180 for i in idxs)            # faded rows are ON the table
    assert any(i < 180 for i in idxs)             # so are the clean ones
    costed = [r for r in rows if r["index"] >= 180]
    assert costed and all("FadeGuy" in (r["cost"] or "") for r in costed)
    assert all(r["cost"] is None for r in rows if r["index"] < 180)


def _override_md(row, why):
    return "\n".join([
        "| pick | id | players |", "|---|---|---|",
        "| 1 | %d | %s |" % (row["index"], ", ".join(row["roster"])),
        "", "**Why**: " + why])


def _fade_row():
    roster = ["CoreA", "MidGuy", "FadeGuy", "X1", "X2", "X3"]
    return {"index": 42, "roster": roster, "roster_key": "|".join(sorted(roster))}


def test_parse_pick_allows_an_EXPLAINED_strategy_override(tmp_path, monkeypatch):
    """8/29/26: breaking a rule is an OVERRIDE, not an error — provided the
    why names the player and the rule. The strategy is a guide; the written
    reasoning is the price of departing from it."""
    gate = _contract(tmp_path, monkeypatch)
    row = _fade_row()
    out = ls.parse_pick(
        _override_md(row, "Taking FadeGuy against the strategy's fade — he is "
                          "the only path to a winning score here, and the "
                          "lineup runs one Core anchor on purpose."),
        [row], my_entries=1, gate=gate)
    assert out["errors"] == []
    assert out["picks"][0]["index"] == 42
    assert out["picks"][0]["override"]          # recorded, never hidden


def test_parse_pick_rejects_a_SILENT_strategy_override(tmp_path, monkeypatch):
    """An unexplained break is still rejected — an override nobody wrote down
    produces no evidence, and evidence is the whole reason overrides exist."""
    gate = _contract(tmp_path, monkeypatch)
    row = _fade_row()
    out = ls.parse_pick(_override_md(row, "best sim row"), [row],
                        my_entries=1, gate=gate)
    assert out["picks"] == []
    assert any("has to SAY SO" in e for e in out["errors"])
    assert any("FadeGuy" in e for e in out["errors"])


def _uw_rows():
    """Slice rows for the underweight soft-cap tests: two carriers, one clean."""
    rows = []
    for i, roster in ((1, ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"]),
                      (2, ["CoreA", "CoreB", "LevGuy", "UwGuy", "X3", "X4"]),
                      (3, ["CoreA", "CoreB", "LevGuy", "X1", "X2", "X3"])):
        rows.append({"index": i, "roster": roster,
                     "roster_key": "|".join(sorted(roster))})
    return rows


def _pick_md(rows, ids):
    lines = ["| pick | id | players | why |", "|---|---|---|---|"]
    by = {r["index"]: r for r in rows}
    for n, i in enumerate(ids, 1):
        lines.append(f"| {n} | {i} | " + ", ".join(by[i]["roster"]) + " | w |")
    return "\n".join(lines)


def test_parse_pick_allows_an_underweight_carrier_with_a_warning(tmp_path,
                                                                 monkeypatch):
    """The 8/23 Clinch bug, fixed: an UNDERWEIGHT carrier is pickable. Single
    entry — the exact case the old gate banned — saves, with the cost named."""
    gate = _contract(tmp_path, monkeypatch)
    rows = _uw_rows()
    out = ls.parse_pick(_pick_md(rows, [1]), rows, my_entries=1, gate=gate)
    assert out["errors"] == []
    assert [p["index"] for p in out["picks"]] == [1]
    assert any("UNDERWEIGHT" in w for w in out["warnings"])


def test_parse_pick_rejects_same_underweight_player_in_every_entry(tmp_path,
                                                                   monkeypatch):
    """"Less than the crowd, never zero" — the same underweight player in ALL
    entries of a multi-entry contest is not less, and is the one hard stop."""
    gate = _contract(tmp_path, monkeypatch)
    rows = _uw_rows()
    out = ls.parse_pick(_pick_md(rows, [1, 2]), rows, my_entries=2, gate=gate)
    assert out["picks"] == []
    assert any("every entry carries UwGuy" in e for e in out["errors"])
    # A minority carrier is the verdict working as intended: allowed + warned.
    out2 = ls.parse_pick(_pick_md(rows, [1, 3]), rows, my_entries=2, gate=gate)
    assert out2["errors"] == []
    assert len(out2["picks"]) == 2
    assert any("1 of 2" in w and "UwGuy" in w for w in out2["warnings"])


def test_no_leverage_pool_is_completely_unpenalized(tmp_path, monkeypatch):
    """8/28/26 (user directive): a pool where NO lineup carries a low-owned
    player is fully pickable and completely unmarked — nothing deleted, no
    relax needed, and no ⚠ anywhere. The gate enforces THIS slate's strategy;
    an ownership screen is not that."""
    gate = _contract(tmp_path, monkeypatch)
    no_lev = ["CoreA", "CoreB", "MidGuy", "X1", "X2", "X3"]
    pool = {"rosters": [no_lev] * 40}
    elig = ls.eligible_indexes(pool, gate)
    assert elig["relaxed"] == [] and elig["full"] == 40
    assert elig["allowed"] == set(range(40))
    # In the slice, no-leverage rows carry NO marker of any kind.
    sim_pool = _pool()
    c = sim_pool["contests"][0]
    for i in range(len(sim_pool["rosters"])):
        sim_pool["rosters"][i] = ["CoreA", "CoreB", f"M{i}", "X1", "X2", "X3"]
    rows = ls.candidate_slice(sim_pool, c,
                              strategy={"leverage": ["LevGuy"],
                                        "underweight": []})
    assert rows
    assert all(r["strategy"] is None for r in rows)
    md = ls.slice_digest_md("mma_se", c["label"], c, None, rows,
                            sim_pool["ownership"])
    assert "no leverage name" not in md
    # ...and the gate summary says plainly that it is not a rule.
    gmd = ls.gate_summary(gate, elig, pool=pool)
    assert "LEVERAGE IS NOT A RULE HERE" in gmd
    assert "breaks nothing and costs nothing" in gmd


def test_parse_pick_never_mentions_leverage(tmp_path, monkeypatch):
    """A pick set carrying ZERO low-owned players is a complete, valid answer
    (the 7/19 contest winners were exactly that) — no error, no warning, no
    nudge. 8/28/26 user directive."""
    gate = _contract(tmp_path, monkeypatch)
    rows = []
    for i, roster in ((1, ["CoreA", "CoreB", "MidGuy", "X1", "X2", "X3"]),
                      (2, ["CoreA", "CoreB", "MidGuy", "X4", "X5", "X6"]),
                      (3, ["CoreA", "CoreB", "LevGuy", "X1", "X2", "X3"])):
        rows.append({"index": i, "roster": roster,
                     "roster_key": "|".join(sorted(roster))})
    out = ls.parse_pick(_pick_md(rows, [1, 2]), rows, my_entries=2, gate=gate)
    assert out["errors"] == []
    assert len(out["picks"]) == 2
    assert not any("leverage" in w.lower() for w in out["warnings"])
    # Carrying one is equally unremarked — it is information, not a score.
    out2 = ls.parse_pick(_pick_md(rows, [1, 3]), rows, my_entries=2, gate=gate)
    assert out2["errors"] == []
    assert not any("leverage" in w.lower() for w in out2["warnings"])


def test_gate_summary_is_plain_language(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch)
    elig = {"allowed": set(range(5)), "relaxed": ["core"],
            "full": 3, "total": 100}
    md = ls.gate_summary(gate, elig)
    assert "FADE or LEAN FADE" in md and "FadeGuy" in md
    assert "ChalkA" in md
    assert "3 of 100" in md
    assert "⚠️" in md and "core" in md             # the relaxation is announced
    # A dropped rule is not advertised as enforced.
    assert "Core-tier" not in md.split("SOFT RULE")[0].split("dropped")[0] \
        or "at least" not in md.split("\n")[2]
    # UNDERWEIGHT is described as a SOFT rule, never as an exclusion.
    assert "SOFT RULE" in md and "UwGuy" in md
    assert "no player the strategy called UNDERWEIGHT" not in md
    # LEVERAGE is described as NOT A RULE (8/28/26) — never as a requirement
    # of any strength, hard or soft.
    assert "LEVERAGE IS NOT A RULE HERE" in md and "LevGuy" in md
    assert "every lineup needs one" not in md
    assert "at least one player off the strategy's leverage list" not in md
    assert "SOFT RULE — LEVERAGE" not in md


def test_gate_summary_prices_every_rule_against_the_pool(tmp_path, monkeypatch):
    """The 8/23 lesson: the digest reports how many lineups each verdict
    removes (hard) or flags (soft), so a call's price is visible pre-pick."""
    gate = _contract(tmp_path, monkeypatch)
    good = ["CoreA", "CoreB", "LevGuy", "MidGuy", "X1", "X2"]
    uw = ["CoreA", "CoreB", "LevGuy", "UwGuy", "X1", "X2"]
    fade = ["CoreA", "CoreB", "LevGuy", "FadeGuy", "X1", "X2"]
    no_lev = ["CoreA", "CoreB", "MidGuy", "X1", "X2", "X3"]
    pool = {"rosters": [good] * 40 + [uw] * 30 + [fade] * 20 + [no_lev] * 10}
    elig = ls.eligible_indexes(pool, gate)
    md = ls.gate_summary(gate, elig, pool=pool)
    assert "removes 20 of the 100 pooled lineups" in md      # the fade price
    assert "UwGuy (30 pooled lineups carry them)" in md      # the soft price
    assert "put the same underweight player in every entry" in md
    # Leverage is NOT priced, because it costs nothing — the 10 no-leverage
    # lineups in this pool are charged for exactly nothing.
    assert "carry no leverage name" not in md
    assert "LEVERAGE IS NOT A RULE HERE" in md


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


# ---------------------------------------------------------------------------
# 8/29/26 fixes — the three that let both MMA winners through unconsidered
# ---------------------------------------------------------------------------

def test_contract_conflict_core_equals_forbidden_pair(tmp_path, monkeypatch):
    """The 8/29 contract verbatim: Core tier is exactly the forbidden chalk
    pair, so "hold 2 Core" and "never hold both" cannot both be met. The full
    gate returned 0 of 7,500 and the only signal was the word "relaxed"."""
    gate = _contract(
        tmp_path, monkeypatch,
        board=[{"name": "Umar", "tier": "Core"}, {"name": "LiuCe", "tier": "Core"},
               {"name": "MidGuy", "tier": "Good"}],
        chalk_pairs=[{"players": ["Umar", "LiuCe"], "joint_pct": 17.1}])
    conflicts = ls.contract_conflicts(gate)
    assert len(conflicts) == 1
    assert "no lineup on earth can" in conflicts[0]
    assert "Umar" in conflicts[0] and "LiuCe" in conflicts[0]

    # The real consequence: zero pass the full gate, and `core` gets relaxed.
    pool = {"rosters": [["Umar", "LiuCe", "MidGuy", "X1", "X2", "X3"],
                        ["Umar", "MidGuy", "X1", "X2", "X3", "X4"],
                        ["LiuCe", "MidGuy", "X1", "X2", "X3", "X4"]] * 15}
    elig = ls.eligible_indexes(pool, gate)
    # Nothing can satisfy the contract, so NOTHING is clean — and since
    # 8/29/26 every row is still pickable, priced.
    assert elig["full"] == 0
    assert elig["allowed"] == set(range(len(pool["rosters"])))
    assert elig["conflicts"] == conflicts

    # The summary still leads with the contradiction: a zero-clean pool caused
    # by a broken contract must never read like a thin pool.
    md = ls.gate_summary(gate, elig, pool=pool)
    assert md.startswith("\U0001f6d1 THIS SLATE'S STRATEGY CONTRADICTS ITSELF")
    assert "NOT a thin pool" in md
    assert "break NO strategy rule" in md


def test_contract_conflict_absent_on_a_coherent_contract(tmp_path, monkeypatch):
    """Three Core names and a chalk pair inside them is NOT a contradiction —
    a legal pair still exists. No false alarm."""
    gate = _contract(tmp_path, monkeypatch,
                     chalk_pairs=[{"players": ["CoreA", "CoreB"]}])
    assert ls.contract_conflicts(gate) == []
    pool = {"rosters": [["CoreA", "CoreC", "MidGuy", "X1", "X2", "X3"]] * 30}
    elig = ls.eligible_indexes(pool, gate)
    assert elig["conflicts"] == []
    assert not ls.gate_summary(gate, elig, pool=pool).startswith("🛑")


def test_contract_conflict_core_player_also_faded(tmp_path, monkeypatch):
    gate = _contract(tmp_path, monkeypatch,
                     board=[{"name": "FadeGuy", "tier": "Core"},
                            {"name": "CoreB", "tier": "Core"},
                            {"name": "CoreC", "tier": "Core"}])
    conflicts = ls.contract_conflicts(gate)
    assert any("FadeGuy" in c and "must-have" in c and "never play" in c
               for c in conflicts)


def test_contract_conflict_fade_beats_underweight(tmp_path, monkeypatch):
    """A player called both FADE and UNDERWEIGHT: the gate enforces the fade,
    so the softer call is dead. Say which one is actually running."""
    gate = _contract(tmp_path, monkeypatch,
                     calls=[{"name": "UwGuy", "verdict": "underweight"},
                            {"name": "UwGuy", "verdict": "fade"}])
    assert any("doing nothing" in c for c in ls.contract_conflicts(gate))


def test_rule_price_reports_sim_quality_not_just_a_count(tmp_path, monkeypatch):
    """8/29: the LEAN FADE on Sean Woodson removed a quarter of the pool and
    the count alone was already shown. What was missing is that the deleted
    branch held some of the pool's strongest simmed rows."""
    gate = _contract(tmp_path, monkeypatch)
    # 20 rows carry the faded player and hold the 20 BEST top1 values.
    rosters, top1, roi = [], [], []
    for i in range(60):
        faded = i < 20
        rosters.append((["LeanGuy"] if faded else ["MidGuy"])
                       + ["CoreA", "CoreB", f"X{i}", "Y", "Z"])
        top1.append(5.0 - i * 0.05)
        roi.append(90.0 - i)
    pool = {"rosters": rosters}
    contest = {"metrics": {"top1_pct": top1, "roi_pct": roi}}

    bare = ls.rule_price(gate, pool, "fade")
    assert bare["n"] == 20 and bare["pct"] == 33.3
    assert bare["top50_top1"] is None          # no metrics -> no quality claim

    priced = ls.rule_price(gate, pool, "fade", contest)
    assert priced["n"] == 20
    assert priced["top50_top1"] == 20          # it deletes the whole top end
    assert priced["top50_roi"] == 20
    assert priced["best_top1"] == 5.0

    md = ls.gate_summary(gate, ls.eligible_indexes(pool, gate),
                         pool=pool, contest=contest)
    assert "20 of the pool's 50 best rows by Top-1%" in md
    assert "best lineup it removes had a 5.0% chance of finishing first" in md


def test_metric_resolution_band_and_ties():
    """A gap smaller than the sampling band is a tie, not a ranking."""
    rows = [{"index": 0, "top1_pct": 3.56}, {"index": 1, "top1_pct": 3.34},
            {"index": 2, "top1_pct": 3.25}, {"index": 3, "top1_pct": 2.96},
            {"index": 4, "top1_pct": 1.67}]
    res = ls.metric_resolution(rows, sims=10_000)
    assert res["known"] and res["best"] == 3.56
    assert 0.3 < res["band"] < 0.45          # ~2 SE of a 3.56% rate on 10k sims
    # The 0.08 and 0.22 gaps the 8/29 picker treated as decisive are ties.
    assert 0 in res["tied_ids"] and 1 in res["tied_ids"] and 2 in res["tied_ids"]
    assert 4 not in res["tied_ids"]          # a 1.89-point gap is real
    md = ls.resolution_md(res)
    assert "is a TIE, not a ranking" in md
    assert "Look DOWN the table" in md


def test_metric_resolution_invents_nothing_without_a_sim_count():
    rows = [{"index": 0, "top1_pct": 3.5}, {"index": 1, "top1_pct": 2.0}]
    res = ls.metric_resolution(rows, sims=None)
    assert res["known"] is False
    assert res["band"] is None and res["tied_ids"] == []
    assert "resolution: unknown" in ls.resolution_md(res)


def test_digest_marks_tied_rows_when_sims_are_known(tmp_path, monkeypatch):
    pool = _pool()
    c = pool["contests"][0]
    # The shared fixture's synthetic metrics run past 100; a real top1_pct is
    # a percentage, and the tie band is only meaningful on one.
    n = len(pool["rosters"])
    c = dict(c, metrics=dict(c["metrics"],
                             top1_pct=[round(3.6 - i * 0.02, 2) for i in range(n)]))
    rows = ls.candidate_slice(pool, c)
    md_no = ls.slice_digest_md("mma_se", c["label"], c, None, rows,
                               pool["ownership"])
    md_yes = ls.slice_digest_md("mma_se", c["label"], c, None, rows,
                                pool["ownership"], sims=10_000)
    assert "resolution: unknown" in md_no
    assert "is a TIE, not a ranking" in md_yes
    # The tie column exists in both, and the header stays aligned.
    assert "| id | tie | salary |" in md_yes
    # Read the CANDIDATE table only — the family summary above it is also
    # pipe-delimited and has its own column count.
    start = md_yes.index("| id | tie | salary |")
    body = [l for l in md_yes[start:].splitlines()
            if l.startswith("| ") and "id |" not in l and not set(l) <= set("|- ")]
    assert body and all(l.count("|") == 14 for l in body)
    # A 3.6% rate on 10k sims bands at ~0.37, so the top ~19 rows tie.
    assert sum(1 for l in body if "| = |" in l) > 5


# ---------------------------------------------------------------------------
# 8/29/26 picker rebuild — bigger slice, evidence-weighted blend, families
# ---------------------------------------------------------------------------

def test_top1_leads_the_blend_and_projection_does_not(tmp_path):
    """User directive 8/29/26: "the picker's number 1 item to choose from
    should NOT be projected points." Winners project 94 on a 100-scale and so
    does the median entry — projection qualifies a lineup, it never separates
    one. A lineup that is best on the chance of WINNING must outrank a lineup
    that is best on projection."""
    n = 2
    pool = {"rosters": [["A"] * 6, ["B"] * 6],
            "proj": [0.0, 100.0],        # row 1 owns projection outright
            "avg_own": [0.0, 100.0]}     # ...and ownership too
    contest = {"field_size": 5000,
               "metrics": {"top1_pct": [100.0, 0.0],   # row 0 owns top1
                           "cash_pct": [100.0, 0.0]}}  # ...and cash
    b = ls.blend_scores(pool, contest)
    assert b[0] > b[1]
    # Concretely: top1 must outweigh projection on its own.
    solo = ls.blend_scores(
        {"rosters": [["A"] * 6, ["B"] * 6], "proj": [0.0, 100.0],
         "avg_own": [0.0, 0.0]},
        {"field_size": 5000,
         "metrics": {"top1_pct": [100.0, 0.0], "cash_pct": [0.0, 0.0]}})
    assert solo[0] > solo[1]


def test_blend_still_uses_projection_and_ownership_as_real_terms():
    """Demoted is not deleted — pure top1% with nothing behind it measured
    WORSE (42% winner capture) than the blend (58%)."""
    flat = [1.0, 1.0]
    base = {"rosters": [["A"] * 6, ["B"] * 6], "avg_own": [0.0, 0.0]}
    contest = {"field_size": 5000,
               "metrics": {"top1_pct": flat, "cash_pct": flat}}
    b = ls.blend_scores(dict(base, proj=[0.0, 100.0]), contest)
    assert b[1] > b[0]                       # projection still breaks a tie
    o = ls.blend_scores(dict(base, proj=[0.0, 0.0],
                             avg_own=[0.0, 100.0]), contest)
    assert o[1] > o[0]                       # so does ownership


def test_blend_is_one_curve_for_every_field_size():
    """The small-field branch is gone: the tail leads everywhere now, so a
    separate 'small fields pay the tail' weighting had nothing left to do."""
    pool = {"rosters": [["A"] * 6, ["B"] * 6], "proj": [10.0, 20.0],
            "avg_own": [5.0, 9.0]}
    met = {"top1_pct": [3.0, 1.0], "cash_pct": [30.0, 20.0]}
    assert (ls.blend_scores(pool, {"field_size": 300, "metrics": met})
            == ls.blend_scores(pool, {"field_size": 60000, "metrics": met}))


def test_blend_never_rewards_points_per_ownership():
    """Unchanged by the 8/29 re-weighting. proj/ownership correlates -0.084 with the real finish. A cheap-ownership
    lineup must not outrank a better one on that ratio alone."""
    pool = {"rosters": [["A"] * 6, ["B"] * 6],
            "proj": [100.0, 100.0], "avg_own": [5.0, 40.0]}
    flat = [1.0, 1.0]
    b = ls.blend_scores(pool, {"field_size": 5000,
                               "metrics": {"top1_pct": flat, "cash_pct": flat}})
    # Equal projection, higher ownership -> higher blend (ownership is POSITIVE).
    assert b[1] > b[0]


def test_slice_fills_to_the_cap_with_different_ideas():
    """The angles alone stall at ~200 near-identical rows however wide they are
    set — the fill-to-cap branch is what makes a 500-row slice mean anything.
    Regression for the first cut of this rework, which returned 217 rows and
    was LESS diverse than the 100-row slice it replaced.

    Fixture shape is the real one: the top of the blend is a chalk block that
    all shares a core, and the variety lives just below it. A pure rank cut
    never leaves the block; the coverage fill has to."""
    n = 3000
    chalk = ["C1", "C2", "C3", "C4"]
    rosters, proj = [], []
    for i in range(n):
        if i < 700:                     # highest projection, one shared core
            rosters.append(chalk + [f"X{i}", f"Y{i}"])
            proj.append(500.0 - i * 0.01)
        else:                           # everything else, genuinely varied
            rosters.append([f"A{i}", f"B{i}", f"D{i}", f"E{i}", f"F{i}", f"G{i}"])
            proj.append(400.0 - i * 0.01)
    names = sorted({p for r in rosters for p in r})
    pool = {"rosters": rosters, "salary": [49000] * n, "proj": proj,
            "avg_own": [20.0] * n, "ownership": {p: 15.0 for p in names}}
    flat = [1.0] * n
    contest = {"label": "Big SE", "field_size": 5000,
               "metrics": {"top1_pct": flat, "win_pct": flat,
                           "cash_pct": flat, "roi_pct": flat}}
    rows = ls.candidate_slice(pool, contest)
    assert len(rows) == ls._SLICE_CAP == 500
    # Deterministic: same inputs, same slice.
    assert [r["index"] for r in rows] == \
        [r["index"] for r in ls.candidate_slice(pool, contest)]
    # A pure rank cut would be 500 rows off the same 4-man core. The coverage
    # fill has to escape the block, so it touches far more distinct players.
    blend = ls.blend_scores(pool, contest)
    rank_cut = sorted(range(n), key=lambda i: (-blend[i], i))[:500]
    distinct = lambda idxs: len({p for i in idxs for p in rosters[i]})
    assert distinct([r["index"] for r in rows]) > distinct(rank_cut)
    assert any(r["index"] >= 700 for r in rows)     # it left the chalk block


def test_lineup_families_group_the_slice_by_core():
    """500 rows are not 500 ideas. Families let the picker choose a THESIS
    first and a row second."""
    rows = []
    for i in range(12):          # thesis A: everyone shares 4 core players
        rows.append({"index": i, "top1_pct": 3.0, "cash_pct": 30.0, "proj": 400.0,
                     "avg_own": 25.0,
                     "roster": ["CoreA", "CoreB", "CoreC", "CoreD", f"X{i}", f"Y{i}"]})
    for i in range(12, 20):      # thesis B: a completely different core
        rows.append({"index": i, "top1_pct": 2.0, "cash_pct": 25.0, "proj": 380.0,
                     "avg_own": 20.0,
                     "roster": ["AltA", "AltB", "AltC", "AltD", f"X{i}", f"Y{i}"]})
    fams = ls.lineup_families(rows)
    assert len(fams) == 2
    assert fams[0]["n"] == 12 and fams[1]["n"] == 8
    assert set(fams[0]["core"]) == {"CoreA", "CoreB", "CoreC", "CoreD"}
    assert set(fams[1]["core"]) == {"AltA", "AltB", "AltC", "AltD"}
    assert fams[0]["best_cash"] == 30.0
    md = ls.families_md(fams)
    assert "The theses on this slate" in md and "CoreA" in md and "AltA" in md
    # Deterministic.
    assert ls.lineup_families(rows) == fams


def test_override_log_round_trips(tmp_path):
    """The whole reason the gate was softened: overrides must be recorded so
    they can be scored against real finishes later."""
    ls.log_override("mma_se", "UFC Shanghai", "UFC $4K SE", 42,
                    ["A", "B", "C", "D", "E", "F"],
                    ["carries Sean Woodson — the strategy calls him LEAN FADE"],
                    "he is the only path to a winning score", rules_dir=tmp_path)
    ls.log_override("mma_se", "UFC Shanghai", "UFC $3K SE", 77,
                    ["G", "H", "I", "J", "K", "L"],
                    ["carries Sean Woodson — the strategy calls him LEAN FADE"],
                    "same read, different core", rules_dir=tmp_path)
    rep = ls.override_report("mma_se", rules_dir=tmp_path)
    assert rep["n"] == 2
    assert rep["slates"] == ["UFC Shanghai"]
    assert rep["by_rule"]["carries Sean Woodson"] == 2
    assert rep["rows"][0]["reason"].startswith("he is the only path")


def test_override_report_is_empty_before_any_override(tmp_path):
    assert ls.override_report("nascar", rules_dir=tmp_path)["n"] == 0
