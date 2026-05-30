"""Hand-built lineups persistence.

Same pattern as slate_analysis persisted markdown: Claude writes the file,
the Lineups tab renders it. Cleared automatically when an autopsy is logged.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path


_LINEUPS_DIR = Path(__file__).parent.parent / "data" / "lineups"


def load_lineups(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def save_lineups(slug: str, markdown: str) -> None:
    """Write data/lineups/<slug>.md. Called by Claude, not the UI."""
    _LINEUPS_DIR.mkdir(parents=True, exist_ok=True)
    (_LINEUPS_DIR / f"{slug}.md").write_text(markdown)


def clear_lineups(slug: str) -> None:
    """Delete the file. Called after autopsy log so next slate starts fresh."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()
