"""Ownership drift — has the slate moved under the strategy since it was written?

Vendors update ownership between the strategy run and lock. The strategy's
leverage reads freeze at generation time (the strategy sidecar at
`data/strategy_contract/<slug>.json` snapshots each leverage candidate's own%),
so when the user re-uploads a NEWER vendor file, this diffs the candidates'
CURRENT ownership against the snapshot and flags the ones whose leverage thesis
changed — no regeneration, no Claude call, just arithmetic:

  - a candidate that CROSSED the 10% leverage line upward → leverage gone
  - a candidate that drifted ≥ `_DELTA_PTS` points either way → re-read it

Paste/upload only (the projections the user already loads) — never scraped.
Display-only synthesis: it says what moved, never what to do about it.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.autopsy import _norm_name

_CONTRACT_DIR = Path(__file__).parent.parent / "data" / "strategy_contract"

_LEV_LINE = 10.0   # the sub-10% leverage threshold the strategy screens on
_DELTA_PTS = 3.0   # a move this big (either way) is worth a re-read


def ownership_drift(slug: str, pool) -> dict | None:
    """Diff the strategy's leverage-candidate ownership snapshot against the
    CURRENTLY loaded projections. None when there's no strategy snapshot, no
    candidates, or no loaded pool. `pool` = player_pool.build_pool(sources)."""
    p = _CONTRACT_DIR / f"{slug}.json"
    if not p.exists() or pool is None or getattr(pool, "empty", True):
        return None
    try:
        contract = json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    cands = contract.get("leverage_candidates") or []
    if not cands or "ownership" not in pool.columns:
        return None

    current = {}
    for nm, ow in zip(pool["name"], pool["ownership"]):
        if ow is not None and ow == ow:
            current[_norm_name(str(nm))] = float(ow)

    drifted, checked = [], 0
    for c in cands:
        then = c.get("own")
        now = current.get(_norm_name(str(c.get("name", ""))))
        if then is None or now is None:
            continue
        checked += 1
        crossed = then < _LEV_LINE <= now
        if crossed or abs(now - then) >= _DELTA_PTS:
            drifted.append({
                "name": c.get("name"),
                "then": round(float(then), 1),
                "now": round(now, 1),
                "delta": round(now - float(then), 1),
                "crossed_leverage_line": crossed,
            })
    drifted.sort(key=lambda d: -abs(d["delta"]))
    return {
        "generated_at": contract.get("generated_at"),
        "n_candidates": len(cands),
        "n_checked": checked,
        "drifted": drifted,
    }


def drift_md(d: dict) -> str | None:
    """Compact warning block; None when nothing checked or nothing moved."""
    if not d or not d.get("n_checked"):
        return None
    if not d["drifted"]:
        return (f"✅ **Ownership check:** all {d['n_checked']} leverage candidates still "
                f"near their strategy-time ownership (strategy written {d['generated_at']}).")
    lines = [f"⚠️ **Ownership drift since the strategy was written "
             f"({d['generated_at']})** — the loaded projections moved on "
             f"{len(d['drifted'])} of {d['n_checked']} leverage candidates:"]
    for r in d["drifted"]:
        tag = " — **crossed the 10% line; leverage thesis gone**" if r["crossed_leverage_line"] else ""
        lines.append(f"- **{r['name']}**: {r['then']}% → {r['now']}% "
                     f"({r['delta']:+}){tag}")
    lines.append("_Re-read these before lock; regenerate the strategy if the slate moved._")
    return "\n".join(lines)
