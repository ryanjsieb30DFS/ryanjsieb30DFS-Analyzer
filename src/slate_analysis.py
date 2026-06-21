"""Slate strategy persistence.

The persisted markdown at data/slate_analysis/<slug>.md is the written slate
strategy — Claude writes it from the uploaded articles + strategy docs, and the
Slate Strategy tab renders it.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path


_ANALYSIS_DIR = Path(__file__).parent.parent / "data" / "slate_analysis"


def load_persisted(slug: str) -> dict | None:
    """Return {'markdown': str, 'mtime': str} or None if no file exists."""
    p = _ANALYSIS_DIR / f"{slug}.md"
    if not p.exists():
        return None
    return {
        "markdown": p.read_text(),
        "mtime": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
    }


def save_persisted(slug: str, markdown: str) -> None:
    """Write data/slate_analysis/<slug>.md. Called by Claude, not the UI."""
    _ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    (_ANALYSIS_DIR / f"{slug}.md").write_text(markdown)


def clear_persisted(slug: str) -> None:
    """Delete the file. Called after an autopsy log so the next slate starts fresh."""
    p = _ANALYSIS_DIR / f"{slug}.md"
    if p.exists():
        p.unlink()
