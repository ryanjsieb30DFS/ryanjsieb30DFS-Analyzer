"""Per-sport contest registry.

User declares which contests they're entering for the active slate. Claude
reads this when writing slate analysis and lineups so the recommendations
respect contest field sizes, entry counts, and ceiling targets.
"""
from __future__ import annotations

import json
import re
import uuid
from pathlib import Path


_CONTESTS_DIR = Path(__file__).parent.parent / "data" / "contests"

# DK EntryName multi-entry suffix, e.g. "ryanfeller (3/3)" → this entrant's 3rd of 3.
_ENTRY_SUFFIX = re.compile(r"\((\d+)\s*/\s*(\d+)\)\s*$")


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


def infer_type(entry_names) -> str | None:
    """Infer a contest's entry-cap type straight from the standings, so the type is
    NEVER lost to a manual step. DK EntryNames carry a `(n/m)` suffix; the MAX `m`
    across all entrants = the contest's max-entry cap (at least one entrant maxes in
    a real GPP). Maps to the smallest focus cap that fits: SE(1)/3-Max(≤3)/5-Max(≤5).
    Returns None when the cap is outside the focus set (20/150-max MME); defaults to
    SE when there is no multi-entry suffix at all."""
    max_m = 1
    for nm in (entry_names if entry_names is not None else []):
        match = _ENTRY_SUFFIX.search(str(nm))
        if match:
            max_m = max(max_m, int(match.group(2)))
    if max_m <= 1:
        return "SE"
    if max_m <= 3:
        return "3-Max"
    if max_m <= 5:
        return "5-Max"
    return None  # out of focus (MME)


def auto_link(csv_infos, declared, tol: float = 0.15) -> dict:
    """Auto-assign uploaded standings CSVs to declared contests — one-to-one, so no
    manual dropdown. Matches by field-size closeness (within `tol`), preferring a
    same-inferred-type match, then the closest field. Never assigns one declared
    contest to two CSVs.

    `csv_infos`: list of {'name', 'field_size', 'inferred_type'}.
    `declared`:  list of contest dicts (name / type / field_size).
    Returns {csv_name: declared_contest_dict_or_None}."""
    result = {ci["name"]: None for ci in csv_infos}
    pairs = []
    for ci in csv_infos:
        cf = ci.get("field_size") or 0
        for d in (declared or []):
            df = d.get("field_size") or 0
            if not cf or not df:
                continue
            rel = abs(cf - df) / df
            if rel > tol:
                continue
            type_match = 0 if (ci.get("inferred_type") and d.get("type")
                               and ci["inferred_type"] == d["type"]) else 1
            pairs.append((type_match, rel, ci["name"], d))
    pairs.sort(key=lambda p: (p[0], p[1]))  # same-type first, then closest field
    used_csv, used_contest = set(), set()
    for _tm, _rel, csv_name, d in pairs:
        did = d.get("id") or d.get("name")
        if csv_name in used_csv or did in used_contest:
            continue
        result[csv_name] = d
        used_csv.add(csv_name)
        used_contest.add(did)
    return result


def contest_id_from_filename(name) -> str | None:
    """DK contest-standings files are named `contest-standings-<ID>.csv`; return the
    ID (a stable per-instance key for dedup). None when the name doesn't match."""
    m = re.search(r"contest-standings-(\d+)", str(name))
    return m.group(1) if m else None


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
