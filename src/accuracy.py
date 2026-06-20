"""Self-grading accuracy layer — did our actual bets and reads pay off?

The learning loop already grades PROCESS discipline, vendor projection MAE,
red-team hindsight, and lesson mechanisms. What it never measured: were the
players/edges we actually backed correct? This module grades our REVEALED bets —
the lineups we entered — against the structured actuals the autopsy already
captures (overperformers, underperformers, slate-defining low-owned plays, and
per-lineup proj-vs-actual).

Design note: it deliberately does NOT parse the prose slate analysis. Across
archived slates the analysis headings vary (one slate has a `## Player board`
table, another has `## Chalk map` / `## Sub-5% pool`), so prose-call parsing is
unreliable. The lineups we ENTERED are the real expression of our reads, and
they're captured reliably in `autopsy.json`'s `user_lineups`. Everything here is
pure and grades against actuals — it never recomputes them.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.autopsy import _norm_name

_REPO_ROOT = Path(__file__).parent.parent


def _records(autopsy) -> list[dict]:
    """Normalize an autopsy.json payload (list of contest records, or one) to a list."""
    if isinstance(autopsy, list):
        return autopsy
    return [autopsy] if autopsy else []


def _our_players(records: list[dict]) -> set[str]:
    """Normalized names of every player we rostered across our entered lineups."""
    out: set[str] = set()
    for r in records:
        for ln in r.get("user_lineups") or []:
            for p in ln.get("players") or []:
                out.add(_norm_name(p))
    return out


def _merge_named(records: list[dict], key: str) -> dict[str, dict]:
    """Merge a per-record named list (overperformers / underperformers /
    slate_defining_plays) into one norm-name -> row map (first occurrence wins)."""
    out: dict[str, dict] = {}
    for r in records:
        for row in r.get(key) or []:
            nk = _norm_name(row.get("name", ""))
            if nk and nk not in out:
                out[nk] = row
    return out


def grade_edges(autopsy) -> dict:
    """Did we back the right players? Graded from structured actuals only.

    - leverage_capture: of the slate-defining low-owned plays (the cheap players
      that defined winning lineups), what fraction did WE roster? This is the
      sharp signal — owning the low-owned plays that actually paid off.
    - overperformer_capture: fraction of the top proj-beating players we rostered.
    - underperformer_exposure: fraction of the top proj-missing busts we rostered
      (LOWER is better — these are the plays we should have faded).
    """
    records = _records(autopsy)
    ours = _our_players(records)
    if not ours:
        return {"gradable": False, "reason": "no entered lineups in this autopsy"}

    def _cap(named: dict[str, dict]):
        if not named:
            return None, [], []
        hit = [named[n]["name"] for n in named if n in ours]
        miss = [named[n]["name"] for n in named if n not in ours]
        return round(len(hit) / len(named), 3), hit, miss

    lev_rate, lev_hit, lev_miss = _cap(_merge_named(records, "slate_defining_plays"))
    over_rate, over_hit, _ = _cap(_merge_named(records, "top_overperformers"))
    under_rate, under_hit, _ = _cap(_merge_named(records, "top_underperformers"))

    return {
        "gradable": True,
        "n_our_players": len(ours),
        "leverage_capture": lev_rate,
        "leverage_hit": lev_hit,
        "leverage_missed": lev_miss,
        "overperformer_capture": over_rate,
        "overperformer_hit": over_hit,
        "underperformer_exposure": under_rate,
        "underperformer_hit": under_hit,
    }


def grade_lineups(autopsy) -> dict:
    """Grade the lineups we actually entered against their projection and finish.

    Dedupes entries across contest records by (entry name, roster). Per lineup:
    ratio = actual_points / proj_total (>1 = beat its own projection); percentile.
    """
    records = _records(autopsy)
    seen: set = set()
    rows: list[dict] = []
    for r in records:
        for ln in r.get("user_lineups") or []:
            key = (ln.get("entry_name"),
                   tuple(sorted(_norm_name(p) for p in ln.get("players") or [])))
            if key in seen:
                continue
            seen.add(key)
            proj, pts = ln.get("proj_total"), ln.get("points")
            ratio = round(pts / proj, 3) if proj and pts is not None else None
            rows.append({
                "entry_name": ln.get("entry_name"),
                "points": pts,
                "proj_total": proj,
                "ratio": ratio,
                "percentile": ln.get("percentile"),
                "avg_own": ln.get("avg_own"),
            })
    if not rows:
        return {"gradable": False, "reason": "no entered lineups"}

    ratios = [x["ratio"] for x in rows if x["ratio"] is not None]
    pcts = [x["percentile"] for x in rows if x["percentile"] is not None]
    return {
        "gradable": True,
        "n_lineups": len(rows),
        "avg_ratio": round(sum(ratios) / len(ratios), 3) if ratios else None,
        "best_percentile": min(pcts) if pcts else None,
        "median_percentile": round(sorted(pcts)[len(pcts) // 2], 1) if pcts else None,
        "n_top_10pct": sum(1 for p in pcts if p <= 10),
        "lineups": rows,
    }


def slate_accuracy(autopsy) -> dict:
    """The per-slate self-grade, persisted as accuracy.json at autopsy-log time."""
    return {"edges": grade_edges(autopsy), "lineups": grade_lineups(autopsy)}


def _history_root(slug: str) -> Path:
    return _REPO_ROOT / "rules" / slug / "history"


def accuracy_rollup(slug: str, last_n: int = 10) -> dict:
    """Trend the self-grade across the most recent archived slates."""
    root = _history_root(slug)
    if not root.exists():
        return {"n": 0, "slates": []}
    dirs = sorted(d for d in root.iterdir() if d.is_dir())[-last_n:]

    slates: list[dict] = []
    for d in dirs:
        ap = d / "autopsy.json"
        if not ap.exists():
            continue
        try:
            rec = json.loads(ap.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        e, ln = grade_edges(rec), grade_lineups(rec)
        slates.append({
            "slate": d.name,
            "leverage_capture": e.get("leverage_capture"),
            "overperformer_capture": e.get("overperformer_capture"),
            "underperformer_exposure": e.get("underperformer_exposure"),
            "avg_ratio": ln.get("avg_ratio"),
            "best_percentile": ln.get("best_percentile"),
        })

    def _avg(key: str, nd: int = 3):
        vals = [s[key] for s in slates if s.get(key) is not None]
        return round(sum(vals) / len(vals), nd) if vals else None

    return {
        "n": len(slates),
        "slates": slates,
        "mean_leverage_capture": _avg("leverage_capture"),
        "mean_overperformer_capture": _avg("overperformer_capture"),
        "mean_underperformer_exposure": _avg("underperformer_exposure"),
        "mean_lineup_ratio": _avg("avg_ratio"),
        "mean_best_percentile": _avg("best_percentile", 1),
    }


def _pct(v) -> str:
    return f"{round(v * 100)}%" if v is not None else "—"


def slate_accuracy_md(autopsy) -> str:
    """Per-slate self-grade as a compact markdown block (Autopsy tab panel)."""
    acc = slate_accuracy(autopsy)
    e, ln = acc["edges"], acc["lineups"]
    out = ["### Self-grade — did our bets pay off?", ""]
    if e.get("gradable"):
        out += [
            f"- **Leverage capture:** {_pct(e['leverage_capture'])} of the slate-defining "
            f"low-owned plays were in our lineups"
            + (f" (missed: {', '.join(e['leverage_missed'])})" if e.get("leverage_missed") else ""),
            f"- **Overperformer capture:** {_pct(e['overperformer_capture'])} of the top "
            f"proj-beaters rostered"
            + (f" ({', '.join(e['overperformer_hit'])})" if e.get("overperformer_hit") else ""),
            f"- **Bust exposure:** {_pct(e['underperformer_exposure'])} of the top proj-missers "
            f"rostered (lower is better)"
            + (f" ({', '.join(e['underperformer_hit'])})" if e.get("underperformer_hit") else ""),
        ]
    else:
        out.append(f"- *Edges not gradable: {e.get('reason')}*")
    if ln.get("gradable"):
        out += [
            f"- **Our lineups:** {ln['n_lineups']} entered · best finish "
            f"{ln['best_percentile']}th pct · avg actual/proj ratio {ln['avg_ratio']} · "
            f"{ln['n_top_10pct']} in the top 10%",
        ]
    else:
        out.append(f"- *Lineups not gradable: {ln.get('reason')}*")
    return "\n".join(out)


def rollup_md(slug: str, last_n: int = 10) -> str:
    """Self-grade trend for the bundle — so the next slate's analysis is anchored
    to how our past reads ACTUALLY did, not vibes."""
    r = accuracy_rollup(slug, last_n)
    if not r["n"]:
        return ""
    lines = [
        f"## Self-grade (how our past reads actually did — last {r['n']} slate(s))",
        "",
        f"- Mean **leverage capture**: {_pct(r['mean_leverage_capture'])} "
        f"(share of slate-defining low-owned plays we owned)",
        f"- Mean **overperformer capture**: {_pct(r['mean_overperformer_capture'])}",
        f"- Mean **bust exposure**: {_pct(r['mean_underperformer_exposure'])} (lower is better)",
        f"- Mean **lineup actual/proj ratio**: {r['mean_lineup_ratio']}",
        f"- Mean **best finish**: {r['mean_best_percentile']}th percentile",
        "",
        "| Slate | Lev capture | Over capture | Bust expo | Ratio | Best pct |",
        "|---|---|---|---|---|---|",
    ]
    for s in r["slates"]:
        lines.append(
            f"| {s['slate']} | {_pct(s['leverage_capture'])} | {_pct(s['overperformer_capture'])} | "
            f"{_pct(s['underperformer_exposure'])} | {s['avg_ratio'] if s['avg_ratio'] is not None else '—'} | "
            f"{s['best_percentile'] if s['best_percentile'] is not None else '—'} |"
        )
    return "\n".join(lines)
