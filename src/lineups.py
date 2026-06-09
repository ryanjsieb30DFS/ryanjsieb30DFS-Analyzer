"""Persisted hand-built lineups.

Claude writes data/lineups/<slug>.md (via the Analyze tab's "Build lineups"
button, which runs headless claude -p). This module just reads + clears it,
mirroring src/slate_analysis.py.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

_LINEUPS_DIR = Path(__file__).parent.parent / "data" / "lineups"


def load_lineups(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None if no file exists."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def clear_lineups(slug: str) -> None:
    """Delete the file. Called after an autopsy log so the next slate starts fresh."""
    p = _LINEUPS_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()
