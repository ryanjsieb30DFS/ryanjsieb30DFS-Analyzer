"""Trimmed ledger views the headless runs read (src/lessons_view.py)."""
from src import lessons_view as lv


def _lessons():
    return [
        {"id": "x-2026-01-01-open", "born": "2026-01-01", "status": "hypothesis",
         "statement": "An open idea.", "confirmations": [],
         "contradictions": [{"date": "2026-02-01", "history_dir": "h", "note": "did not fire"}]},
        {"id": "x-2026-01-02-valid", "born": "2026-01-02", "status": "validated",
         "statement": "A proven idea.",
         "confirmations": [{"date": "2026-03-01", "history_dir": "h2", "note": "held"},
                           {"date": "2026-02-01", "history_dir": "h1", "note": "older"}]},
        {"id": "x-2026-01-03-cod", "born": "2026-01-03", "status": "codified",
         "statement": "SECRET codified text", "codified_in": "framework.md — Rule 4"},
        {"id": "x-2026-01-04-ret", "born": "2026-01-04", "status": "retired",
         "statement": "RETIRED text", "retired_reason": "gone"},
    ]


def test_open_view_has_only_open_lessons_plus_codified_ids():
    md = lv.render_open_lessons(_lessons(), "mma_se")
    assert "## x-2026-01-01-open" in md and "## x-2026-01-02-valid" in md
    assert "confirmations: 0 · contradictions: 1" in md
    assert "latest note: contradiction 2026-02-01: did not fire" in md
    assert "latest note: confirmation 2026-03-01: held" in md   # newest, not first
    assert "SECRET codified text" not in md and "RETIRED text" not in md
    assert "`x-2026-01-03-cod` — framework.md — Rule 4" in md
    assert "x-2026-01-04-ret" not in md


def test_recent_autopsies_keeps_preamble_and_last_n():
    text = "# Autopsies\nintro\n\n" + "".join(f"## 2026-01-0{i} — slate {i}\nbody {i}\n\n"
                                            for i in range(1, 9))
    out = lv.recent_autopsy_entries(text, n=3)
    assert out.startswith("# Autopsies\nintro")
    assert "slate 5" not in out and "slate 6" in out and "slate 8" in out
    assert "last 3 of 8" in out


def test_writers_regenerate_files(tmp_path, monkeypatch):
    monkeypatch.setattr(lv, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr("src.ledger_hygiene._REPO_ROOT", tmp_path)
    d = tmp_path / "rules" / "mma_se"; d.mkdir(parents=True)
    (d / "lessons.yaml").write_text("lessons:\n  - id: a-2026-01-01-b\n    born: '2026-01-01'\n"
                                    "    status: hypothesis\n    statement: hi\n")
    (d / "autopsies.md").write_text("## one\n\n## two\n")
    assert lv.write_open_lessons("mma_se").read_text().count("## a-2026-01-01-b") == 1
    assert "## two" in lv.write_recent_autopsies("mma_se", n=1).read_text()
    assert lv.write_open_lessons("nascar") is None   # no ledger, nothing written


def test_runs_regenerate_views_before_shelling_out(monkeypatch):
    from src import analysis_runner as ar
    calls = []
    monkeypatch.setattr(ar, "refresh_trimmed_views", lambda slug: calls.append(slug))
    monkeypatch.setattr(ar, "build_bundle", lambda *a, **k: "bundle.md")
    monkeypatch.setattr(ar, "_run_claude", lambda *a, **k: {"ok": True})
    ar.run_analysis("mma_se", "UFC", "mma")
    assert calls == ["mma_se"]


def test_strategy_prompt_reads_trimmed_views_not_full_ledgers(monkeypatch):
    from src import analysis_runner as ar
    captured = {}
    monkeypatch.setattr(ar, "refresh_trimmed_views", lambda slug: None)
    monkeypatch.setattr(ar, "build_bundle", lambda *a, **k: "bundle.md")
    monkeypatch.setattr(ar, "_run_claude",
                        lambda prompt, *a, **k: captured.setdefault("p", prompt) and {"ok": True})
    ar.run_analysis("mma_se", "UFC", "mma")
    p = captured["p"]
    assert "rules/mma_se/lessons_open.md" in p and "rules/mma_se/autopsies_recent.md" in p
    assert "rules/mma_se/lessons.yaml" not in p and "rules/mma_se/autopsies.md`" not in p
