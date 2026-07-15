"""Player-pool tier calibration — is the ranked board actually calibrated?

The Claude-generated player pool tiers every rosterable player and is the
PRIMARY hand-build reference — yet nothing ever checked the tiers against what
actually happened. This grades them: at autopsy-log time, parse the persisted
pool's ranked table (data/player_pool/<slug>.md), join each player to their
actual FPTS from the DK standings, and roll up per-tier averages. If your top
tier keeps scoring no better than your third, the tier boundaries — the thing
your builds lean on — are broken.

Tier-vocabulary-AGNOSTIC: it groups by whatever Tier strings the table used
(Core/Good/Okay/Fade today, Core/Pivot/Dart in older slates), preserving table
order (best tier first) and stripping the orthogonal `· Leverage` label. Output
is archived to <history_dir>/pool_calibration.json, summarized into
results.jsonl (`tier_summary`, `tiers_ordered`) for the process trend, and read
by the post-autopsy review. Pure/deterministic; never blocks the log.
"""
from __future__ import annotations

import re

from src.autopsy import _norm_name

_ROW = re.compile(r"^\s*\|(.+)\|\s*$")


def parse_pool_tiers(md: str) -> list[dict]:
    """(player, tier) rows from the pool's leading ranked table, in table order.
    Empty list when there's no parsable table or no Tier column."""
    if not md:
        return []
    header_cols, tier_i, name_i = None, None, None
    out: list[dict] = []
    for line in md.splitlines():
        m = _ROW.match(line)
        if not m:
            if header_cols is not None and out:
                break  # table ended
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if header_cols is None:
            lowered = [c.lower() for c in cells]
            if "tier" in lowered:
                header_cols = cells
                tier_i = lowered.index("tier")
                name_i = lowered.index("player") if "player" in lowered else 1
            continue
        if set("".join(cells)) <= {"-", ":", " ", ""}:
            continue  # separator row
        if tier_i is None or len(cells) <= max(tier_i, name_i):
            continue
        name = cells[name_i].strip("* ")
        tier_raw = cells[tier_i].strip("*` ")
        # `· Leverage` is orthogonal to quality — strip it off the tier.
        tier = re.split(r"\s*·\s*", tier_raw)[0].strip()
        if name and tier:
            out.append({"name": name, "tier": tier})
    return out


def grade_tiers(pool_md: str, players_df) -> dict:
    """Per-tier actual-FPTS rollup + ordering check + leakage.

    `players_df` = the parsed standings' players frame (name / actual_fpts) —
    scores are identical across the slate's contests, so any contest works."""
    rows = parse_pool_tiers(pool_md)
    if not rows or players_df is None or players_df.empty:
        return {"gradable": False}
    fpts = {}
    for nm, fp in zip(players_df["name"], players_df["actual_fpts"]):
        if fp is not None and fp == fp:
            fpts[_norm_name(nm)] = float(fp)

    tier_order: list[str] = []
    by_tier: dict[str, list[float]] = {}
    matched = 0
    for r in rows:
        t = r["tier"]
        if t not in by_tier:
            by_tier[t] = []
            tier_order.append(t)  # table order = board's best-first order
        f = fpts.get(_norm_name(r["name"]))
        if f is not None:
            by_tier[t].append(f)
            matched += 1
    tiers = []
    for t in tier_order:
        vals = by_tier[t]
        tiers.append({
            "tier": t,
            "n": len(vals),
            "avg_fpts": round(sum(vals) / len(vals), 1) if vals else None,
            "max_fpts": round(max(vals), 1) if vals else None,
        })
    graded = [t for t in tiers if t["avg_fpts"] is not None]
    ordered = all(a["avg_fpts"] >= b["avg_fpts"]
                  for a, b in zip(graded, graded[1:])) if len(graded) >= 2 else None

    # Leakage: a bottom-tier player who outscored the TOP tier's average — the
    # board buried someone who mattered.
    leakage = []
    if graded and graded[0]["avg_fpts"] is not None:
        top_avg = graded[0]["avg_fpts"]
        bottom = tier_order[-1]
        for r in rows:
            if r["tier"] != bottom:
                continue
            f = fpts.get(_norm_name(r["name"]))
            if f is not None and f > top_avg:
                leakage.append({"name": r["name"], "tier": bottom, "fpts": round(f, 1)})

    summary = " > ".join(f"{t['tier']} {t['avg_fpts']}" for t in graded)
    if ordered is not None:
        summary += "  ✓ ordered" if ordered else "  ✗ OUT OF ORDER"
    return {
        "gradable": True,
        "n_pool": len(rows),
        "n_matched": matched,
        "tiers": tiers,
        "tiers_ordered": ordered,
        "leakage": leakage[:5],
        "summary": summary,
    }


def calibration_md(cal: dict) -> str | None:
    if not cal or not cal.get("gradable"):
        return None
    out = [f"### Player-pool tier calibration ({cal['n_matched']} of "
           f"{cal['n_pool']} board players matched to actuals)",
           "| Tier | Players | Avg FPTS | Best |", "|---|---|---|---|"]
    for t in cal["tiers"]:
        out.append(f"| **{t['tier']}** | {t['n']} | {t['avg_fpts']} | {t['max_fpts']} |")
    if cal.get("tiers_ordered") is True:
        out.append("- ✅ Tier ordering HELD — higher tiers outscored lower ones on average.")
    elif cal.get("tiers_ordered") is False:
        out.append("- ⚠️ **Tier ordering BROKE** — a lower tier out-averaged a higher one. "
                   "The board's boundaries need attention.")
    for lk in cal.get("leakage") or []:
        out.append(f"- 🕳️ Buried: **{lk['name']}** ({lk['tier']}) scored {lk['fpts']} — "
                   f"above the top tier's average.")
    return "\n".join(out)
