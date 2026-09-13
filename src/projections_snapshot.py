"""Preliminary-vs-final projections (NFL Classic stage 2, 9/12/26).

ETR's Saturday file is preliminary; the final file lands ~11:30 ET Sunday
after the injury reports. Uploading the final file for a vendor that
already has a file loaded now REPLACES it (before this, the two files sat
side by side and `merge_same_vendor` kept the HIGHER projection per name —
a downgraded player silently kept his Saturday number). The replaced frame
is kept here as the preliminary snapshot so the diff can show what moved.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.autopsy import _norm_name

_REPO_ROOT = Path(__file__).parent.parent
_SNAP_DIR = _REPO_ROOT / "data" / "projections_prev"

# Swing thresholds (user decision 9/12/26: "injury news plus big swings").
PROJ_ABS = 2.0      # points
PROJ_PCT = 0.15     # 15% of the preliminary projection
OWN_ABS = 3.0       # ownership points


def _path(slug: str) -> Path:
    return _SNAP_DIR / f"{slug}.json"


def save_prelim(slug: str, source_name: str, vendor: str, df: pd.DataFrame) -> None:
    _SNAP_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps({
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source_name": source_name,
        "vendor": vendor,
        "rows": df.to_dict(orient="records"),
    }, default=str, indent=2))


def load_prelim(slug: str) -> dict | None:
    p = _path(slug)
    if not p.exists():
        return None
    try:
        blob = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    blob["df"] = pd.DataFrame(blob.get("rows") or [])
    return blob


def clear_prelim(slug: str) -> None:
    p = _path(slug)
    if p.exists():
        p.unlink()


def _f(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return None if v != v else v


def diff_prelim_vs_final(prev: pd.DataFrame, cur: pd.DataFrame,
                         pool_names: list[str] | None = None) -> dict:
    """What moved between the preliminary and the final file.

    Returns {gone: [rows], new: [rows], moves: [rows], flagged: [rows],
             pool_hits: [rows], n_prev, n_cur}. A `move` row carries name,
    pos, team, salary/proj/own before + after and deltas; `flagged` is the
    subset over the thresholds (or any salary change); `gone` players
    vanished from the file (ruled out / no longer priced) — always flagged.
    `pool_hits` = flagged + gone rows whose name is in `pool_names`."""
    def _index(df):
        out = {}
        if df is None or df.empty or "name" not in df.columns:
            return out
        for _, r in df.iterrows():
            out.setdefault(_norm_name(str(r["name"])), r)
        return out

    pi, ci = _index(prev), _index(cur)
    pool = {_norm_name(n) for n in (pool_names or [])}

    def _base(r):
        return {"name": str(r["name"]),
                "pos": str(r.get("position") or "") if "position" in r.index else "",
                "team": str(r.get("team") or "") if "team" in r.index else ""}

    gone = [dict(_base(r), in_pool=k in pool) for k, r in pi.items() if k not in ci]
    new = [dict(_base(r), in_pool=k in pool) for k, r in ci.items() if k not in pi]
    moves, flagged = [], []
    for k, r in ci.items():
        if k not in pi:
            continue
        p = pi[k]
        row = _base(r)
        for col, key in (("salary", "sal"), ("proj_points", "proj"), ("ownership", "own")):
            b = _f(p.get(col)) if col in p.index else None
            a = _f(r.get(col)) if col in r.index else None
            row[f"{key}_before"], row[f"{key}_after"] = b, a
            row[f"{key}_delta"] = (a - b) if (a is not None and b is not None) else None
        reasons = []
        pd_ = row["proj_delta"]
        if pd_ is not None and (abs(pd_) >= PROJ_ABS or
                                (row["proj_before"] and abs(pd_) / abs(row["proj_before"]) >= PROJ_PCT)):
            reasons.append(f"proj {pd_:+.1f}")
        od = row["own_delta"]
        if od is not None and abs(od) >= OWN_ABS:
            reasons.append(f"own {od:+.1f}")
        sd = row["sal_delta"]
        if sd:
            reasons.append(f"salary {sd:+,.0f}")
        row["reasons"] = reasons
        row["in_pool"] = k in pool
        if row["proj_delta"] is not None or row["own_delta"] is not None or sd:
            moves.append(row)
        if reasons:
            flagged.append(row)
    flagged.sort(key=lambda x: -abs(x["proj_delta"] or 0))
    pool_hits = [g for g in gone if g["in_pool"]] + [f for f in flagged if f["in_pool"]]
    return {"gone": gone, "new": new, "moves": moves, "flagged": flagged,
            "pool_hits": pool_hits, "n_prev": len(pi), "n_cur": len(ci)}


def diff_md(d: dict) -> str:
    """Plain-language summary of a diff for the Projections tab."""
    if not d:
        return ""
    L = [f"**Final vs preliminary:** {d['n_prev']} players before, {d['n_cur']} now."]
    if d["gone"]:
        L.append("**Gone from the file (likely ruled out):** "
                 + ", ".join(f"{g['name']} ({g['pos']} {g['team']})".strip()
                             + (" — IN YOUR POOL" if g["in_pool"] else "") for g in d["gone"]))
    if d["new"]:
        L.append("**New in the file:** " + ", ".join(
            f"{g['name']} ({g['pos']} {g['team']})".strip() for g in d["new"]))
    if d["flagged"]:
        L.append(f"**Big swings ({len(d['flagged'])}):**")
        for f in d["flagged"][:40]:
            L.append(f"- {f['name']} ({f['pos']} {f['team']}) — " + ", ".join(f["reasons"])
                     + (" — **in your pool**" if f["in_pool"] else ""))
    if not d["gone"] and not d["flagged"]:
        L.append("No player vanished and nothing moved past the swing thresholds.")
    return "\n".join(L)
