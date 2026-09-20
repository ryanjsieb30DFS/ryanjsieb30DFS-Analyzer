"""MME-only nights store best_percentile=None with best_percentile_mme set
(9/15 MNF, 9/19 MEGA). Trend readers fall back; the jsonl is never rewritten."""
from src import history
from src.slate_breakdown import results_md


def test_headline_percentile_falls_back_to_mme():
    assert history.headline_percentile({"best_percentile": 4.2, "best_percentile_mme": 1.0}) == 4.2
    assert history.headline_percentile({"best_percentile": None, "best_percentile_mme": 1.8}) == 1.8
    assert history.headline_percentile({"best_percentile": None}) is None
    assert history.headline_rank({"best_rank": None, "best_rank_mme": 584}) == 584


def test_process_trend_block_uses_fallback(monkeypatch):
    rows = [{"date": "2026-09-06", "best_percentile": 12.0},
            {"date": "2026-09-19", "best_percentile": None, "best_percentile_mme": 1.8}]
    monkeypatch.setattr(history, "load_results", lambda slug, n=None: rows)
    md = history.process_trend_block("mma_se")
    assert "12.0 → 1.8" in md


def test_results_md_headline_uses_fallback():
    res = {"slate_label": "MEGA", "best_percentile": None, "best_percentile_mme": 1.8,
           "contests": [{"name": "MEGA", "type": "MME", "field_size": 30000,
                         "my_entries": 100, "best_rank": 584, "best_percentile": 1.8}]}
    assert "top 1.8%" in results_md(res)


def test_real_ledgers_have_no_null_headline_after_fallback():
    for slug in ("mma_se", "nfl_sd"):
        for r in history.load_results(slug):
            if r.get("best_percentile") is None and r.get("best_percentile_mme") is not None:
                assert history.headline_percentile(r) is not None
