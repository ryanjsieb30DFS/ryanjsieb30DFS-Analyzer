"""Living shark envelope accumulation: append + count-weighted, idempotent refresh."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import shark_accumulate as acc  # noqa: E402


def _seed_baseline(tmp_path):
    d = tmp_path / "rules" / "shared"
    d.mkdir(parents=True)
    (d / "shark_baseline.json").write_text(json.dumps({"sports": {"golf": {
        "n_with_sharks": 10,
        "shark_envelope": {"own_per_slot": 16.0, "leverage_pct": 50.0,
                           "anchor_exposure": 0.40, "unique_pct": 90.0},
    }}}))
    return d


def _point(monkeypatch, tmp_path):
    d = _seed_baseline(tmp_path)
    monkeypatch.setattr(acc, "_BASELINE_PATH", d / "shark_baseline.json")
    monkeypatch.setattr(acc, "_OBS_PATH", d / "shark_observations.jsonl")


def test_record_skips_incomplete(monkeypatch, tmp_path):
    _point(monkeypatch, tmp_path)
    assert acc.record_observation(None, {"gradable": True}, "s", "d") is False
    assert acc.record_observation("golf", {"gradable": False}, "s", "d") is False
    assert acc.record_observation("golf", {"gradable": True, "own_per_slot": 12.0,
                                           "leverage_pct": 80.0, "anchor_exposure": None,
                                           "unique_pct": 100.0}, "s", "d") is False


def test_refresh_blends_seed_and_observation(monkeypatch, tmp_path):
    _point(monkeypatch, tmp_path)
    prof = {"gradable": True, "own_per_slot": 12.0, "leverage_pct": 80.0,
            "anchor_exposure": 0.30, "unique_pct": 100.0, "n_entries": 20}
    assert acc.record_observation("golf", prof, "pga_classic", "2026-07-05") is True
    base = acc.refresh_baseline()
    env = base["sports"]["golf"]["shark_envelope"]
    # seed weight 10, one obs weight 1 -> (16*10 + 12)/11 = 15.636
    assert env["own_per_slot"] == round((16.0 * 10 + 12.0) / 11, 3)
    assert base["sports"]["golf"]["accumulated_contests"] == 1
    assert base["sports"]["golf"]["seed_envelope"]["own_per_slot"] == 16.0  # frozen


def test_refresh_is_idempotent(monkeypatch, tmp_path):
    _point(monkeypatch, tmp_path)
    acc.record_observation("golf", {"gradable": True, "own_per_slot": 12.0,
                                    "leverage_pct": 80.0, "anchor_exposure": 0.30,
                                    "unique_pct": 100.0}, "s", "d")
    first = acc.refresh_baseline()["sports"]["golf"]["shark_envelope"]["own_per_slot"]
    second = acc.refresh_baseline()["sports"]["golf"]["shark_envelope"]["own_per_slot"]
    assert first == second  # seed frozen -> re-run never double-counts
