"""The small-field home-game line is scoped away from NFL Showdown — SD is a
different game (5-20 entries in large-field lottos, framed by its own
strategy block), so the bundle must not tell Claude the home game is
SE/3-Max/5-Max on an nfl_sd run."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import bundle  # noqa: E402


def _contests(_slug):
    return [{"name": "Test", "type": "SE", "entries": 1, "entry_fee": 5.0,
             "prize_pool": 500.0, "field_size": 100, "payout_shape": "top-heavy"}]


def _summary(_slug):
    return {"n_contests": 1, "total_entries": 1}


def _build(slug, sport, tmp_path, monkeypatch):
    monkeypatch.setattr(bundle, "load_contests", _contests)
    monkeypatch.setattr(bundle, "portfolio_summary", _summary)
    monkeypatch.setattr(bundle, "_BUNDLE_DIR", tmp_path)
    return bundle.build_bundle(slug, "Test (SE)", sport).read_text()


def test_home_game_line_present_for_classic_and_absent_for_showdown(tmp_path, monkeypatch):
    classic = _build("nfl_classic", "nfl", tmp_path, monkeypatch)
    sd = _build("nfl_sd", "nfl", tmp_path, monkeypatch)
    assert "The home game is **small-field GPPs" in classic
    assert "The home game is **small-field GPPs" not in sd
    # Payout-shape pointer names a section that exists in the strategy prompt.
    assert "`## Slate at a glance`" in classic
    assert "`## How to approach the slate`" not in classic
