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


# Controlled vocabulary: DK entry-cap types. The Analyzer's HOME GAME is
# small-field GPPs — Single Entry, 3-Max, and 5-Max (the FOCUS set below).
# 7/29/26 (MME plan Phase 1): the large-field types (20-Max mini-MAX and
# 150-Max MME) are now DECLARABLE and LOGGABLE as a separate parallel track —
# but they never blend into the small-field machinery: the sharp envelope,
# grading calibration, dossier, and the results-trend headline all gate on
# FOCUS_CONTEST_TYPES membership and stay sealed.
CONTEST_TYPES = {
    "SE":      {"default_max_entries": 1},
    "3-Max":   {"default_max_entries": 3},
    "5-Max":   {"default_max_entries": 5},
    "20-Max":  {"default_max_entries": 20},
    "150-Max": {"default_max_entries": 150},
}

# The focus set — imported where downstream code must gate on "is this an
# in-scope small-field contest". Deliberately NOT frozenset(CONTEST_TYPES):
# the MME types exist in the vocabulary but never in the focus set.
FOCUS_CONTEST_TYPES = frozenset({"SE", "3-Max", "5-Max"})

# The large-field track (the MME plan's field-exploitation game).
MME_CONTEST_TYPES = frozenset({"20-Max", "150-Max"})


def infer_type(entry_names) -> str | None:
    """Infer a contest's entry-cap type straight from the standings, so the type is
    NEVER lost to a manual step. DK EntryNames carry a `(n/m)` suffix; the MAX `m`
    across all entrants = the contest's max-entry cap (at least one entrant maxes in
    a real GPP). Maps to the smallest cap that fits: SE(1) / 3-Max(≤3) / 5-Max(≤5) /
    20-Max(≤20) / 150-Max(above). Defaults to SE when there is no multi-entry
    suffix at all."""
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
    if max_m <= 20:
        return "20-Max"
    return "150-Max"


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


def canonical_contest_name(slug: str, name: str) -> str:
    """Snap a declared-contest name to the Sim's name for the same contest.

    9/6/26 user directive (contest names sync across both tools): the Sim is
    the naming authority. On the 9/5 MMA slate the user typed "UFC $4k
    Clinch" while the Sim knew "UFC $4K Clinch [Single Entry]"; every
    name-keyed join downstream (picker check, override outcomes) went empty.
    If a Sim contest or pushed-pool label matches this name on the shared
    join key, the stored name becomes the Sim's (type tags like "(SE)"
    stripped — they are pool-label decoration, not part of the DK name).
    No match (or no Sim repo) keeps the typed name unchanged."""
    from src.lineup_selection import _contest_join_key
    from src import sim_link

    key = _contest_join_key(name)
    if not key:
        return name
    labels: list[str] = []
    try:
        labels += sim_link.sim_contest_names(slug)
    except Exception:  # noqa: BLE001 — canonicalizing must never block a save
        pass
    try:
        pool = sim_link.load_sim_pool(slug) or {}
        labels += [str(c.get("label") or "") for c in pool.get("contests") or []]
    except Exception:  # noqa: BLE001
        pass
    for lab in labels:
        if lab and _contest_join_key(lab) == key:
            canon = re.sub(
                r"\s*\((se|3-?max|5-?max|20-?max|150-?max|mme)\)\s*$",
                "", lab, flags=re.I).strip()
            return canon or name
    return name


# ---------------------------------------------------------------------------
# Payout ladders (9/6/26 contest-tab parity: the Sim tab's format is the
# canonical one, and the user wants the payout structure in both tools).
# Both functions are VERBATIM ports from the Sim repo — parser from
# src/contests_db.py, classifier from src/analyzer_link.py — so a ladder
# pastes and classifies identically in either tool.
# ---------------------------------------------------------------------------

_LADDER_LINE = re.compile(
    r"^\s*(\d[\d,]*)\s*(?:st|nd|rd|th)?\s*"
    r"(?:[-–to ]+(\d[\d,]*)\s*(?:st|nd|rd|th)?)?"
    r"\s*[:\s]\s*\$?\s*([\d,]+(?:\.\d+)?)\s*$",
    re.IGNORECASE,
)


def parse_dk_payout_text_with_diagnostics(
    text: str,
) -> tuple[list[tuple[int, int, float]], list[tuple[int, str]]]:
    """Parse a DK payout-ladder paste into (parsed_ladder, failed_lines).

    failed_lines = [(line_no_1based, raw_text), ...] for non-blank lines that
    didn't match — the UI names exactly which lines need fixing."""
    ladder: list[tuple[int, int, float]] = []
    failed: list[tuple[int, str]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        m = _LADDER_LINE.match(line)
        if not m:
            failed.append((i, raw))
            continue
        start = int(m.group(1).replace(",", ""))
        end = int(m.group(2).replace(",", "")) if m.group(2) else start
        payout = float(m.group(3).replace(",", ""))
        if end < start:
            start, end = end, start
        ladder.append((start, end, payout))
    return ladder, failed


def payout_shape_from_ladder(ladder) -> str | None:
    """Classify payout shape from the real ladder: first place's share of the
    total prize money. ~10-15% = Top-heavy GPP; barely-above-min-cash = Flat.
    Vocabulary matches the declaration dropdown. None without a usable
    ladder — never guess."""
    try:
        rows = [(int(a), int(b), float(p)) for a, b, p in (ladder or [])
                if float(p) > 0]
    except (TypeError, ValueError):
        return None
    if not rows:
        return None
    total = sum((b - a + 1) * p for a, b, p in rows)
    if total <= 0:
        return None
    first = max((p for a, b, p in rows if a == 1), default=None)
    if first is None:
        return None
    share = first / total
    if share >= 0.08:
        return "Top-heavy"
    if share <= 0.03:
        return "Flat"
    return "Balanced"


def update_contest(slug: str, contest_id: str, updates: dict) -> None:
    """Update fields on one declared contest in place (id and name are not
    updatable — the name is the cross-tool join key, set at declare time)."""
    contests = load_contests(slug)
    for c in contests:
        if c.get("id") == contest_id:
            c.update({k: v for k, v in updates.items()
                      if k not in ("id", "name")})
            break
    _save(slug, contests)


def add_contest(slug: str, contest: dict) -> None:
    """Append a contest. Auto-fills id; snaps the name to the Sim's (see
    canonical_contest_name)."""
    contests = load_contests(slug)
    contest = dict(contest)
    if contest.get("name"):
        contest["name"] = canonical_contest_name(slug, str(contest["name"]))
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
