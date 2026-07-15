"""Per-pro shark dossier — track the SPECIFIC humans who beat you, over time.

`shark_accumulate` keeps an AGGREGATE per-sport envelope ("the sharks collectively
run ~16% own/slot"). This module keeps the individual record: every autopsy where a
tracked handle is in-field, it appends one row per NAMED pro to
`rules/shared/shark_dossier.jsonl` with that pro's structural fingerprint AND your
own side of the same contest, so we can say "moklovin has been in 3 of your MMA
slates, always max-anchors the chalk with zero leverage, and beat you 2 of 3."

Two more jobs:
  - `promotion_candidates` / `promote` — AUTO-DISCOVERY: the handles that keep
    finishing top of YOUR contests (from `field_tendencies` top_opponents) but
    aren't on the watchlist yet get surfaced, and promotion appends them to the
    `shark_handles_learned.yaml` overlay (never rewrites the curated watchlist).
  - `shark_reality_block` — forward-feeds the observed envelope + named-pro
    patterns into the slate bundle, so the strategy's sharp-envelope target
    reflects what the pros actually did in your contests, not just the static
    playbook.

Per the [[feedback_play_like_sharks]] goal. Tracking + synthesis only — never a
play/fade command. Re-logs collapse by (handle, contest_id) so counts never inflate.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from src.contests import FOCUS_CONTEST_TYPES
from src.shark_accumulate import FEATURES

_SHARED = Path(__file__).parent.parent / "rules" / "shared"
_DOSSIER_PATH = _SHARED / "shark_dossier.jsonl"
_BASELINE_PATH = _SHARED / "shark_baseline.json"


def _dedup(rows: list[dict]) -> list[dict]:
    """Collapse re-logs of the same pro in the same contest: rows sharing a
    (handle, contest_id) keep only the LATEST by date. Rows without a contest_id
    pass through unchanged (older/non-DK-filename logs)."""
    latest: dict[tuple, dict] = {}
    for r in rows:
        cid = r.get("contest_id")
        if not cid:
            continue
        k = (str(r.get("handle", "")).lower(), cid)
        if k not in latest or (r.get("date") or "") >= (latest[k].get("date") or ""):
            latest[k] = r
    out = []
    for r in rows:
        cid = r.get("contest_id")
        if not cid:
            out.append(r)
        elif latest.get((str(r.get("handle", "")).lower(), cid)) is r:
            out.append(r)
    return out


def _load_dossier() -> list[dict]:
    if not _DOSSIER_PATH.exists():
        return []
    out = []
    for line in _DOSSIER_PATH.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return _dedup(out)


# ---------------------------------------------------------------- record --------
def record_pros(slug: str, sport: str | None, parsed: dict, gap: dict, date: str,
                contest_type: str | None, field_size: int,
                contest_id: str | None = None) -> int:
    """Append one per-pro row for each tracked shark in-field this contest. Returns
    how many were written. Gated to SE/3-Max/5-Max (the same small-field focus as
    the envelope). Each row carries the pro's structural fingerprint + YOUR side of
    the same contest + `beat_user` (did the pro's best entry out-finish yours)."""
    if not sport or contest_type not in FOCUS_CONTEST_TYPES:
        return 0
    from src import shark_gap as sg
    handles = (sg.load_handles().get("sharks_by_sport") or {}).get(sport, [])
    pros = sg.per_pro_profiles(parsed, handles)
    if not pros:
        return 0
    user = (gap or {}).get("user") or {}
    u_best = user.get("best_pctile")
    lines = []
    for handle, prof in pros.items():
        row = {"handle": handle, "sport": sport, "slug": slug, "date": date,
               "contest_type": contest_type, "contest_id": contest_id,
               "field_size": field_size}
        for f in FEATURES:
            row[f] = prof.get(f)
        row["best_pctile"] = prof.get("best_pctile")
        row["n_entries"] = prof.get("n_entries")
        row["user_own_per_slot"] = user.get("own_per_slot")
        row["user_leverage_pct"] = user.get("leverage_pct")
        row["user_anchor_exposure"] = user.get("anchor_exposure")
        row["user_best_pctile"] = u_best
        pb = prof.get("best_pctile")
        row["beat_user"] = bool(pb is not None and u_best is not None and pb < u_best)
        lines.append(json.dumps(row))
    if lines:
        _DOSSIER_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _DOSSIER_PATH.open("a") as f:
            f.write("\n".join(lines) + "\n")
    return len(lines)


# ---------------------------------------------------------------- rollups -------
def _pattern(p: dict) -> str:
    """A one-line read of how this pro plays, from their accumulated tendencies."""
    bits = []
    anc = p.get("anchor_tendency")
    if anc is not None and anc >= 0.8:
        bits.append("rides the chalk anchors")
    elif anc is not None and anc <= 0.4:
        bits.append("fades the chalk anchors")
    lev = p.get("leverage_rate")
    if lev is not None and lev >= 50:
        bits.append("carries a sub-5% leverage piece in most lineups")
    elif lev is not None and lev <= 15:
        bits.append("little-to-no leverage")
    own = p.get("median_own_per_slot")
    if own is not None:
        bits.append(f"~{own}% own/slot")
    return ", ".join(bits) if bits else "not enough signal yet"


def summarize_pro(handle: str) -> dict | None:
    """Roll one named pro's dossier across the contests they've appeared in:
    contests seen, sports, median own/slot, leverage rate, anchor tendency, their
    beat-you record, and a derived one-line pattern. None if never logged."""
    hl = str(handle).lower()
    rows = [r for r in _load_dossier() if str(r.get("handle", "")).lower() == hl]
    if not rows:
        return None
    rows.sort(key=lambda r: r.get("date") or "")
    n = len(rows)

    def _med(field):
        vals = sorted(r.get(field) for r in rows if r.get(field) is not None)
        return round(vals[len(vals) // 2], 1) if vals else None

    def _avg(field):
        vals = [r.get(field) for r in rows if r.get(field) is not None]
        return round(sum(vals) / len(vals), 2) if vals else None

    prof = {
        "handle": next((r.get("handle") for r in reversed(rows) if r.get("handle")), handle),
        "n_contests": n,
        "sports": sorted({r.get("sport") for r in rows if r.get("sport")}),
        "median_own_per_slot": _med("own_per_slot"),
        "leverage_rate": _avg("leverage_pct"),
        "anchor_tendency": _avg("anchor_exposure"),
        "median_best_pctile": _med("best_pctile"),
        "beat_user_n": sum(1 for r in rows if r.get("beat_user")),
        "beat_user_of": n,
    }
    prof["pattern"] = _pattern(prof)
    return prof


def dossier_md(sport: str) -> str | None:
    """A compact per-pro table for the Autopsy tab — the named humans in your
    <sport> contests and how they play vs you. None if no pros logged."""
    rows = [r for r in _load_dossier() if r.get("sport") == sport]
    if not rows:
        return None
    handles, seen = [], set()
    for r in rows:
        hl = str(r.get("handle", "")).lower()
        if hl and hl not in seen:
            seen.add(hl)
            handles.append(r.get("handle"))
    pros = [p for p in (summarize_pro(h) for h in handles) if p]
    if not pros:
        return None
    pros.sort(key=lambda p: (-p["beat_user_n"], p.get("median_best_pctile") or 100))
    out = ["### Named pros — how the sharks in your contests actually play",
           "| Pro | Seen | Beat you | Own/slot | Leverage% | Anchor | Pattern |",
           "|---|---|---|---|---|---|---|"]
    for p in pros:
        out.append(
            f"| **{p['handle']}** | {p['n_contests']} | {p['beat_user_n']}/{p['beat_user_of']} | "
            f"{p.get('median_own_per_slot')} | {p.get('leverage_rate')} | "
            f"{p.get('anchor_tendency')} | {p['pattern']} |"
        )
    return "\n".join(out)


# ------------------------------------------------------ auto-discovery ----------
def promotion_candidates(slug: str, min_contests: int = 2) -> list[dict]:
    """Recurring high-finishers in YOUR <slug> contests (from field_tendencies
    `top_opponents`) who keep showing up but AREN'T on the shark watchlist yet —
    the pros quietly beating you that nobody has flagged. Returns
    [{handle, sport, in_n, best_pctile}], most-recurring first."""
    from src import field_tendencies as ft
    from src import shark_gap as sg
    rows = ft._load(slug)  # already deduped by contest_id
    if not rows:
        return []
    cfg = sg.load_handles()
    sport = (cfg.get("slug_sport") or {}).get(slug)
    listed = {h.lower() for h in (cfg.get("sharks_by_sport") or {}).get(sport, [])}
    user = {u.lower() for u in (cfg.get("user") or [])}
    cnt: Counter = Counter()
    best: dict[str, float] = {}
    disp: dict[str, str] = {}
    for r in rows:
        seen_in_row = set()
        for o in (r.get("top_opponents") or []):
            h = o.get("handle") if isinstance(o, dict) else o
            if not h:
                continue
            hl = str(h).lower()
            if hl in listed or hl in user:
                continue
            disp.setdefault(hl, h)
            if hl not in seen_in_row:
                cnt[hl] += 1
                seen_in_row.add(hl)
            p = o.get("percentile") if isinstance(o, dict) else None
            if p is not None:
                best[hl] = min(best.get(hl, 100.0), p)
    return [{"handle": disp[hl], "sport": sport, "in_n": c,
             "best_pctile": round(best.get(hl, 100.0), 2)}
            for hl, c in cnt.most_common() if c >= min_contests]


def promote(sport: str, handle: str) -> bool:
    """Add a discovered handle to the `shark_handles_learned.yaml` overlay (unioned
    into the watchlist by `shark_gap.load_handles`). The curated `shark_handles.yaml`
    is left untouched. Returns False if sport/handle missing or already present."""
    if not sport or not handle:
        return False
    from src import shark_gap as sg
    import yaml
    data = {}
    if sg._LEARNED_PATH.exists():
        try:
            data = yaml.safe_load(sg._LEARNED_PATH.read_text()) or {}
        except Exception:  # noqa: BLE001
            data = {}
    if not isinstance(data, dict):
        data = {}
    lst = list(data.get(sport) or [])
    if handle.lower() in {x.lower() for x in lst}:
        return False
    lst.append(handle)
    data[sport] = lst
    sg._LEARNED_PATH.parent.mkdir(parents=True, exist_ok=True)
    sg._LEARNED_PATH.write_text(
        "# Auto-discovered shark handles promoted from recurring opponents.\n"
        "# Managed by the app (Autopsy tab); unioned into shark_handles.yaml by\n"
        "# shark_gap.load_handles(). Shape: {sport: [handles]}.\n"
        + yaml.safe_dump(data, sort_keys=True, default_flow_style=False)
    )
    return True


# ------------------------------------------------- forward-feed to bundle -------
def shark_reality_block(slug: str) -> str | None:
    """Forward-feed block for the slate bundle: the observed per-sport shark
    envelope (from `shark_baseline.json`) + the named-pro patterns. Mirrors
    `field_tendencies.bundle_block`. None when there's no shark history for the
    sport. Pure synthesis — the sharp-envelope is a descriptive target, not a
    command."""
    from src import shark_gap as sg
    sport = (sg.load_handles().get("slug_sport") or {}).get(slug)
    if not sport:
        return None
    env = user_env = None
    try:
        block = (json.loads(_BASELINE_PATH.read_text()).get("sports") or {}).get(sport) or {}
        env, user_env = block.get("shark_envelope"), block.get("user_envelope")
    except Exception:  # noqa: BLE001
        pass
    pros_md = dossier_md(sport)
    if not env and not pros_md:
        return None
    lines = [
        "## Shark reality — how the pros play YOUR contests",
        "FORWARD-LOOKING, accumulated from your logged autopsies. The observed "
        "sharp-envelope target for your small-field GPPs: match the STRUCTURE "
        "(own/slot, leverage rate, anchor discipline, all-unique). Surface it as the "
        "target; do NOT issue play/fade commands.",
    ]
    if env:
        line = (f"- **Your {sport} shark envelope:** own/slot **{env.get('own_per_slot')}**, "
                f"leverage **{env.get('leverage_pct')}%**, anchor-exposure **{env.get('anchor_exposure')}**, "
                f"unique **{env.get('unique_pct')}%**.")
        if user_env:
            line += (f" You run: own/slot {user_env.get('own_per_slot')}, "
                     f"leverage {user_env.get('leverage_pct')}%, anchor {user_env.get('anchor_exposure')} — "
                     f"that delta is the gap to close.")
        lines.append(line)
    if pros_md:
        lines.append("\n".join(l for l in pros_md.splitlines() if not l.startswith("### ")))
    return "\n".join(lines)
