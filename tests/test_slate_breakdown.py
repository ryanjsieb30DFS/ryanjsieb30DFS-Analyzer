"""The archived-slate breakdown.

Exists because every numeric read the autopsy produced was invisible: bound to the
uploader (gone on Clear), rendered once from session state at log time (gone on
restart), or written to JSON and never displayed. A user who logged an autopsy and
asked "where is the breakdown?" had nowhere to look.
"""
import json
from pathlib import Path

import pytest

from src.slate_breakdown import (breakdown_md, results_md, lineups_md,
                                 retro_grade_md, list_archives, archive_label,
                                 has_review, review_md)

_REAL = (Path(__file__).parent.parent / "rules" / "mma_se" / "history"
         / "2026-07-26__ufc-fight-night-ankalaev-vs-guskov-7-25-26")


def test_results_md_renders_each_contest():
    md = results_md({
        "slate_label": "UFC Test",
        "contests": [
            {"name": "A", "type": "SE", "field_size": 490, "my_entries": 1,
             "best_rank": 72, "best_percentile": 14.7},
            {"name": "B", "type": "3-Max", "field_size": 594, "my_entries": 3,
             "best_rank": 21, "best_percentile": 3.5},
        ],
        "best_percentile": 3.5, "total_buy_in": 29.0, "entries_total": 4,
    })
    assert "UFC Test" in md
    assert "top 14.7%" in md and "top 3.5%" in md
    assert "490" in md and "594" in md
    assert "$29 in" in md
    assert results_md(None) is None
    assert results_md({"contests": []}) is None


def test_lineups_md_sorts_best_finish_first():
    md = lineups_md({"lineups": {"n_top_10pct": 1, "lineups": [
        {"entry_name": "worst", "points": 300.0, "percentile": 71.0, "avg_own": 32.2},
        {"entry_name": "best", "points": 587.3, "percentile": 3.5, "avg_own": 33.5},
    ]}})
    assert md.index("best") < md.index("worst"), "best finish must come first"
    assert "top 3.5%" in md and "1 of 2 finished in the top 10%" in md
    assert lineups_md(None) is None


def test_retro_grade_md_says_when_the_checks_did_not_work():
    """The whole point of the retro grade is self-validation: flagged lineups
    should finish WORSE. When they finish better, the gates are miscalibrated and
    the user needs to be told, not left to infer it."""
    # Flagged finished worse (higher percentile) -> checks worked.
    worked = retro_grade_md({"gradable": True, "lineups": [
        {"percentile": 60.0, "flags": [{"msg": "too chalky"}]},
        {"percentile": 10.0, "flags": []},
    ]})
    assert "the checks worked" in worked
    assert "too chalky" in worked
    # Flagged finished BETTER -> must say the gates want recalibrating.
    broke = retro_grade_md({"gradable": True, "lineups": [
        {"percentile": 5.0, "flags": [{"msg": "too chalky"}]},
        {"percentile": 80.0, "flags": []},
    ]})
    assert "did NOT work" in broke and "recalibrating" in broke
    # Nothing flagged is a distinct, valid outcome.
    none_flagged = retro_grade_md({"gradable": True, "lineups": [
        {"percentile": 5.0, "flags": []}, {"percentile": 9.0, "flags": []}]})
    assert "No lineup was flagged" in none_flagged
    assert retro_grade_md(None) is None
    assert retro_grade_md({"gradable": False}) is None


def test_sections_degrade_independently(tmp_path):
    """Older archives are missing files newer versions write. One absent file must
    omit its section, never blank the whole breakdown."""
    d = tmp_path / "2026-01-01__partial"
    d.mkdir()
    (d / "results.json").write_text(json.dumps({
        "slate_label": "Partial", "contests": [
            {"name": "X", "type": "SE", "field_size": 100, "my_entries": 1,
             "best_rank": 5, "best_percentile": 5.0}]}))
    md = breakdown_md(d)
    assert "Partial" in md and "top 5.0%" in md
    # Nothing at all -> an explanation, not an empty string or a crash.
    empty = tmp_path / "2026-01-02__empty"
    empty.mkdir()
    assert "No archived numbers" in breakdown_md(empty)
    assert "missing from disk" in breakdown_md(tmp_path / "does-not-exist")


def test_corrupt_json_does_not_break_the_view(tmp_path):
    d = tmp_path / "2026-01-03__corrupt"
    d.mkdir()
    (d / "results.json").write_text("{not json")
    (d / "accuracy.json").write_text(json.dumps({"lineups": {"lineups": [
        {"entry_name": "ok", "points": 1.0, "percentile": 50.0}]}}))
    md = breakdown_md(d)
    assert "Your lineups" in md      # the good file still renders


def test_archives_listed_newest_first_with_labels():
    if not _REAL.exists():
        pytest.skip("real archive fixture not present")
    dirs = list_archives("mma_se")
    assert dirs, "expected archived MMA slates"
    names = [d.name for d in dirs]
    assert names == sorted(names, reverse=True), "newest first"
    assert _REAL.name == names[0]
    label = archive_label(_REAL)
    assert "Ankalaev" in label and "2026-07-26" in label


def test_the_real_7_26_ufc_archive():
    """Regression against the actual slate the user could not find on screen.
    These three numbers are the ones that were invisible."""
    if not _REAL.exists():
        pytest.skip("real archive fixture not present")
    md = breakdown_md(_REAL)
    assert "top 3.5%" in md                       # best finish
    assert "0 of 2" in md                          # leverage candidates rostered
    assert "Tier ordering BROKE" in md             # board tiers out of order
    for section in ("How it finished", "Your lineups", "Strategy adherence",
                    "tier calibration", "Shark gap", "Retro grade"):
        assert section in md, f"missing section: {section}"


def test_review_helpers():
    if not _REAL.exists():
        pytest.skip("real archive fixture not present")
    # This slate's review had not been run when the fixture was captured; either
    # state is valid, but the two helpers must agree with each other.
    assert has_review(_REAL) == (review_md(_REAL) is not None)
