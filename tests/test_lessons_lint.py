"""Ledger integrity lint + rot report (src/lessons_lint.py) and the
ledger_hygiene promote / retire paths that were untested."""
import pytest

from src import lessons_lint as ll
from src import ledger_hygiene as lh

SLUGS = ("pga_classic", "pga_rd4_sd", "mma_se", "nascar", "nfl_sd", "nfl_classic")


@pytest.mark.parametrize("slug", SLUGS)
def test_every_current_ledger_is_clean(slug):
    assert ll.lint_lessons(slug) == []


def _ok():
    return {"id": "mma-se-2026-01-05-x", "born": "2026-01-05", "status": "hypothesis",
            "statement": "s", "confirmations": [], "contradictions": [],
            "codified_in": None, "retired_reason": None}


def test_lint_catches_each_violation():
    a = _ok(); b = _ok()                                     # duplicate id
    c = dict(_ok(), id="c", status="maybe")                  # bad status
    d = dict(_ok(), id="d", confirmations=[{"note": "no date"}])
    e = dict(_ok(), id="e", confirmations=[{"date": "2026-01-01", "history_dir": "h"}])  # before born
    f = dict(_ok(), id="f", status="codified", codified_in=None)
    g = dict(_ok(), id="g", contradictions=[{"date": "2026-02-01"}])   # no history pointer
    errs = ll.lint_lessons_list([a, b, c, d, e, f, g])
    joined = "\n".join(errs)
    assert "duplicate id" in joined
    assert "status 'maybe'" in joined
    assert "d: confirmations[0] has no YYYY-MM-DD date" in joined
    assert "before born" in joined
    assert "f: codified but codified_in is empty" in joined
    assert "g: contradictions[0] has no history_dir" in joined


def test_lint_accepts_every_history_key_spelling():
    for key in ("history_dir", "origin_dir", "history", "slate"):
        l = dict(_ok(), confirmations=[{"date": "2026-01-06", key: "x", "note": "n"}])
        assert ll.lint_lessons_list([l]) == []


def test_lint_on_disk_reports_broken_yaml(tmp_path, monkeypatch):
    monkeypatch.setattr(ll, "_REPO_ROOT", tmp_path)
    d = tmp_path / "rules" / "mma_se"; d.mkdir(parents=True)
    d.joinpath("lessons.yaml").write_text("lessons: [unclosed\n")
    assert any("does not parse" in e for e in ll.lint_lessons("mma_se"))
    assert ll.lint_lessons("nascar") == []          # missing ledger is clean


def test_legacy_ids_warn_not_fail():
    assert ll.is_dated_slug_id("nfl-classic-2026-09-19-te-bring-back")
    assert ll.is_dated_slug_id("mma-se-2026-05-09-verify-submission-before-lock")
    assert not ll.is_dated_slug_id("nfl_classic_te_bring_back")
    assert ll.lint_lessons_list([dict(_ok(), id="nfl_classic_te_bring_back")]) == []


def test_review_prompt_carries_ledger_discipline_and_id_convention(monkeypatch, tmp_path):
    from src import analysis_runner as ar
    captured = {}
    monkeypatch.setattr(ar, "refresh_trimmed_views", lambda slug: None)
    monkeypatch.setattr(ar, "_run_claude",
                        lambda prompt, *a, **k: captured.setdefault("p", prompt) and
                        captured.setdefault("kw", k) and {"ok": True})
    ar.run_autopsy_review("nfl_classic", "NFL Classic", "nfl", hist_dir=tmp_path)
    p = captured["p"]
    assert "at most 2 NEW" in p
    assert "MUST get a confirmation OR a contradiction" in p
    assert "prefer CONFIRMING or CONTRADICTING an EXISTING" in p
    assert "`nfl-classic-YYYY-MM-DD-<short-kebab>`" in p
    assert callable(captured["kw"]["post_check"])


def _rows(dates):
    return [{"date": d} for d in dates]


def test_rot_report_lists_only_unchecked_hypotheses_after_3_slates(tmp_path, monkeypatch):
    monkeypatch.setattr(lh, "_REPO_ROOT", tmp_path)
    d = tmp_path / "rules" / "mma_se"; d.mkdir(parents=True)
    d.joinpath("lessons.yaml").write_text("""lessons:
  - {id: old-unchecked, born: "2026-01-01", status: hypothesis, statement: a}
  - {id: old-checked, born: "2026-01-01", status: hypothesis, statement: b,
     contradictions: [{date: "2026-02-01", history_dir: h, note: n}]}
  - {id: new-unchecked, born: "2026-03-01", status: hypothesis, statement: c}
  - {id: valid-unchecked, born: "2026-01-01", status: validated, statement: d}
""")
    rows = _rows(["2026-01-10", "2026-02-10", "2026-02-20", "2026-03-05"])
    rot = ll.rot_report("mma_se", rows)
    assert [r["id"] for r in rot] == ["old-unchecked"]
    assert rot[0]["slates_since"] == 4
    assert "old-unchecked" in ll.rot_report_md(rot)
    assert "nothing is rotting" in ll.rot_report_md([])


# --- ledger_hygiene promote / retire paths --------------------------------

def test_hygiene_promotion_bar_at_three_confirming_slates():
    two = {"id": "a", "status": "hypothesis", "statement": "x",
           "confirmations": [{"date": "2026-01-02"}]}                 # origin + 1 = 2
    three = {"id": "b", "status": "validated", "statement": "y",
             "confirmations": [{"date": "2026-01-02"}, {"date": "2026-01-03"}]}  # 3
    done = dict(three, id="c", status="codified")
    assert lh.confirming_slates(two) == 2 and lh.confirming_slates(three) == 3
    assert [x["id"] for x in lh.near_promotion([two, three, done])] == ["a"]
    assert [x["id"] for x in lh.overdue_promotion([two, three, done])] == ["b"]


def test_hygiene_stale_hypotheses_retire_path():
    stale = {"id": "s", "status": "hypothesis", "born": "2026-01-01", "statement": "x",
             "confirmations": []}
    fresh_but_confirmed = dict(stale, id="c", confirmations=[{"date": "2026-01-05"}])
    retired = dict(stale, id="r", status="retired")
    rows = _rows(["2026-01-10", "2026-01-20", "2026-01-30"])
    out = lh.stale_hypotheses([stale, fresh_but_confirmed, retired], rows,
                              min_slates=3, min_days=10_000)
    assert [x["id"] for x in out] == ["s"] and out[0]["slates_since"] == 3
    # Two slates is not yet a fair shot.
    assert lh.stale_hypotheses([stale], rows[:2], min_slates=3, min_days=10_000) == []
