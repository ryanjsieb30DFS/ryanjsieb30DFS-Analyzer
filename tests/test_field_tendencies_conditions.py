"""A trap is a price, not a driver (8/9/26): condition-dict traps, trap-shape
rollups, field-size gating, bundle copy, and the history backfill."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd  # noqa: E402

from src import field_tendencies as ft  # noqa: E402
from src.bundle import _trap_price_lines  # noqa: E402


def _profile(field_size=500):
    return {
        "gradable": True,
        "crowded_players": [
            {"name": "Chalky", "field_own": 45.0, "actual_fpts": 50.0},
            {"name": "Popular", "field_own": 30.0, "actual_fpts": 20.0},
        ],
        "crowded_combos": [{"players": ["Chalky", "Popular"]}],
        "fish_traps": [
            {"name": "Popular", "fish_pct": 60.0, "winner_pct": 5.0, "gap": 55.0,
             "actual_fpts": 20.0, "field_own": 30.0, "own_rank": 2},
            {"name": "Dart", "fish_pct": 20.0, "winner_pct": 0.0, "gap": 20.0,
             "actual_fpts": 5.0, "field_own": 4.0, "own_rank": 9},
        ],
        "top_opponents": [],
        "winners_profile": {"avg_own_per_slot": 33.0, "unique_pct": 80.0},
        "fish_profile": {"avg_own_per_slot": 28.0},
    }


def _pool():
    # Popular: 2nd-highest own but only 3rd-best projection -> edge -1 (trap-shaped).
    return pd.DataFrame({
        "name": ["Chalky", "Popular", "Better", "Dart"],
        "salary": [10500, 8200, 8000, 5200],
        "ownership": [40.0, 30.0, 15.0, 4.0],
        "proj_points": [55.0, 40.0, 44.0, 20.0],
    })


def test_record_stores_condition_dicts_with_projection_context(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    assert ft.record("nascar", "SE", 500, _profile(), "2026-08-09",
                     contest_name="Test SE", contest_id="c1", pool=_pool())
    row = json.loads(ft._path("nascar").read_text().strip())
    assert row["schema_version"] == 2
    trap = row["fish_traps"][0]
    assert trap["name"] == "Popular"
    # Standings-side condition survives...
    assert trap["fish_pct"] == 60.0 and trap["field_own"] == 30.0
    # ...and the slate's price context is attached.
    assert trap["salary"] == 8200 and trap["salary_tier"] == "Upper-mid ($8-10k)"
    assert trap["proj_own"] == 30.0
    assert trap["edge"] == -1          # owned ahead of projection = trap-shaped
    crowd = row["crowded_players"][0]
    assert crowd["own"] == 45.0 and crowd["fpts"] == 50.0
    assert crowd["salary"] == 10500    # crowds get the context too


def test_record_without_pool_still_stores_conditions(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    assert ft.record("nascar", "SE", 500, _profile(), "2026-08-09", pool=None)
    row = json.loads(ft._path("nascar").read_text().strip())
    trap = row["fish_traps"][0]
    assert trap["fish_pct"] == 60.0 and "salary" not in trap and "edge" not in trap


def test_field_size_gating(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    ft.record("nascar", "SE", 490, _profile(), "2026-08-01", contest_id="a")
    ft.record("nascar", "SE", 588, _profile(), "2026-08-02", contest_id="b")
    ft.record("nascar", "SE", 23461, _profile(), "2026-08-03", contest_id="c")
    # Target 500: the 23k row is NOT comparable and is excluded.
    summ = ft.summarize("nascar", "SE", target_field_size=500)
    assert summ["n_contests"] == 2
    # No target: legacy behavior — everything pools.
    assert ft.summarize("nascar", "SE")["n_contests"] == 3
    # A row with no recorded size survives the gate (old rows never vanish).
    assert ft._size_ok(None, 500) and ft._size_ok(0, 500)
    assert not ft._size_ok(23461, 500) and ft._size_ok(600, 500)


def test_trap_shape_ignores_legacy_bare_names():
    legacy = {"fish_traps": ["Byron", "Bubba"]}
    assert ft._trap_shape([legacy]) is None            # names carry no evidence
    v2 = {"fish_traps": _profile()["fish_traps"]}
    ts = ft._trap_shape([legacy, v2])
    assert ts["n_traps"] == 2 and ts["n_rows"] == 1    # only the dict row counts
    assert ts["chalk_share"] == {"k": 1, "t": 2}       # Popular 30% own; Dart 4%
    assert ts["fish_pct_median"] in (20.0, 60.0)


def test_summaries_have_no_trap_name_counts(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    for i in range(2):
        ft.record("nascar", "SE", 500, _profile(), f"2026-08-0{i+1}",
                  contest_name="Test SE", contest_id=str(i))
    for summ in (ft.summarize("nascar", "SE"),
                 ft.summarize_contest("nascar", "Test SE")):
        assert summ is not None
        assert "recurring_traps" not in summ
        assert summ["trap_shape"] is not None
        assert json.dumps(summ)                        # stays serializable


def test_bundle_block_copy_rules(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    for i in range(2):
        ft.record("nascar", "SE", 500, _profile(), f"2026-08-0{i+1}",
                  contest_name="Test SE", contest_id=str(i))
    block = ft.bundle_block("nascar", [{"name": "Test SE", "type": "SE",
                                        "field_size": 500}])
    assert block is not None
    assert "A TRAP IS A PRICE, NOT A DRIVER" in block
    assert "your opponents" in block
    assert "recurring fish-traps" not in block         # the old name list is gone
    assert "Chalky (in 2 of 2)" in block               # crowd names stay (opponent map)
    assert "trap shape" in block


def test_trap_price_lines_current_slate():
    lines = _trap_price_lines(_pool())
    # Popular (30% own, projection rank 3) is this slate's trap-shaped price.
    assert any("Popular" in l for l in lines)
    assert any("owned ahead of projection" in l for l in lines)
    # Chalky (top own, top projection, edge 0) is aligned — not trap-shaped.
    assert not any("Chalky" in l for l in lines)
    assert _trap_price_lines(pd.DataFrame()) == []


def test_migration_round_trip(tmp_path):
    from scripts.migrate_field_tendencies import migrate_slug
    rules = tmp_path / "rules" / "nascar"
    hist = rules / "history" / "2026-07-26__test-slate"
    hist.mkdir(parents=True)
    (hist / "autopsy.json").write_text(json.dumps([{
        "contest_id": "111", "entries": 490,
        "field_profile": {
            "crowded_players": [{"name": "Chalky", "field_own": 45.0,
                                 "actual_fpts": 50.0}],
            "fish_traps": [{"name": "Popular", "fish_pct": 60.0,
                            "winner_pct": 5.0, "gap": 55.0, "actual_fpts": 20.0}],
        },
    }]))
    (hist / "bundle.md").write_text("\n".join([
        "### Vendor — file.csv (3 players)",
        "| name | salary | ownership | proj_points |",
        "| --- | --- | --- | --- |",
        "| Popular | 8200 | 30.0 | 40.0 |",
        "| Better | 8000 | 15.0 | 44.0 |",
        "| Chalky | 10500 | 40.0 | 55.0 |",
    ]))
    legacy_row = {"date": "2026-07-26 20:00", "contest_type": "SE",
                  "contest_id": "111", "field_size": 490,
                  "crowded_players": ["Chalky"], "fish_traps": ["Popular"]}
    unmatched_row = {"date": "2026-01-01 12:00", "contest_type": "SE",
                     "contest_id": "999", "field_size": 42,
                     "crowded_players": ["Ghost"], "fish_traps": ["Ghost"]}
    p = rules / "field_tendencies.jsonl"
    p.write_text(json.dumps(legacy_row) + "\n" + json.dumps(unmatched_row) + "\n")

    s = migrate_slug(tmp_path, "nascar")
    assert s["matched"] == 1 and s["legacy"] == 1 and s["written"]
    assert p.with_suffix(".jsonl.bak").exists()
    rows = [json.loads(l) for l in p.read_text().splitlines()]
    migrated, untouched = rows
    assert migrated["schema_version"] == 2
    trap = migrated["fish_traps"][0]
    assert trap["name"] == "Popular" and trap["fish_pct"] == 60.0
    assert trap["salary"] == 8200 and trap["proj_own"] == 30.0
    assert trap["edge"] == -1                          # own rank 2, proj rank 1... trap-shaped
    assert untouched == unmatched_row                  # no archive -> left as-is
