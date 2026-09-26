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
    # contest_type became a focus gate 7/18 — an in-focus type is required.
    assert acc.record_observation("golf", prof, "pga_classic", "2026-07-05",
                                  contest_type="SE") is True
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


def test_observed_envelope_is_per_slug_and_unseeded(monkeypatch, tmp_path):
    """9/26/26: two live NFL Classic slates at 19.6 / 17.4 must read as 18.5, not
    the seed-blended 14 — and a golf row for the same sport family must not leak in."""
    _point(monkeypatch, tmp_path)
    rows = [
        {"slug": "nfl_classic", "sport": "nfl", "contest_id": "1", "contest_type": "SE",
         "own_per_slot": 19.6, "leverage_pct": 66.7, "anchor_exposure": 0.8, "unique_pct": 100.0},
        {"slug": "nfl_classic", "sport": "nfl", "contest_id": "2", "contest_type": "3-Max",
         "own_per_slot": 17.4, "leverage_pct": 100.0, "anchor_exposure": 0.4, "unique_pct": 77.8},
        {"slug": "nfl_classic", "sport": "nfl", "contest_id": "3", "contest_type": "20-Max",
         "own_per_slot": 40.0, "leverage_pct": 0.0, "anchor_exposure": 1.0, "unique_pct": 50.0},
        {"slug": "pga_classic", "sport": "golf", "contest_id": "4", "contest_type": "SE",
         "own_per_slot": 9.0, "leverage_pct": 100.0, "anchor_exposure": 0.1, "unique_pct": 100.0},
    ]
    acc._OBS_PATH.parent.mkdir(parents=True, exist_ok=True)
    acc._OBS_PATH.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    obs = acc.observed_envelope("nfl_classic")
    assert obs["n"] == 2                      # the 20-Max row is out of focus
    assert obs["own_per_slot"] == 18.5
    assert obs["own_per_slot_values"] == [19.6, 17.4]
    assert acc.observed_envelope("nascar") is None


def test_summarize_pro_filters_by_sport(monkeypatch, tmp_path):
    """youdacao's NFL line must not be his golf median."""
    from src import shark_dossier as sd
    p = tmp_path / "shark_dossier.jsonl"
    rows = [
        {"handle": "youdacao", "sport": "golf", "slug": "pga_classic", "date": "2026-08-11",
         "contest_id": "a", "own_per_slot": 17.6, "leverage_pct": 50, "anchor_exposure": 0.3, "best_pctile": 5},
        {"handle": "youdacao", "sport": "nfl", "slug": "nfl_classic", "date": "2026-09-13",
         "contest_id": "b", "own_per_slot": 16.9, "leverage_pct": 100, "anchor_exposure": 0.5, "best_pctile": 80},
        {"handle": "youdacao", "sport": "nfl", "slug": "nfl_classic", "date": "2026-09-26",
         "contest_id": "c", "own_per_slot": 18.7, "leverage_pct": 100, "anchor_exposure": 0.5, "best_pctile": 79},
    ]
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    monkeypatch.setattr(sd, "_DOSSIER_PATH", p)
    assert sd.summarize_pro("youdacao")["n_contests"] == 3
    nfl = sd.summarize_pro("youdacao", "nfl")
    assert nfl["n_contests"] == 2 and nfl["sports"] == ["nfl"]
    assert nfl["median_own_per_slot"] == 18.7
    assert "17.6" not in sd.dossier_md("nfl")
