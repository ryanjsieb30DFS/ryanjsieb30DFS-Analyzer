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


def contest_key(name) -> str:
    """Stable identity for a recurring contest — matches contest_templates._norm
    (casefolded, stripped) so the same declared/saved contest keys consistently
    across slates. Empty string when there's no usable name."""
    return str(name).strip().casefold() if name else ""


def record(slug: str, contest_type: str | None, field_size: int,
           profile: dict, date: str, contest_name: str | None = None) -> bool:
    """Append one contest's field tendencies. Returns True if written; skips a
    non-gradable profile. `contest_name` (the declared contest's name) enables the
    SPECIFIC-contest rollup (`summarize_contest`); without it only the by-type
    rollup applies."""
    if not profile or not profile.get("gradable"):
        return False
    win = profile.get("winners_profile") or {}
    fish = profile.get("fish_profile") or {}
    row = {
        "date": date,
        "contest_type": contest_type or "unknown",
        "contest_name": contest_name or None,
        "contest_key": contest_key(contest_name),
        "field_size": field_size,
        "crowded_players": [c["name"] for c in profile.get("crowded_players", [])[:8]],
        "crowded_combos": [c["players"] for c in profile.get("crowded_combos", [])[:5]],
        "fish_traps": [t["name"] for t in profile.get("fish_traps", [])[:8]],
        "top_opponents": [{"handle": o["handle"], "percentile": o.get("percentile")}
                          for o in (profile.get("top_opponents") or [])[:15]],
        "winners_avg_own": win.get("avg_own_per_slot"),
        "winners_unique_pct": win.get("unique_pct"),
        "fish_avg_own": fish.get("avg_own_per_slot"),
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


def summarize_contest(slug: str, name) -> dict | None:
    """Across past logs of ONE specific recurring contest (keyed by name), the
    field's reliable tendencies: crowded players, recurring fish-traps, recurring
    OPPONENTS (handles that keep showing up), and the sharpness trend (are winners
    running more/less chalk over time). None until ≥2 logs of that contest exist.
    Sharper than `summarize` (by-type) because the same contest = the same field."""
    key = contest_key(name)
    if not key:
        return None
    rows = [r for r in _load(slug) if r.get("contest_key") == key]
    if len(rows) < 2:
        return None
    rows.sort(key=lambda r: r.get("date") or "")
    n = len(rows)
    crowd_ct: Counter = Counter()
    trap_ct: Counter = Counter()
    opp_ct: Counter = Counter()
    for r in rows:
        for nm in set(r.get("crowded_players") or []):
            crowd_ct[nm] += 1
        for nm in set(r.get("fish_traps") or []):
            trap_ct[nm] += 1
        for o in (r.get("top_opponents") or []):
            h = o.get("handle") if isinstance(o, dict) else o
            if h:
                opp_ct[h] += 1

    # Sharpness trend: winners' avg ownership, earlier half vs later half.
    def _trend(field: str):
        vals = [r.get(field) for r in rows if r.get(field) is not None]
        if len(vals) < 2:
            return None
        half = len(vals) // 2 or 1
        older = sum(vals[:half]) / half
        newer = sum(vals[half:]) / (len(vals) - half)
        return round(newer - older, 1)

    return {
        "n_contests": n,
        "contest_name": next((r.get("contest_name") for r in reversed(rows)
                              if r.get("contest_name")), None) or name,
        "reliably_crowded": [{"name": nm, "in_n": c, "of": n}
                             for nm, c in crowd_ct.most_common(8) if c >= 2],
        "recurring_traps": [{"name": nm, "in_n": c, "of": n}
                            for nm, c in trap_ct.most_common(8) if c >= 2],
        "recurring_opponents": [{"handle": h, "in_n": c, "of": n}
                                for h, c in opp_ct.most_common(10) if c >= 2],
        "winners_own_trend": _trend("winners_avg_own"),
        "winners_unique_trend": _trend("winners_unique_pct"),
    }


def _crowd_traps_str(s: dict) -> str:
    parts = []
    if s.get("reliably_crowded"):
        crowd = ", ".join(f"{c['name']} (in {c['in_n']} of {c['of']})"
                          for c in s["reliably_crowded"])
        parts.append(f"the field reliably crowds **{crowd}**")
    if s.get("recurring_traps"):
        traps = ", ".join(f"{t['name']} (in {t['in_n']} of {t['of']})"
                          for t in s["recurring_traps"])
        parts.append(f"recurring fish-traps: **{traps}**")
    if s.get("recurring_opponents"):
        opps = ", ".join(f"{o['handle']} (in {o['in_n']} of {o['of']})"
                         for o in s["recurring_opponents"])
        parts.append(f"recurring opponents: {opps}")
    tr = s.get("winners_own_trend")
    if tr is not None and abs(tr) >= 1.0:
        parts.append(f"winners trending {'chalkier' if tr > 0 else 'sharper'} "
                     f"({tr:+} own/slot vs earlier)")
    return "; ".join(parts)


def bundle_block(slug: str, contests) -> str | None:
    """Forward-feed block for the slate bundle. For each contest the user is entering,
    prefer the SPECIFIC-contest history (`summarize_contest`, keyed by name — the
    same contest = the same field) and fall back to the by-TYPE history
    (`summarize`) when the specific one has <2 logs. Returns a markdown block, or
    None when nothing has enough history. Pure synthesis — surfaces where the field
    crowds so the user can leverage AWAY; issues no play/fade command.

    `contests` = the declared-contest dicts (each with `name` + `type`)."""
    seen_keys, seen_types, blocks = set(), set(), []
    for c in (contests or []):
        name = (c or {}).get("name")
        ctype = (c or {}).get("type")
        key = contest_key(name)
        # 1) Specific recurring contest (sharpest).
        if key and key not in seen_keys:
            seen_keys.add(key)
            sc = summarize_contest(slug, name)
            if sc and _crowd_traps_str(sc):
                blocks.append(
                    f"- **{sc['contest_name']}** (your {sc['n_contests']} past logs of THIS "
                    f"contest): {_crowd_traps_str(sc)}."
                )
                continue  # specific covers it; don't also emit the type row
        # 2) Fallback: by contest type.
        if ctype and ctype not in seen_types:
            seen_types.add(ctype)
            st_ = summarize(slug, ctype)
            if st_ and _crowd_traps_str(st_):
                blocks.append(
                    f"- **{ctype}** (across your {st_['n_contests']} past {ctype} contests): "
                    f"{_crowd_traps_str(st_)}."
                )
    if not blocks:
        return None
    return (
        "## Field tendencies — how the field plays YOUR contests\n"
        "FORWARD-LOOKING, accumulated from your logged autopsies (specific contest when there's "
        "enough history, else by contest type). The field reliably piles into these — that is where "
        "leverage-AWAY lives, and the recurring opponents are who you're actually beating. Surface "
        "it as a tension; do NOT tell the user to fade anyone.\n"
        + "\n".join(blocks)
    )
