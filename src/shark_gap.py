"""Shark-gap: quantify what the sharks do differently than us, structurally.

The self-grade (`src.accuracy`) measures OUTCOMES (did our bets pay off). This
module measures BEHAVIOR — the structural fingerprint that defines shark play
(ownership envelope, leverage rate, chalk-anchor exposure, lineup uniqueness) —
for any set of handles in a contest's standings, so we can put real numbers on
"what are the sharks doing differently than me" and trend convergence over time.

It reuses `src.autopsy.parse_dk_results` (its `{lineups, players}` shape), so it
runs on any DK contest-standings CSV. Everything here is pure/deterministic.

Per the [[feedback_play_like_sharks]] goal: the sharks are the benchmark; this
puts the gap on every measurable axis, per slate, per sport.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

from src.autopsy import _norm_name

_REPO_ROOT = Path(__file__).parent.parent
_HANDLES_PATH = _REPO_ROOT / "rules" / "shared" / "shark_handles.yaml"
_LEARNED_PATH = _REPO_ROOT / "rules" / "shared" / "shark_handles_learned.yaml"

# A play is a "leverage piece" below this field ownership; the sharks carry one
# in the majority of lineups (sharp_playbook: PGA 60-80%, NFL 64-86%).
_LEVERAGE_OWN = 5.0
# How many of the field's chalkiest plays count as the "chalk anchors" whose
# exposure the recurring leak under-weights (RD4 SD Fitzpatrick, NASCAR Reddick).
_N_ANCHORS = 3


def _handle(entry_name) -> str:
    return str(entry_name).split("(")[0].strip().lower()


def _lineups_for(parsed: dict, handles) -> list[list[str]]:
    """Rosters (list of player-name lists) for the given handles; handles=None
    matches nothing. Use the sentinel set to pull a specific player's entries."""
    wanted = {h.lower() for h in (handles or [])}
    L = parsed["lineups"]
    return [list(r) for r, h in zip(L["Lineup_parsed"], L["EntryName"].map(_handle))
            if h in wanted and r]


def _ranks_for(parsed: dict, handles) -> list[int]:
    wanted = {h.lower() for h in (handles or [])}
    L = parsed["lineups"]
    return [int(rk) for rk, h in zip(L["Rank"], L["EntryName"].map(_handle)) if h in wanted]


def chalk_anchors(parsed: dict, n: int = _N_ANCHORS) -> list[str]:
    """The field's n highest-owned plays (normalized names) — the chalk anchors
    whose exposure separates disciplined sharks from over-faders."""
    P = parsed["players"].dropna(subset=["actual_own"])
    top = P.sort_values("actual_own", ascending=False).head(n)
    return [_norm_name(x) for x in top["name"]]


def structural_profile(parsed: dict, handles, anchors: list[str] | None = None) -> dict:
    """The behavioral fingerprint for a set of handles in this contest.

    Dimensions (all field-ownership based, so they're decisions, not results):
      own_per_slot   — mean per-lineup average field own% (the envelope number)
      leverage_pct   — share of lineups carrying a sub-5%-owned play
      anchor_exposure— mean exposure across the slate's chalk anchors (0-1)
      max_overlap    — worst shared-player count between any two of their lineups
      unique_pct     — share of lineups with a distinct roster
      best/median_pctile — finish distribution
    Returns {gradable: False} if the handles have no lineups here.
    """
    field = len(parsed["lineups"])
    lineups = _lineups_for(parsed, handles)
    n = len(lineups)
    if not n:
        return {"gradable": False, "n_entries": 0}

    P = parsed["players"]
    own = {_norm_name(nm): o for nm, o in zip(P["name"], P["actual_own"])
           if o is not None and o == o}
    anchors = anchors if anchors is not None else chalk_anchors(parsed)

    norm_sets = [set(_norm_name(p) for p in lp) for lp in lineups]

    # ownership envelope: per-lineup average field own%, then mean over lineups
    per_lineup_own = []
    lev_hits = 0
    for lp in lineups:
        owns = [own.get(_norm_name(p)) for p in lp]
        owns = [o for o in owns if o is not None]
        if owns:
            per_lineup_own.append(sum(owns) / len(owns))
            if any(o < _LEVERAGE_OWN for o in owns):
                lev_hits += 1
    own_per_slot = round(sum(per_lineup_own) / len(per_lineup_own), 1) if per_lineup_own else None

    # chalk-anchor exposure: mean over anchors of (share of lineups rostering it)
    if anchors:
        anchor_exp = sum(
            sum(1 for s in norm_sets if a in s) / n for a in anchors
        ) / len(anchors)
        anchor_exposure = round(anchor_exp, 3)
        per_anchor = {a: round(sum(1 for s in norm_sets if a in s) / n, 3) for a in anchors}
    else:
        anchor_exposure, per_anchor = None, {}

    max_overlap = max((len(a & b) for a, b in combinations(norm_sets, 2)), default=0)
    unique_pct = round(len({frozenset(s) for s in norm_sets}) / n * 100, 1)

    ranks = _ranks_for(parsed, handles)
    pct = sorted(round(r / field * 100, 2) for r in ranks) if (ranks and field) else []

    return {
        "gradable": True,
        "n_entries": n,
        "own_per_slot": own_per_slot,
        "leverage_pct": round(lev_hits / n * 100, 1),
        "anchor_exposure": anchor_exposure,
        "anchor_exposure_by_player": per_anchor,
        "max_overlap": max_overlap,
        "unique_pct": unique_pct,
        "best_pctile": pct[0] if pct else None,
        "median_pctile": pct[len(pct) // 2] if pct else None,
    }


def present_handles(parsed: dict, handles) -> list[str]:
    """The watchlist handles that actually have ≥1 entry in this contest, kept in
    the caller's spelling (matched case-insensitively)."""
    seen = set(parsed["lineups"]["EntryName"].map(_handle))
    return [h for h in (handles or []) if str(h).lower() in seen]


def per_pro_profiles(parsed: dict, handles) -> dict:
    """Per-HANDLE structural fingerprint for each watchlist handle present in this
    contest — the individual pros, not the aggregate bucket `structural_profile`
    returns. Keyed by the handle as spelled in `handles`. Every pro is measured
    against ONE shared set of chalk anchors (the same axis as the shark gap)."""
    anchors = chalk_anchors(parsed)
    out = {}
    for h in present_handles(parsed, handles):
        prof = structural_profile(parsed, [h], anchors)
        if prof.get("gradable"):
            out[h] = prof
    return out


# Dimensions where we compare us to the sharks, with how to read the delta.
_DIMS = [
    ("own_per_slot", "avg own%/slot", "lower = more contrarian"),
    ("leverage_pct", "% lineups w/ sub-5% piece", "sharks carry one in most"),
    ("anchor_exposure", "exposure to chalk anchors", "under-owning these is the recurring leak"),
    ("unique_pct", "% unique rosters", "sharks are all-unique"),
]


def shark_gap(parsed: dict, shark_handles, user_handles) -> dict:
    """Us vs the in-field sharks on every structural axis, with the deltas."""
    anchors = chalk_anchors(parsed)
    sharks = structural_profile(parsed, shark_handles, anchors)
    user = structural_profile(parsed, user_handles, anchors)

    deltas = []
    if sharks.get("gradable") and user.get("gradable"):
        for key, label, read in _DIMS:
            sv, uv = sharks.get(key), user.get(key)
            if sv is None or uv is None:
                continue
            deltas.append({
                "dim": key, "label": label, "read": read,
                "user": uv, "shark": sv, "delta": round(uv - sv, 3),
            })
        deltas.sort(key=lambda d: -abs(d["delta"]))

    return {
        "field": len(parsed["lineups"]),
        "anchors": anchors,
        "sharks": sharks,
        "user": user,
        "deltas": deltas,
        "sharks_in_field": sharks.get("gradable", False),
    }


def _load_learned() -> dict:
    """Auto-discovered handles promoted from recurring opponents, kept in a
    separate overlay (`shark_handles_learned.yaml`, shape `{sport: [handles]}`) so
    the curated `shark_handles.yaml` (its `&core` anchor + comments) is never
    rewritten. Empty dict if missing/bad."""
    if not _LEARNED_PATH.exists():
        return {}
    try:
        import yaml
        data = yaml.safe_load(_LEARNED_PATH.read_text()) or {}
        return data if isinstance(data, dict) else {}
    except Exception:  # noqa: BLE001 — overlay is optional; never break the autopsy
        return {}


def load_handles() -> dict:
    """Read the per-sport shark watchlist config (empty dict if missing/bad),
    unioned with the auto-discovered `shark_handles_learned.yaml` overlay so
    promoted pros are benchmarked without touching the curated file."""
    try:
        import yaml
        cfg = yaml.safe_load(_HANDLES_PATH.read_text()) or {}
    except Exception:  # noqa: BLE001 — config is optional; never break the autopsy
        cfg = {}
    learned = _load_learned()
    if learned:
        by_sport = dict(cfg.get("sharks_by_sport") or {})
        for sport, names in learned.items():
            existing = list(by_sport.get(sport) or [])
            lower = {n.lower() for n in existing}
            for nm in (names or []):
                if nm and nm.lower() not in lower:
                    existing.append(nm)
                    lower.add(nm.lower())
            by_sport[sport] = existing
        cfg["sharks_by_sport"] = by_sport
    return cfg


def gap_for_slug(slug: str, parsed: dict) -> dict:
    """Compute the shark-gap for a slate slug using the configured handles."""
    cfg = load_handles()
    sport = (cfg.get("slug_sport") or {}).get(slug)
    sharks = (cfg.get("sharks_by_sport") or {}).get(sport, [])
    user = cfg.get("user", [])
    g = shark_gap(parsed, sharks, user)
    g["slug"], g["sport"] = slug, sport
    return g


def gap_md(gap: dict) -> str:
    """Render the shark-gap as a compact markdown block."""
    out = ["### Shark gap — what they did differently (structural)"]
    if not gap.get("sharks_in_field"):
        out.append("- *No tracked sharks in this contest — can't compute a structural gap.*")
        return "\n".join(out)
    s, u = gap["sharks"], gap["user"]
    out.append(f"- **Entries:** sharks {s['n_entries']} · you {u['n_entries']}")
    out.append("")
    out.append("| Dimension | You | Sharks | Δ |")
    out.append("|---|---|---|---|")
    for d in gap["deltas"]:
        out.append(f"| {d['label']} | {d['user']} | {d['shark']} | {d['delta']:+} |")
    out.append("")
    out.append(f"_Read top-down — biggest gap first. {gap['deltas'][0]['label']}: "
               f"{gap['deltas'][0]['read']}._" if gap["deltas"] else "")
    return "\n".join(out)
