"""Field tendencies: shape-first + on-slate name filtering (7/31/26).
The user's direction: surface the ownership PATTERN the field piles into, not
stale player names — a warning must never demand the strategy discuss a player
who isn't on the current card."""
import src.field_tendencies as ft


def _write_rows(tmp_path, monkeypatch, rows):
    import json
    monkeypatch.setattr(ft, "_REPO_ROOT", tmp_path)
    p = tmp_path / "rules" / "mma_se" / "field_tendencies.jsonl"
    p.parent.mkdir(parents=True)
    with p.open("w") as f:
        for i, r in enumerate(rows):
            r.setdefault("contest_id", str(i))
            f.write(json.dumps(r) + "\n")


def _row(i, crowded, ctype="SE"):
    return {"date": f"2026-07-{10+i:02d}", "contest_type": ctype,
            "contest_name": None, "contest_key": "", "field_size": 500,
            "crowded_players": crowded, "crowded_combos": [],
            "fish_traps": [], "top_opponents": [],
            "winners_avg_own": 33.0, "winners_unique_pct": 90.0,
            "fish_avg_own": 36.0}


def test_summarize_reads_legacy_strings_and_new_dicts(tmp_path, monkeypatch):
    _write_rows(tmp_path, monkeypatch, [
        _row(1, ["Max Holloway", "Paddy Pimblett"]),                       # legacy
        _row(2, [{"name": "Max Holloway", "own": 41.2},                    # new
                 {"name": "King Green", "own": 33.0}]),
    ])
    s = ft.summarize("mma_se", "SE")
    crowd = {c["name"] for c in s["reliably_crowded"]}
    assert "Max Holloway" in crowd                    # counted across both shapes
    shape = s["crowd_shape"]
    assert shape["avg_crowd_size"] == 2.0
    assert shape["own_median"] in (33.0, 41.2)        # from the dict row only


def test_names_filtered_to_current_slate(tmp_path, monkeypatch):
    _write_rows(tmp_path, monkeypatch, [
        _row(1, [{"name": "Max Holloway", "own": 40.0},
                 {"name": "King Green", "own": 30.0}]),
        _row(2, [{"name": "Max Holloway", "own": 42.0},
                 {"name": "King Green", "own": 31.0}]),
    ])
    contests = [{"name": None, "type": "SE"}]
    # No filter: both names surface (legacy behavior).
    assert set(ft.crowded_names("mma_se", contests)) == {"Max Holloway", "King Green"}
    # New card, full roster turnover: NO names -> no warning material...
    assert ft.crowded_names("mma_se", contests,
                            current_names=["Ilia Topuria", "Movsar Evloev"]) == []
    # ...but the bundle block still carries the SHAPE + off-slate note.
    block = ft.bundle_block("mma_se", contests,
                            current_names=["Ilia Topuria", "Movsar Evloev"])
    assert "SHAPE: the field reliably piles onto" in block
    assert "NOT on this card" in block
    assert "Max Holloway" not in block.replace("past crowd name", "")
    # A crowd player who IS on the card still surfaces by name.
    on_slate = ft.crowded_names("mma_se", contests,
                                current_names=["King Green", "Someone Else"])
    assert on_slate == ["King Green"]
    block2 = ft.bundle_block("mma_se", contests,
                             current_names=["King Green", "Someone Else"])
    assert "King Green" in block2
