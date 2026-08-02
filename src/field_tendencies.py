"""Cumulative field-tendencies store — the "moving forward" substrate for the
Field/Fish autopsy analysis.

Each logged autopsy appends one compact row per contest to
`rules/<slug>/field_tendencies.jsonl` (append-only, NOT cleared with the slate,
like results.jsonl). Rows carry both a `contest_type` and a `contest_name`/
`contest_key` (the specific recurring contest), plus a `contest_id` (the DK
contest instance) used to DEDUP re-logs — `_load` collapses rows sharing a
`contest_id` to the latest, so re-uploading the same standings never inflates the
"in N of M" reliability counts. Two rollups read through it: `summarize` (by
type) and the sharper `summarize_contest` (by name — the same contest = the same
field). Both surface "the field reliably crowds X / Y is a recurring fish trap"
in the autopsy panel; `bundle_block` forward-feeds the same synthesis into the
next slate's bundle so the slate strategy can leverage AWAY from the crowd.
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
           profile: dict, date: str, contest_name: str | None = None,
           contest_id: str | None = None,
           sim_capture: dict | None = None) -> bool:
    """Append one contest's field tendencies. Returns True if written; skips a
    non-gradable profile. `contest_name` (the declared contest's name) enables the
    SPECIFIC-contest rollup (`summarize_contest`); without it only the by-type
    rollup applies. `contest_id` (the DK contest instance id) is stored for dedup."""
    if not profile or not profile.get("gradable"):
        return False
    win = profile.get("winners_profile") or {}
    fish = profile.get("fish_profile") or {}
    row = {
        "date": date,
        "contest_type": contest_type or "unknown",
        "contest_name": contest_name or None,
        "contest_key": contest_key(contest_name),
        "contest_id": contest_id,
        "field_size": field_size,
        # {name, own} since 7/31/26 — the ownership LEVEL the field piled into
        # is the transferable read (rosters turn over; bands don't). Legacy
        # rows are bare name strings; every reader handles both.
        "crowded_players": [{"name": c["name"], "own": c.get("field_own")}
                            for c in profile.get("crowded_players", [])[:8]],
        "crowded_combos": [c["players"] for c in profile.get("crowded_combos", [])[:5]],
        "fish_traps": [t["name"] for t in profile.get("fish_traps", [])[:8]],
        "top_opponents": [{"handle": o["handle"], "percentile": o.get("percentile")}
                          for o in (profile.get("top_opponents") or [])[:15]],
        "winners_avg_own": win.get("avg_own_per_slot"),
        "winners_unique_pct": win.get("unique_pct"),
        "fish_avg_own": fish.get("avg_own_per_slot"),
    }
    # Roster-level structure from the Sim's full-field capture, when one
    # exists for this contest — real dupe stats + dead-structure share the
    # standings-only profile can't see. Extra keys; old rows unaffected.
    if sim_capture:
        for k in ("unique_pct", "max_dupe", "pct_single_entry_users",
                  "mean_entries_per_user", "top3_chalk_lineup_pct",
                  "dead_structure_pct", "match_method"):
            if sim_capture.get(k) is not None:
                row[f"capture_{k}"] = sim_capture[k]
    p = _path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(row) + "\n")
    return True


def _dedup(rows: list[dict]) -> list[dict]:
    """Collapse re-logs of the SAME contest instance. Rows sharing a non-null
    `contest_id` (the DK contest instance) keep only the LATEST by `date` — so
    re-uploading a standings CSV and re-logging never double-counts and inflates
    the "in N of M" reliability numbers. Rows without a `contest_id` (older schema
    or non-DK-filename logs) pass through unchanged. Order is otherwise preserved."""
    latest: dict[str, dict] = {}
    for r in rows:
        cid = r.get("contest_id")
        if cid and (cid not in latest or (r.get("date") or "") >= (latest[cid].get("date") or "")):
            latest[cid] = r
    out = []
    for r in rows:
        cid = r.get("contest_id")
        if not cid:
            out.append(r)
        elif latest.get(cid) is r:
            out.append(r)
    return out


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
    return _dedup(out)


def _crowd_entries(r: dict) -> list[tuple]:
    """A row's crowded players as (name, own-or-None) tuples — new rows store
    {name, own} dicts, legacy rows bare strings."""
    out = []
    for c in (r.get("crowded_players") or []):
        if isinstance(c, dict):
            nm = c.get("name")
            if nm:
                out.append((str(nm), c.get("own")))
        elif c:
            out.append((str(c), None))
    return out


def _crowd_shape(rows: list[dict]) -> dict | None:
    """The transferable read (7/31/26, user direction): the ownership PATTERN
    the field piles into, independent of which names wore it. Player names
    rotate off the slate (MMA rosters turn over ~100% per card); the shape —
    how many names the field crowds and at what ownership level — persists."""
    sizes, owns = [], []
    for r in rows:
        entries = _crowd_entries(r)
        if entries:
            sizes.append(len(entries))
        owns += [o for _, o in entries if isinstance(o, (int, float))]
    if not sizes:
        return None
    out = {"avg_crowd_size": round(sum(sizes) / len(sizes), 1)}
    if owns:
        owns.sort()
        out["own_median"] = round(float(owns[len(owns) // 2]), 1)
        out["own_min"] = round(float(owns[0]), 1)
        out["own_max"] = round(float(owns[-1]), 1)
    return out


def _row_pairs(r: dict) -> set[tuple]:
    """A row's crowded pairs as order-stable sorted tuples (dupe-magnet PAIRS —
    the two-player stacks the field piles into together)."""
    out = set()
    for pair in (r.get("crowded_combos") or []):
        ps = pair.get("players") if isinstance(pair, dict) else pair
        if ps and len(ps) == 2:
            out.add(tuple(sorted(str(p) for p in ps)))
    return out


_CAPTURE_FIELDS = ("unique_pct", "max_dupe", "pct_single_entry_users",
                   "mean_entries_per_user", "top3_chalk_lineup_pct",
                   "dead_structure_pct")


def _capture_structure(rows: list[dict]) -> dict | None:
    """Median roster-level structure across the rows that carry a Sim capture.

    `log_contest` writes these `capture_*` keys from the Sim's full-field
    capture, but until 7/25/26 NOTHING read them back — so the stated goal of
    the capture bridge ("field reliably does X" reads carrying roster-level
    evidence) was never actually implemented; the data just accumulated on disk.
    Returns None when no row has any capture, so the caller stays silent rather
    than implying evidence it doesn't have."""
    out: dict = {}
    for f in _CAPTURE_FIELDS:
        vals = sorted(r[f"capture_{f}"] for r in rows
                      if isinstance(r.get(f"capture_{f}"), (int, float)))
        if vals:
            out[f] = round(float(vals[len(vals) // 2]), 1)
            out[f"{f}_n"] = len(vals)
    return out or None


def _capture_structure_str(s: dict) -> str:
    """One plain-language sentence about the field's real roster structure."""
    cap = (s or {}).get("capture_structure")
    if not cap:
        return ""
    bits = []
    if cap.get("unique_pct") is not None:
        bits.append(f"only **{cap['unique_pct']}% of entries were unique rosters**")
    if cap.get("max_dupe") is not None:
        bits.append(f"the most-copied lineup appeared **{int(cap['max_dupe'])} times**")
    if cap.get("mean_entries_per_user") is not None:
        bits.append(f"the average opponent entered **{cap['mean_entries_per_user']} "
                    f"lineups**")
    if cap.get("pct_single_entry_users") is not None:
        bits.append(f"**{cap['pct_single_entry_users']}% of opponents were "
                    f"single-entry**")
    if cap.get("top3_chalk_lineup_pct") is not None:
        bits.append(f"the top-3 chalk players landed together in "
                    f"**{cap['top3_chalk_lineup_pct']}%** of lineups")
    if cap.get("dead_structure_pct") is not None:
        bits.append(f"**{cap['dead_structure_pct']}%** of entries carried a "
                    f"structurally dead build")
    if not bits:
        return ""
    n = max((v for k, v in cap.items() if k.endswith("_n")), default=0)
    return (f"from the full-field captures ({n} contest{'s' if n != 1 else ''}): "
            + ", ".join(bits))


def summarize(slug: str, contest_type: str | None) -> dict | None:
    """Across past contests of this type, which players/traps the field RELIABLY
    crowds (appeared in ≥2 contests). None when there's no prior history."""
    rows = [r for r in _load(slug)
            if contest_type and r.get("contest_type") == contest_type]
    if len(rows) < 2:  # need repetition before calling something "reliable"
        return None
    crowd_ct: Counter = Counter()
    trap_ct: Counter = Counter()
    pair_ct: Counter = Counter()
    for r in rows:
        for nm in {nm for nm, _ in _crowd_entries(r)}:
            crowd_ct[nm] += 1
        for nm in set(r.get("fish_traps") or []):
            trap_ct[nm] += 1
        for pr in _row_pairs(r):
            pair_ct[pr] += 1
    n = len(rows)
    return {
        "n_contests": n,
        "capture_structure": _capture_structure(rows),
        "crowd_shape": _crowd_shape(rows),
        "reliably_crowded": [{"name": nm, "in_n": c, "of": n}
                             for nm, c in crowd_ct.most_common(8) if c >= 2],
        "recurring_traps": [{"name": nm, "in_n": c, "of": n}
                            for nm, c in trap_ct.most_common(8) if c >= 2],
        "recurring_pairs": [{"players": list(pr), "in_n": c, "of": n}
                            for pr, c in pair_ct.most_common(5) if c >= 2],
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
    pair_ct: Counter = Counter()
    for r in rows:
        for nm in {nm for nm, _ in _crowd_entries(r)}:
            crowd_ct[nm] += 1
        for nm in set(r.get("fish_traps") or []):
            trap_ct[nm] += 1
        for o in (r.get("top_opponents") or []):
            h = o.get("handle") if isinstance(o, dict) else o
            if h:
                opp_ct[h] += 1
        for pr in _row_pairs(r):
            pair_ct[pr] += 1

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
        "capture_structure": _capture_structure(rows),
        "crowd_shape": _crowd_shape(rows),
        "reliably_crowded": [{"name": nm, "in_n": c, "of": n}
                             for nm, c in crowd_ct.most_common(8) if c >= 2],
        "recurring_traps": [{"name": nm, "in_n": c, "of": n}
                            for nm, c in trap_ct.most_common(8) if c >= 2],
        "recurring_opponents": [{"handle": h, "in_n": c, "of": n}
                                for h, c in opp_ct.most_common(10) if c >= 2],
        "recurring_pairs": [{"players": list(pr), "in_n": c, "of": n}
                            for pr, c in pair_ct.most_common(5) if c >= 2],
        "winners_own_trend": _trend("winners_avg_own"),
        "winners_unique_trend": _trend("winners_unique_pct"),
    }


def _crowd_traps_str(s: dict, current_names: set | None = None) -> str:
    """Shape-first (7/31/26, user direction): the OWNERSHIP PATTERN the field
    piles into leads; specific player names appear ONLY when the player is on
    the current slate (`current_names`, normalized). Past names that rotated
    off the card collapse into the shape read — the strategy must never be
    asked to discuss a player who isn't playing."""
    from src.autopsy import _norm_name

    def _on_slate(nm: str) -> bool:
        return current_names is None or _norm_name(str(nm)) in current_names

    parts = []
    # SHAPE lead — always transferable, name-free.
    shape = s.get("crowd_shape")
    if shape:
        line = (f"SHAPE: the field reliably piles onto ~{shape['avg_crowd_size']:g} "
                f"names per contest")
        if shape.get("own_median") is not None:
            line += (f", arriving around {shape['own_median']:g}% ownership "
                     f"(range {shape['own_min']:g}-{shape['own_max']:g}%)")
        parts.append(line)
    crowd_all = s.get("reliably_crowded") or []
    crowd_on = [c for c in crowd_all if _on_slate(c["name"])]
    if crowd_on:
        crowd = ", ".join(f"{c['name']} (in {c['in_n']} of {c['of']})"
                          for c in crowd_on)
        parts.append(f"the field reliably crowds **{crowd}**")
    elif crowd_all and current_names is not None:
        parts.append(f"its {len(crowd_all)} past crowd name(s) are NOT on this "
                     f"card — apply the shape to THIS card's consensus favorites "
                     f"(sized in `## Chalk combos`)")
    traps_on = [t for t in (s.get("recurring_traps") or []) if _on_slate(t["name"])]
    if traps_on:
        traps = ", ".join(f"{t['name']} (in {t['in_n']} of {t['of']})"
                          for t in traps_on)
        parts.append(f"recurring fish-traps: **{traps}**")
    pairs_on = [p for p in (s.get("recurring_pairs") or [])
                if all(_on_slate(nm) for nm in p["players"])]
    if pairs_on:
        prs = ", ".join(f"{p['players'][0]} + {p['players'][1]} (in {p['in_n']} of {p['of']})"
                        for p in pairs_on)
        parts.append(f"the field PAIRS **{prs}** — a dupe-magnet stack; leverage lives "
                     f"in breaking it")
    if s.get("recurring_opponents"):
        # Opponent HANDLES are people, not slate players — never filtered.
        opps = ", ".join(f"{o['handle']} (in {o['in_n']} of {o['of']})"
                         for o in s["recurring_opponents"])
        parts.append(f"recurring opponents: {opps}")
    tr = s.get("winners_own_trend")
    if tr is not None and abs(tr) >= 1.0:
        parts.append(f"winners trending {'chalkier' if tr > 0 else 'sharper'} "
                     f"({tr:+} own/slot vs earlier)")
    # Roster-level structure from the Sim's full-field captures — the standings
    # profile can't see duplication or entries-per-user at all.
    cap_str = _capture_structure_str(s)
    if cap_str:
        parts.append(cap_str)
    return "; ".join(parts)


def _norm_name_set(current_names):
    """Normalized set of the loaded slate's player names, or None (= no filter)."""
    if current_names is None:
        return None
    from src.autopsy import _norm_name
    return {_norm_name(str(n)) for n in current_names}


def bundle_block(slug: str, contests, current_names=None) -> str | None:
    """Forward-feed block for the slate bundle. For each contest the user is entering,
    prefer the SPECIFIC-contest history (`summarize_contest`, keyed by name — the
    same contest = the same field) and fall back to the by-TYPE history
    (`summarize`) when the specific one has <2 logs. Returns a markdown block, or
    None when nothing has enough history. Pure synthesis — surfaces where the field
    crowds so the user can leverage AWAY; issues no play/fade command.

    `contests` = the declared-contest dicts (each with `name` + `type`).
    `current_names` = the loaded slate's player names; when given, past
    crowd/trap/pair NAMES render only if the player is on this slate —
    otherwise only the ownership SHAPE is surfaced (7/31/26)."""
    norm_now = _norm_name_set(current_names)
    seen_keys, seen_types, blocks = set(), set(), []
    for c in (contests or []):
        name = (c or {}).get("name")
        ctype = (c or {}).get("type")
        key = contest_key(name)
        # 1) Specific recurring contest (sharpest).
        if key and key not in seen_keys:
            seen_keys.add(key)
            sc = summarize_contest(slug, name)
            if sc and _crowd_traps_str(sc, norm_now):
                blocks.append(
                    f"- **{sc['contest_name']}** (your {sc['n_contests']} past logs of THIS "
                    f"contest): {_crowd_traps_str(sc, norm_now)}."
                )
                continue  # specific covers it; don't also emit the type row
        # 2) Fallback: by contest type.
        if ctype and ctype not in seen_types:
            seen_types.add(ctype)
            st_ = summarize(slug, ctype)
            if st_ and _crowd_traps_str(st_, norm_now):
                blocks.append(
                    f"- **{ctype}** (across your {st_['n_contests']} past {ctype} contests): "
                    f"{_crowd_traps_str(st_, norm_now)}."
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


def crowded_names(slug: str, contests, current_names=None) -> list[str]:
    """The reliably-crowded player names that `bundle_block` surfaces for this
    slate's declared contests — flat and de-duplicated. Uses the SAME select logic
    (specific recurring contest when it has enough history, else by type) and the
    SAME emit condition as `bundle_block`, so this is exactly the crowd set the
    bundle shows — never a superset. Empty when there's no field-tendency history.
    Powers the app's field-tendency coverage-gap check.

    `contests` = the declared-contest dicts (each with `name` + `type`)."""
    norm_now = _norm_name_set(current_names)
    seen_keys, seen_types, names = set(), set(), []

    def _add(summary):
        from src.autopsy import _norm_name
        for c in (summary.get("reliably_crowded") or []):
            nm = c.get("name")
            if not nm or nm in names:
                continue
            # On-slate only (7/31/26): the app must never warn about a player
            # who isn't on the current card.
            if norm_now is not None and _norm_name(str(nm)) not in norm_now:
                continue
            names.append(nm)

    for c in (contests or []):
        name = (c or {}).get("name")
        ctype = (c or {}).get("type")
        key = contest_key(name)
        if key and key not in seen_keys:
            seen_keys.add(key)
            sc = summarize_contest(slug, name)
            if sc and _crowd_traps_str(sc, norm_now):  # same emit test bundle_block uses
                _add(sc)
                continue
        if ctype and ctype not in seen_types:
            seen_types.add(ctype)
            st_ = summarize(slug, ctype)
            if st_ and _crowd_traps_str(st_, norm_now):
                _add(st_)
    return names
