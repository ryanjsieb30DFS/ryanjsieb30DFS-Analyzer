"""The post-autopsy review must review the slate it SAYS it will.

The bug this pins: the UI and the runner each called `latest_history_dir(slug)`
independently, so nothing tied the run to the directory the user was shown. With
unlogged CSVs sitting in the uploader, the review ran twice against a week-old
archived slate and gave no indication. `run_apply_proposals` had the same shape, so
Approve could apply a different review than the one displayed.
"""
import inspect

from src import analysis_runner


def test_both_runners_accept_an_explicit_hist_dir():
    for fn in (analysis_runner.run_autopsy_review,
               analysis_runner.run_apply_proposals):
        params = inspect.signature(fn).parameters
        assert "hist_dir" in params, f"{fn.__name__} must take an explicit hist_dir"
        assert params["hist_dir"].default is None, (
            f"{fn.__name__}: hist_dir must default to None so the plain "
            "latest-archive behaviour still works when no dir is passed")


def test_runner_honors_the_passed_dir_over_the_latest_archive(tmp_path, monkeypatch):
    """The pinned dir must win. Without this, a slate logged between render and
    click silently retargets the run."""
    pinned = tmp_path / "2020-01-01__pinned"
    pinned.mkdir()
    newest = tmp_path / "2099-12-31__newest"
    newest.mkdir()
    # analysis_runner imports latest_history_dir INSIDE the function, so patch it
    # on src.history (the source module) rather than on analysis_runner.
    from src import history
    monkeypatch.setattr(history, "latest_history_dir", lambda slug: newest)
    seen = {}

    def _fake_run(prompt, out_path, collateral=None):
        seen["out"] = out_path
        return {"ok": True, "error": None, "duration_s": 0.0, "cost_usd": None}

    monkeypatch.setattr(analysis_runner, "_run_claude", _fake_run)

    analysis_runner.run_autopsy_review("mma_se", "MMA", "mma", hist_dir=pinned)
    assert seen["out"].parent == pinned, (
        f"reviewed {seen['out'].parent.name}, not the pinned {pinned.name}")

    # Omitting it falls back to the newest archive — unchanged behaviour.
    seen.clear()
    analysis_runner.run_autopsy_review("mma_se", "MMA", "mma")
    assert seen["out"].parent == newest
