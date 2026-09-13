"""NFL Classic pool lock (9/12/26) — Claude's tiered board IS the pool.

The weekly Classic process is two-stage (user directive 9/12/26): Saturday
night / Sunday morning the PLAYER POOL is finalized position by position
(QB → RB → WR → TE → DST) from the preliminary ETR file; Sunday ~11:30 ET,
once ETR finalizes after the injury reports, the BUILDS are finalized.

Claude drafts the board (Core / Good / Okay / Fade + Leverage). The user
reviews it per position and may flip any tier or leverage flag — those
flips are the OVERRIDES stored here (data/player_pool/<slug>_overrides.json)
so a re-rank never silently undoes an approved call. "Lock pool → Sim"
writes the approved board into the strategy contract as a HARD pool:
Core / Good / Okay are IN, Fade is OUT, and the Sim switches Include
accordingly — nobody outside the pool is ever built.

Tiers are information for the builder and the picker; they never become
exposure rules here (rules enter only through approved autopsy proposals).
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src import player_pool, sessions
from src.autopsy import _norm_name
from src.nfl_classic_defs import normalize_position

_REPO_ROOT = Path(__file__).parent.parent
_POOL_DIR = _REPO_ROOT / "data" / "player_pool"
_CONTRACT_DIR = _REPO_ROOT / "data" / "strategy_contract"

POSITIONS = ("QB", "RB", "WR", "TE", "DST")
TIERS = ("Core", "Good", "Okay", "Fade")
IN_POOL_TIERS = ("Core", "Good", "Okay")


def _overrides_path(slug: str) -> Path:
    return _POOL_DIR / f"{slug}_overrides.json"


def load_overrides(slug: str) -> dict:
    """{normalized name: {tier, leverage, pos}} — the user's flips."""
    p = _overrides_path(slug)
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text())
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_overrides(slug: str, overrides: dict) -> None:
    _POOL_DIR.mkdir(parents=True, exist_ok=True)
    _overrides_path(slug).write_text(json.dumps(overrides, indent=2))


def set_override(slug: str, name: str, tier: str | None = None,
                 leverage: bool | None = None, pos: str | None = None) -> None:
    """Record one flip. A tier outside TIERS is ignored."""
    ov = load_overrides(slug)
    key = _norm_name(name)
    row = dict(ov.get(key) or {})
    if tier is not None and tier in TIERS:
        row["tier"] = tier
    if leverage is not None:
        row["leverage"] = bool(leverage)
    if pos:
        row["pos"] = pos
    row["name"] = name
    ov[key] = row
    save_overrides(slug, ov)


def clear_overrides(slug: str) -> None:
    p = _overrides_path(slug)
    if p.exists():
        p.unlink()


def board_rows(slug: str) -> list[dict]:
    """The reviewable board: Claude's parsed tiers joined to the loaded
    projections (position / team / opponent / salary / proj / own), with the
    user's overrides applied. One row per board player:
      {name, pos, team, opponent, salary, proj, own, claude_tier, tier,
       leverage, in_pool, overridden}
    Position comes from the projections (rulebook-normalized); the board
    table's Pos column is the fallback. Players Claude tiered but who are no
    longer in the projections (dropped from a final file) are kept with
    `missing: True` so the review can show them."""
    from src import pool_calibration
    saved = player_pool.load_pool(slug)
    if not saved:
        return []
    parsed = pool_calibration.parse_pool_tiers(saved["markdown"])
    sources = sessions.load_sources(slug)
    proj = player_pool.build_pool(sources) if sources else None
    by_norm: dict = {}
    if proj is not None and not proj.empty:
        for _, r in proj.iterrows():
            by_norm[_norm_name(str(r["name"]))] = r
    overrides = load_overrides(slug)
    out: list[dict] = []
    for r in parsed:
        key = _norm_name(r["name"])
        p = by_norm.get(key)
        ov = overrides.get(key) or {}

        def _num(col):
            if p is None or col not in p.index:
                return None
            v = p[col]
            try:
                v = float(v)
            except (TypeError, ValueError):
                return None
            return None if v != v else v

        pos = normalize_position(p["position"]) if p is not None and "position" in p.index else ""
        pos = pos or normalize_position(r.get("pos") or "") or str(ov.get("pos") or "")
        tier = str(ov.get("tier") or r["tier"])
        lev = bool(ov.get("leverage", r.get("leverage", False)))
        out.append({
            "name": r["name"],
            "pos": pos,
            "team": (str(p["team"]) if p is not None and "team" in p.index and p["team"] == p["team"] else ""),
            "opponent": (str(p["opponent"]) if p is not None and "opponent" in p.index and p["opponent"] == p["opponent"] else ""),
            "salary": _num("salary"),
            "proj": _num("proj_points"),
            "own": _num("ownership"),
            "claude_tier": r["tier"],
            "tier": tier,
            "leverage": lev,
            "in_pool": tier in IN_POOL_TIERS,
            "overridden": bool(ov),
            "missing": p is None,
        })
    return out


def rows_by_position(rows: list[dict]) -> dict[str, list[dict]]:
    """Rows grouped in walk order (QB → RB → WR → TE → DST, then anything
    else), each group in board order."""
    groups: dict[str, list[dict]] = {p: [] for p in POSITIONS}
    for r in rows:
        groups.setdefault(r["pos"] or "?", []).append(r)
    return {k: v for k, v in groups.items() if v}


def pool_summary(rows: list[dict]) -> dict:
    """Per-position counts: {pos: {in, out, Core, Good, Okay, Fade, leverage}}
    plus a total."""
    out: dict = {}
    for r in rows:
        g = out.setdefault(r["pos"] or "?", {"in": 0, "out": 0, "leverage": 0,
                                              **{t: 0 for t in TIERS}})
        g["in" if r["in_pool"] else "out"] += 1
        if r["tier"] in g:
            g[r["tier"]] += 1
        if r["leverage"]:
            g["leverage"] += 1
    out["total"] = {"in": sum(1 for r in rows if r["in_pool"]),
                    "out": sum(1 for r in rows if not r["in_pool"])}
    return out


def _contract_path(slug: str) -> Path:
    return _CONTRACT_DIR / f"{slug}.json"


def lock_pool(slug: str) -> dict:
    """Write the approved board into the strategy contract as a HARD pool and
    refresh the contract's `board` block with the overrides applied. Returns
    the pool block written."""
    rows = board_rows(slug)
    players = [{"name": r["name"], "pos": r["pos"], "tier": r["tier"],
                "leverage": r["leverage"], "in": r["in_pool"]}
               for r in rows if not r["missing"]]
    block = {
        "locked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "hard": True,
        "slug": slug,
        "n_in": sum(1 for p in players if p["in"]),
        "n_out": sum(1 for p in players if not p["in"]),
        "by_position": {pos: sum(1 for p in players if p["in"] and p["pos"] == pos)
                        for pos in POSITIONS},
        "players": players,
    }
    p = _contract_path(slug)
    try:
        payload = json.loads(p.read_text()) if p.exists() else {}
    except (json.JSONDecodeError, OSError):
        payload = {}
    if not payload:
        payload = {"generated_at": block["locked_at"], "slug": slug, "calls": [],
                   "fades": [], "leverage_candidates": []}
    payload["pool"] = block
    payload["board"] = [{"name": x["name"], "tier": x["tier"],
                         "leverage": x["leverage"], "pos": x["pos"]} for x in players]
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2))
    return block


def locked_pool(slug: str) -> dict | None:
    """The contract's pool block, or None when nothing is locked."""
    p = _contract_path(slug)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text()).get("pool") or None
    except (json.JSONDecodeError, OSError):
        return None


def unlock_pool(slug: str) -> None:
    p = _contract_path(slug)
    if not p.exists():
        return
    try:
        payload = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return
    payload.pop("pool", None)
    p.write_text(json.dumps(payload, indent=2))
