"""Load per-sport strategy docs and recent autopsy lessons.

Surfaces the contents of rules/<slug>/{philosophy,framework,autopsies}.md plus
the tail of rules/<slug>/autopsy_data.jsonl so the UI can render strategy
context alongside every slate analysis.
"""
from __future__ import annotations

import json
from pathlib import Path

_RULES_DIR = Path(__file__).parent.parent / "rules"


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def load_strategy(slug: str) -> dict:
    """Return the active sport's strategy bundle.

    Keys:
      philosophy, framework, autopsies   -> raw markdown (empty string if missing)
      recent_lessons                     -> list[dict] of last 5 autopsy_data.jsonl entries (newest first)
      track_files                        -> list[str] for slug=="nascar"; empty otherwise
    """
    sport_dir = _RULES_DIR / slug
    bundle = {
        "philosophy": _read(sport_dir / "philosophy.md"),
        "framework": _read(sport_dir / "framework.md"),
        "autopsies": _read(sport_dir / "autopsies.md"),
        "recent_lessons": _recent_lessons(sport_dir / "autopsy_data.jsonl"),
        "track_files": _nascar_tracks() if slug == "nascar" else [],
    }
    return bundle


def _recent_lessons(jsonl_path: Path, n: int = 5) -> list[dict]:
    if not jsonl_path.exists():
        return []
    rows: list[dict] = []
    for line in jsonl_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return list(reversed(rows[-n:]))


def _nascar_tracks() -> list[str]:
    tracks_dir = _RULES_DIR / "nascar" / "tracks"
    if not tracks_dir.exists():
        return []
    return sorted(
        p.stem for p in tracks_dir.glob("*.md") if p.stem.lower() != "readme"
    )


def load_track(track_slug: str) -> str:
    """Return the markdown for a specific NASCAR track."""
    return _read(_RULES_DIR / "nascar" / "tracks" / f"{track_slug}.md")


def load_shared(name: str) -> str:
    """Return the markdown for a shared rule doc (e.g., 'anchor_equivalence')."""
    return _read(_RULES_DIR / "shared" / f"{name}.md")
