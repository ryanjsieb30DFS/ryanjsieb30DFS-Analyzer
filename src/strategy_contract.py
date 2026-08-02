"""Strategy contract — the Analyzer → Sim-tool hand-off.

When a slate strategy is generated, emit a machine-readable sidecar at
`data/strategy_contract/<slug>.json` with the strategy's per-player CALLS from
the `## Fades` + `## Leverage` sections (legacy: combined `## Leverage & fades`) — each bolded bullet's name + verdict
(play / pass / pass_mix / underweight / lean_fade / fade) — plus the leverage
candidates the strategy was required to address.

The Sim tool shows the calls in its Build tab and one-clicks ONLY the hard
`fade` verdicts onto its Include column. Lean fades / underweights are
display-only (the strategy says under-own, not zero), and PLAY calls are never
touched — the Analyzer still never builds lineups; the user decides.

Verdict parsing lives in `player_pool.parse_calls` (shared with the
verdict-aware `extract_fades` that feeds pool membership); this module filters
the parsed names to the loaded projections universe so section headings never
leak through, and serializes the hand-off.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from src import player_pool, landscape
from src.player_pool import parse_calls  # noqa: F401 — shared parser, re-exported
from src.autopsy import _norm_name

_CONTRACT_DIR = Path(__file__).parent.parent / "data" / "strategy_contract"


def _path(slug: str) -> Path:
    return _CONTRACT_DIR / f"{slug}.json"


# "a minimum of 2 and maximum of 3 leaderboard golfers", "min 2 / max 3 LB",
# "using 2-3 leaderboard golfers per lineup" — the shapes RD4 SD articles use.
_LB_PATTERNS = (
    # "min 2, max 3" and "a minimum of 2 and maximum of 3". The gaps must allow
    # WORDS ("of", "and"), not just punctuation — `\W` here silently failed to
    # match the real 8/2/26 sentence, which is the whole reason this exists.
    r"\bmin(?:imum)?\b[^.]{0,25}?(\d+)[^.]{0,40}?\bmax(?:imum)?\b[^.]{0,25}?(\d+)",
    r"(\d)\s*(?:-|–|to)\s*(\d)\s+(?:leaderboard|LB|T-?\d+)\b",
)
_LB_CONTEXT = re.compile(r"leaderboard|\bLB\b|T-?\d+\s+and\s+ties", re.I)
_LB_TOPN = re.compile(r"\bT-?(\d{1,2})\b")


def parse_structure_rules(strategy_md: str) -> list[dict]:
    """Structural quotas the written strategy states in prose.

    RD4 Showdown articles set a SHAPE as well as names — "a minimum of 2 and
    maximum of 3 leaderboard golfers (T-10 and ties) per lineup". That is a
    real build rule, but until now it lived only in the prose: the contract had
    no field for it, so the Sim never received it and 17 of 34 entered lineups
    on 8/2/26 broke it.

    Returns [{kind: "leaderboard", top_n, min, max, quote}]. Only the NUMBERS
    come from here — the Sim resolves WHICH golfers from its own `current_score`
    column, so a parse that finds nothing costs nothing (the Sim falls back to
    its defaults and the user sets them by hand, as before).

    Deliberately conservative: a sentence must mention the leaderboard AND
    carry a min/max pair. Ambiguity is left to the user rather than guessed —
    a wrong quota silently shapes thousands of lineups.
    """
    out: list[dict] = []
    for raw in re.split(r"(?<=[.!?])\s+|\n", strategy_md or ""):
        if not _LB_CONTEXT.search(raw):
            continue
        for pat in _LB_PATTERNS:
            m = re.search(pat, raw, re.I)
            if not m:
                continue
            lo, hi = int(m.group(1)), int(m.group(2))
            if not (0 <= lo <= hi <= 6):
                continue        # not a per-lineup quota (6-player rosters)
            topn = _LB_TOPN.search(raw)
            # Window around the MATCH, not the head of the block. Strategy
            # bullets run long, and a leading slice can show text that doesn't
            # contain the rule at all — which defeats the point of quoting it.
            lo_i, hi_i = max(0, m.start() - 90), min(len(raw), m.end() + 90)
            quote = " ".join(raw[lo_i:hi_i].split())
            out.append({
                "kind": "leaderboard",
                "top_n": int(topn.group(1)) if topn else 10,
                "min": lo,
                "max": hi,
                # Shown to the user in the Sim so two bare numbers never have to
                # be taken on trust.
                "quote": ("…" if lo_i else "") + quote + ("…" if hi_i < len(raw) else ""),
            })
            break
        if out:
            break               # first explicit statement wins
    return out


def write_contract(slug: str, strategy_md: str, sources: dict) -> Path:
    """Write the contract from the just-generated strategy + loaded projections."""
    calls = parse_calls(strategy_md)

    universe = {}
    pool = None
    if sources:
        pool = player_pool.build_pool(sources)
        if not pool.empty:
            universe = {_norm_name(str(n)): str(n) for n in pool["name"]}

    if universe:
        resolved = []
        for c in calls:
            key = _norm_name(c["name"])
            actual = universe.get(key)
            if actual is None and len(key) >= 4:
                # Last-name-only calls ("Donchenko") — substring match, unique
                # only, and never on fragments shorter than 4 chars (a 3-letter
                # scrap resolving to one random player is worse than a drop).
                hits = [v for k, v in universe.items() if key in k]
                actual = hits[0] if len(hits) == 1 else None
            if actual is not None:
                resolved.append({"name": actual, "verdict": c["verdict"]})
        calls = resolved

    # One call per player. Parsing artifacts have produced the same player
    # with two verdicts (a matchup-header phantom PLAY beside a real
    # LEAN FADE); the harsher explicit verdict wins.
    _severity = {"fade": 5, "lean_fade": 4, "underweight": 3,
                 "pass": 2, "pass_mix": 1, "play": 0}
    by_name: dict[str, dict] = {}
    for c in calls:
        cur = by_name.get(c["name"])
        if cur is None or _severity.get(c["verdict"], 0) > _severity.get(cur["verdict"], 0):
            by_name[c["name"]] = c
    calls = list(by_name.values())

    leverage: list[dict] = []
    chalk_pairs: list[dict] = []
    anchor_pairs: list[dict] = []
    if pool is not None and not pool.empty:
        cands = landscape.leverage_candidates(pool)
        for _, r in cands.iterrows():
            leverage.append({
                "name": str(r.get("name")),
                # NaN-guarded: a bare NaN here writes non-standard JSON that
                # the Sim's json.loads chokes on, and drift counts it as
                # "checked" while never being able to flag it.
                "own": (round(float(r["ownership"]), 2)
                        if "ownership" in cands.columns
                        and r["ownership"] == r["ownership"] else None),
            })
        # Slate-specific RULE MATERIAL for the Sim's builder (7/29/26, user
        # request): the field's likeliest duplicated pairs and the
        # anchor-equivalence twin sets — the Sim renders one-click Player-Group
        # rules from these ("never both halves", "at most 1 of the twins").
        # Data-derived from the same landscape math the strategy cites; no
        # LLM parsing involved, so the names always exist in the pool.
        try:
            chalk_pairs = [{"players": c["players"], "joint_pct": c["joint_pct"]}
                           for c in landscape.chalky_combos(pool)[:4]]
        except Exception:  # noqa: BLE001 — rule material is additive, never blocks
            chalk_pairs = []
        try:
            anchor_pairs = [{"players": [str(n) for n in g["players"]][:4]}
                            for g in landscape.anchor_equivalence_check(pool)[:3]
                            if len(g.get("players") or []) >= 2]
        except Exception:  # noqa: BLE001
            anchor_pairs = []

    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "slug": slug,
        "calls": calls,
        # Hard fades ONLY — what the Sim tool may auto-apply to Include.
        "fades": [c["name"] for c in calls if c["verdict"] == "fade"],
        "leverage_candidates": leverage,
        "chalk_pairs": chalk_pairs,
        "anchor_pairs": anchor_pairs,
        # Structural quotas stated in the strategy's prose ("min 2 / max 3
        # leaderboard golfers per lineup"). The Sim pre-fills its leaderboard
        # rule from these; it resolves WHICH golfers itself from current_score.
        "structure_rules": parse_structure_rules(strategy_md),
        # The tiered player board (Core/Good/Okay/Fade + Leverage), machine-
        # readable, so the Sim can show each player's tier at build time. Rides
        # the contract because the contract already has the full slate
        # lifecycle (written on generation, cleared + archived with the slate).
        "board": _board_rows(slug),
    }
    p = _path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2))
    return p


def _board_rows(slug: str) -> list[dict]:
    """The persisted player board's (name, tier, leverage) rows, [] when no
    board exists or the table doesn't parse."""
    try:
        from src import pool_calibration
        saved = player_pool.load_pool(slug)
        if not saved:
            return []
        rows = pool_calibration.parse_pool_tiers(saved["markdown"])
        out = []
        for r in rows:
            tier_raw = str(r.get("tier") or "")
            out.append({
                "name": str(r.get("player") or r.get("name") or ""),
                "tier": tier_raw.replace("· Leverage", "").replace("·", "").strip(),
                "leverage": "leverage" in tier_raw.lower(),
            })
        return [r for r in out if r["name"] and r["tier"]]
    except Exception:  # noqa: BLE001 — the board is an enhancement, never a blocker
        return []


def update_board(slug: str) -> None:
    """Refresh (or create) the contract's board block after a standalone
    player-pool run — the board can regenerate without a new strategy."""
    p = _path(slug)
    try:
        payload = json.loads(p.read_text()) if p.exists() else {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "slug": slug, "calls": [], "fades": [], "leverage_candidates": [],
        }
    except (json.JSONDecodeError, OSError):
        return
    payload["board"] = _board_rows(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2))


def clear_contract(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()
