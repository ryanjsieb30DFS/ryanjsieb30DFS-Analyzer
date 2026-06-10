"""Persisted Claude-written per-slate artifacts: lineups + red-team review.

Claude writes data/lineups/<slug>.md (Analyze tab "Build lineups" button) and
data/red_team/<slug>.md ("Red team the lineups" button) via headless claude -p.
This module just reads + clears them, mirroring src/slate_analysis.py.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

_LINEUPS_DIR = Path(__file__).parent.parent / "data" / "lineups"
_RED_TEAM_DIR = Path(__file__).parent.parent / "data" / "red_team"


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


def load_red_team(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None if no file exists."""
    p = _RED_TEAM_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def clear_red_team(slug: str) -> None:
    """Delete the file. Called after an autopsy log so the next slate starts fresh."""
    p = _RED_TEAM_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()
