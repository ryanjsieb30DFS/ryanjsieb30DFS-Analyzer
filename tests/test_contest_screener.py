"""Contest screener: your record in contests shaped like the declared ones."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.contest_selection import screen_declared, screen_md  # noqa: E402


def _rows():
    """A small ledger: 6 SE <500 contests, 1 150-Max 10k+ contest."""
    base = {"date": "2026-08-01", "slug": "mma_se", "sport": "mma",
            "my_entries": 1, "entry_fee": 5, "buy_in": 5, "winnings": None,
            "roi_pct": None, "best_rank": 10}
    rows = [{**base, "slate_label": f"S{i}", "name": f"C{i}", "type": "SE",
             "field_size": 400, "field_bucket": "<500",
             "best_percentile": p}
            for i, p in enumerate([5.0, 20.0, 35.0, 50.0, 8.0, 60.0])]
    rows.append({**base, "slate_label": "S9", "name": "Big", "type": "150-Max",
                 "field_size": 20000, "field_bucket": "10k+",
                 "best_percentile": 1.0, "my_entries": 10})
    return pd.DataFrame(rows)


def test_screen_matches_most_specific_shape_first():
    recs = screen_declared(
        [{"name": "Tonight SE", "type": "SE", "field_size": 390},
         {"name": "New 5-Max", "type": "5-Max", "field_size": 390},
         {"name": "Alien", "type": "20-Max", "field_size": 3000}],
        _rows())
    se, five, alien = recs
    assert se["basis"] == "same type + field size" and se["n"] == 6
    assert se["median_pctile"] == 27.5 and not se["thin"]
    assert se["top10_rate"] == 33.0          # 2 of 6 finishes at or under 10
    # No 5-Max history at all -> widened to the field-size bucket; the basis
    # label is what carries that caveat (6 rows, so not numerically thin).
    assert five["basis"] == "same field size" and five["n"] == 6
    assert not five["thin"]
    # Nothing comparable in any direction.
    assert alien["n"] == 0 and alien["basis"] is None


def test_screen_md_is_honest_about_samples_and_entry_counts():
    md = screen_md(screen_declared(
        [{"name": "Tonight SE", "type": "SE", "field_size": 390},
         {"name": "Big MME", "type": "150-Max", "field_size": 20000}],
        _rows()))
    assert "lower is better" in md.lower()
    assert "⚠️ thin" in md                    # the 1-contest 150-Max history
    # The best-of-N-entries caveat must ride the table — a multi-entry shape's
    # record always looks better than a single-entry shape's.
    assert "10 tries" in md
    assert "not a command" in md
