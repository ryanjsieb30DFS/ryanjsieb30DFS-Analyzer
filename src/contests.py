"""Per-sport contest registry.

User declares which contests they're entering for the active slate. Claude
reads this when writing slate analysis and lineups so the recommendations
respect contest field sizes, entry counts, and ceiling targets.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path


_CONTESTS_DIR = Path(__file__).parent.parent / "data" / "contests"


# Controlled vocabulary: DK entry-cap types. The Analyzer is focused on
# small-field GPPs — Single Entry, 3-Max, and 5-Max only. Everything downstream
# (slate strategy, sharp envelope, field analysis) optimizes for this set; the
# 150-max MME game is a different animal and is intentionally out of scope.
CONTEST_TYPES = {
    "SE":     {"default_max_entries": 1},
    "3-Max":  {"default_max_entries": 3},
    "5-Max":  {"default_max_entries": 5},
}

# The focus set (also the keys above) — imported where downstream code must
# gate on "is this an in-scope small-field contest".
FOCUS_CONTEST_TYPES = frozenset(CONTEST_TYPES)


def _path(slug: str) -> Path:
    return _CONTESTS_DIR / f"{slug}.json"


def load_contests(slug: str) -> list[dict]:
    p = _path(slug)
    if not p.exists():
        return []
    return json.loads(p.read_text()).get("contests", [])


def _save(slug: str, contests: list[dict]) -> None:
    _CONTESTS_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps({"contests": contests}, indent=2))


def add_contest(slug: str, contest: dict) -> None:
    """Append a contest. Auto-fills id."""
    contests = load_contests(slug)
    contest = dict(contest)
    contest["id"] = uuid.uuid4().hex[:8]
    contests.append(contest)
    _save(slug, contests)


def remove_contest(slug: str, contest_id: str) -> None:
    contests = [c for c in load_contests(slug) if c.get("id") != contest_id]
    _save(slug, contests)


def clear_contests(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()


def portfolio_summary(slug: str) -> dict:
    """Roll up: contest count, total entries, unique lineups needed."""
    contests = load_contests(slug)
    if not contests:
        return {"n_contests": 0, "total_entries": 0, "unique_lineups_needed": 0}
    return {
        "n_contests": len(contests),
        "total_entries": sum(int(c.get("my_entries", 0)) for c in contests),
        # Unique lineups = MAX of my_entries across contests (DK allows reusing
        # a lineup across distinct contests, so the max is the count we need to build).
        "unique_lineups_needed": max((int(c.get("my_entries", 0)) for c in contests), default=0),
    }
