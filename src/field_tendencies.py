"""Cumulative field-tendencies store — the "moving forward" substrate for the
Field/Fish autopsy analysis.

Each logged autopsy appends one compact row per contest to
`rules/<slug>/field_tendencies.jsonl` (append-only, NOT cleared with the slate,
like results.jsonl). Keyed by `contest_type` — the "specific contests" dimension
the user cares about ($5 mini-MAX fields play fishier than $1K single-entry).
`summarize` rolls the history for a contest type into "the field reliably crowds
X / Y is a recurring fish trap," surfaced in the autopsy panel when prior rows
exist. (Auto-feeding this into the next slate's strategy is a deferred follow-up.)
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent


def _path(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "field_tendencies.jsonl"


def record(slug: str, contest_type: str | None, field_size: int,
           profile: dict, date: str) -> bool:
    """Append one contest's field tendencies. Returns True if written; skips a
    non-gradable profile."""
    if not profile or not profile.get("gradable"):
        return False
    row = {
        "date": date,
        "contest_type": contest_type or "unknown",
        "field_size": field_size,
        "crowded_players": [c["name"] for c in profile.get("crowded_players", [])[:8]],
        "crowded_combos": [c["players"] for c in profile.get("crowded_combos", [])[:5]],
        "fish_traps": [t["name"] for t in profile.get("fish_traps", [])[:8]],
        "winners_avg_own": (profile.get("winners_profile") or {}).get("avg_own_per_slot"),
        "fish_avg_own": (profile.get("fish_profile") or {}).get("avg_own_per_slot"),
    }
    p = _path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(row) + "\n")
    return True


def _load(slug: str) -> list[dict]:
    p = _path(slug)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def summarize(slug: str, contest_type: str | None) -> dict | None:
    """Across past contests of this type, which players/traps the field RELIABLY
    crowds (appeared in ≥2 contests). None when there's no prior history."""
    rows = [r for r in _load(slug)
            if contest_type and r.get("contest_type") == contest_type]
    if len(rows) < 2:  # need repetition before calling something "reliable"
        return None
    crowd_ct: Counter = Counter()
    trap_ct: Counter = Counter()
    for r in rows:
        for nm in set(r.get("crowded_players") or []):
            crowd_ct[nm] += 1
        for nm in set(r.get("fish_traps") or []):
            trap_ct[nm] += 1
    n = len(rows)
    return {
        "n_contests": n,
        "reliably_crowded": [{"name": nm, "in_n": c, "of": n}
                             for nm, c in crowd_ct.most_common(8) if c >= 2],
        "recurring_traps": [{"name": nm, "in_n": c, "of": n}
                            for nm, c in trap_ct.most_common(8) if c >= 2],
    }
