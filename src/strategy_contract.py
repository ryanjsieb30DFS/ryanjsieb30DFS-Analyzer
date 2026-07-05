"""Strategy contract — the Analyzer → Sim-tool hand-off.

When a slate strategy is generated, emit a machine-readable sidecar at
`data/strategy_contract/<slug>.json` with the strategy's per-player CALLS from
the `## Leverage & fades` section — each bolded bullet's name + verdict
(play / pass / pass_mix / underweight / lean_fade / fade) — plus the leverage
candidates the strategy was required to address.

The Sim tool shows the calls in its Build tab and one-clicks ONLY the hard
`fade` verdicts onto its Include column. Lean fades / underweights are
display-only (the strategy says under-own, not zero), and PLAY calls are never
touched — the Analyzer still never builds lineups; the user decides.

NOTE: this module parses verdicts itself instead of `player_pool.extract_fades`
— that helper sweeps every bolded name in the section when the strategy doesn't
use a literal "**Fades**" subheading (e.g. "Additional fades / underweights"),
which would have marked PLAY calls as fades. Names are additionally filtered to
the loaded projections universe so section headings never leak through.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from src import player_pool, landscape
from src.player_pool import _leading_name
from src.autopsy import _norm_name

_CONTRACT_DIR = Path(__file__).parent.parent / "data" / "strategy_contract"

# Order matters: longer/more-specific tokens first so "LEAN FADE" isn't read as
# "FADE" and "PASS/MIX" isn't read as "PASS".
_VERDICT_TOKENS = [
    ("LEAN FADE", "lean_fade"),
    ("UNDERWEIGHT", "underweight"),
    ("PASS/MIX", "pass_mix"),
    ("FADE", "fade"),
    ("PASS", "pass"),
    ("PLAY", "play"),
]


def _path(slug: str) -> Path:
    return _CONTRACT_DIR / f"{slug}.json"


def _verdict_for(bold_text: str, after_bold: str, line: str) -> str | None:
    """The call's verdict, read where the convention puts it: inside the bolded
    lead ('**Keith Mitchell $10,000 — FADE.**'), else the first clause after the
    bold ('— PASS/MIX.'), else anywhere in the line (last resort)."""
    for scope in (bold_text, after_bold.split(".")[0], line):
        u = scope.upper()
        for token, verdict in _VERDICT_TOKENS:
            if token in u:
                return verdict
    return None


def parse_calls(strategy_md: str) -> list[dict]:
    """Per-player calls from the '## Leverage & fades' section: one entry per
    bolded bullet with a recognizable verdict. Names are NOT yet filtered to the
    projections universe — `write_contract` does that."""
    if not strategy_md:
        return []
    sec = re.search(r"##\s*Leverage\s*&\s*fades(.*?)(?:\n##\s|\Z)", strategy_md, re.S | re.I)
    if not sec:
        return []
    calls = []
    for line in sec.group(1).splitlines():
        m = re.search(r"\*\*(.+?)\*\*", line)
        if not m:
            continue
        name = _leading_name(m.group(1))
        if not name:
            continue
        verdict = _verdict_for(m.group(1), line[m.end():], line)
        if verdict:
            calls.append({"name": name, "verdict": verdict})
    return calls


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
            actual = universe.get(_norm_name(c["name"]))
            if actual is None:
                # Last-name-only calls ("Donchenko") — substring match, unique only.
                hits = [v for k, v in universe.items() if _norm_name(c["name"]) in k]
                actual = hits[0] if len(hits) == 1 else None
            if actual is not None:
                resolved.append({"name": actual, "verdict": c["verdict"]})
        calls = resolved

    leverage: list[dict] = []
    if pool is not None and not pool.empty:
        cands = landscape.leverage_candidates(pool)
        for _, r in cands.iterrows():
            leverage.append({
                "name": str(r.get("name")),
                "own": (float(r["ownership"]) if "ownership" in cands.columns else None),
            })

    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "slug": slug,
        "calls": calls,
        # Hard fades ONLY — what the Sim tool may auto-apply to Include.
        "fades": [c["name"] for c in calls if c["verdict"] == "fade"],
        "leverage_candidates": leverage,
    }
    p = _path(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2))
    return p


def clear_contract(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()
