"""Unit tests for own-strategy adherence grading + the ledger write-time helpers."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import adherence, history  # noqa: E402


def _records(rosters: list[list[str]]) -> list[dict]:
    return [{"user_lineups": [{"players": r} for r in rosters]}]


def _contract(calls=None, leverage=None) -> dict:
    return {"calls": calls or [], "leverage_candidates": leverage or []}


def test_fade_violation_counted():
    a = adherence.grade_adherence(
        _contract(calls=[{"name": "Chalk Guy", "verdict": "fade"}]),
        _records([["Chalk Guy", "B", "C"], ["D", "E", "F"]]),
    )
    assert a["gradable"] and a["fades_violated"] == 1
    assert a["calls"][0]["followed"] is False
    assert a["calls"][0]["in_lineups"] == 1


def test_fade_honored():
    a = adherence.grade_adherence(
        _contract(calls=[{"name": "Chalk Guy", "verdict": "fade"}]),
        _records([["A", "B", "C"]]),
    )
    assert a["fades_violated"] == 0 and a["calls"][0]["followed"] is True


def test_soft_verdict_threshold():
    # lean_fade honored at <=50% exposure, violated above.
    recs = _records([["X", "B"], ["X", "C"], ["D", "E"]])  # X in 2 of 3 = 67%
    a = adherence.grade_adherence(
        _contract(calls=[{"name": "X", "verdict": "lean_fade"}]), recs)
    assert a["soft_violated"] == 1 and a["calls"][0]["followed"] is False


def test_play_ignored_is_informational_not_violation():
    a = adherence.grade_adherence(
        _contract(calls=[{"name": "Named Play", "verdict": "play"}]),
        _records([["A", "B"]]),
    )
    assert a["fades_violated"] == 0 and a["soft_violated"] == 0
    assert a["calls"][0]["ignored"] is True


def test_leverage_coverage():
    a = adherence.grade_adherence(
        _contract(leverage=[{"name": "Dart One"}, {"name": "Dart Two"}]),
        _records([["Dart One", "B"], ["C", "D"]]),
    )
    assert a["leverage_covered"] == 1 and a["leverage_of"] == 2


def test_duplicate_rosters_count_once():
    # The same bullet entered in two contests is ONE decision.
    recs = [{"user_lineups": [{"players": ["X", "B"]}]},
            {"user_lineups": [{"players": ["X", "B"]}]}]
    a = adherence.grade_adherence(
        _contract(calls=[{"name": "X", "verdict": "fade"}]), recs)
    assert a["n_lineups"] == 1


def test_not_gradable_without_contract_or_lineups():
    assert adherence.grade_adherence(None, _records([["A"]]))["gradable"] is False
    assert adherence.grade_adherence(_contract(calls=[{"name": "A", "verdict": "fade"}]),
                                     [])["gradable"] is False


def test_adherence_md_renders():
    a = adherence.grade_adherence(
        _contract(calls=[{"name": "Chalk Guy", "verdict": "fade"}]),
        _records([["Chalk Guy", "B"]]))
    md = adherence.adherence_md(a)
    assert "FADE call(s) violated" in md and "Chalk Guy" in md


def test_per_contest_zeroed_underweight_flagged():
    # UNDERWEIGHT honored on the pooled numbers (3 of 26 = 11.5%) but ZERO in
    # one contest — the Cameron Young miss the pooled grade called "followed".
    records = [
        {"source_file": "small.csv", "contest_id": "1",
         "user_lineups": [{"players": [f"A{i}", "B", "C"]} for i in range(5)]},
        {"source_file": "big.csv", "contest_id": "2",
         "user_lineups": [{"players": ["Cameron Young", f"D{i}", "E"]} for i in range(3)]
                          + [{"players": [f"F{i}", "G", "H"]} for i in range(18)]},
    ]
    a = adherence.grade_adherence(
        {"calls": [{"name": "Cameron Young", "verdict": "underweight"}]}, records)
    call = a["calls"][0]
    assert call["followed"] is True            # pooled check still passes
    assert call["zeroed_in"] == ["small.csv"]  # ...but the zero is named
    assert a["per_contest_flags"] == 1
    md = adherence.adherence_md(a)
    assert "zeroed in one contest" in md and "small.csv" in md


def test_per_contest_over_exposure_hidden_by_pooling_flagged():
    # lean_fade at 4 of 10 pooled (40%, passes) but 4 of 5 (80%) inside one
    # contest — the pooled average hid the over-exposure.
    records = [
        {"source_file": "a.csv", "contest_id": "1",
         "user_lineups": [{"players": ["Hot Guy", f"A{i}"]} for i in range(4)]
                          + [{"players": ["Z", "Y"]}]},
        {"source_file": "b.csv", "contest_id": "2",
         "user_lineups": [{"players": [f"B{i}", "C"]} for i in range(5)]},
    ]
    a = adherence.grade_adherence(
        {"calls": [{"name": "Hot Guy", "verdict": "lean_fade"}]}, records)
    call = a["calls"][0]
    assert call["followed"] is True
    assert call["over_in"] == ["a.csv"]
    assert a["per_contest_flags"] == 1
    assert "over-exposed inside a.csv" in adherence.adherence_md(a)


def test_single_contest_slate_skips_per_contest_bookkeeping():
    a = adherence.grade_adherence(
        {"calls": [{"name": "X", "verdict": "underweight"}]},
        [{"source_file": "only.csv",
          "user_lineups": [{"players": ["A", "B"]}, {"players": ["C", "D"]}]}])
    assert "by_contest" not in a["calls"][0]
    assert a["per_contest_flags"] == 0


def test_logged_contest_ids_and_trend_block():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prior_root = history._REPO_ROOT
        history._REPO_ROOT = root
        try:
            d = root / "rules" / "test_slug"
            d.mkdir(parents=True)
            (d / "autopsy_data.jsonl").write_text(
                json.dumps({"contest_id": "123"}) + "\n"
                + json.dumps({"contest_id": None}) + "\n"
                + json.dumps({"source_file": "legacy row, no id"}) + "\n")
            assert history.logged_contest_ids("test_slug") == {"123"}

            # trend block: needs >=2 rows, renders the sequences
            assert history.process_trend_block("test_slug") is None
            rows = [
                {"best_percentile": 27.1, "edge_leverage_capture": 0.0,
                 "edge_bust_exposure": 0.5, "shark_gap_top": {"dim": "leverage_pct"},
                 "adherence_fades_violated": 1},
                {"best_percentile": 4.0, "edge_leverage_capture": 0.0,
                 "edge_bust_exposure": 0.2, "shark_gap_top": {"dim": "leverage_pct"},
                 "adherence_fades_violated": 0},
            ]
            (d / "results.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            block = history.process_trend_block("test_slug")
            assert block and "Process trend" in block
            assert "27.1 → 4.0" in block, block
            assert "0% → 0%" in block  # leverage capture sequence
            assert "leverage_pct" in block  # recurring shark-gap axis
            assert "1 → 0" in block  # adherence sequence
        finally:
            history._REPO_ROOT = prior_root


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
