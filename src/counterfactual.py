"""Near-miss counterfactual + winner build story — standings-only.

Every autopsy already holds your entered lineups AND the winner's full roster,
but nothing answered the small-field GPP question that matters most post-contest:
**were you one swap away, or a structural rebuild away?** This module computes:

  - `near_miss`  — your best lineup vs the winning lineup: the points gap, the
    players you shared, the exact roster delta with each player's actual FPTS,
    the single best swap (your player OUT → winner's player IN) and whether that
    one swap would have WON the contest, plus the minimum number of swaps needed.
  - `winner_story` — how the winning lineup was BUILT (ownership-wise): its
    average ownership, the sub-10% pieces it carried, the lowest-owned player
    that carried it (the leverage that actually won), and the ownership product →
    expected duplicates in this field (the dupe risk the winner accepted).

Salary is deliberately absent: DK standings carry no salaries and the autopsy is
standings-only (projections don't exist at autopsy time). Ownership + FPTS are
real actuals, so everything here is ground truth. Pure/deterministic; synthesis
only — it explains what happened, it never commands a play.
"""
from __future__ import annotations

from src.autopsy import _norm_name

# "Leverage piece" threshold for the winner-story read (matches shark_gap's
# sub-10 low-own convention for definers; sub-5 is the dart line).
_LOW_OWN = 10.0


def _fpts_own_maps(parsed: dict) -> tuple[dict, dict]:
    P = parsed["players"]
    fpts = {}
    own = {}
    for nm, fp, ow in zip(P["name"], P["actual_fpts"], P["actual_own"]):
        n = _norm_name(nm)
        if fp is not None and fp == fp:  # not NaN
            fpts[n] = float(fp)
        if ow is not None and ow == ow:
            own[n] = float(ow)
    return fpts, own


def _winner_row(parsed: dict):
    L = parsed["lineups"]
    if L.empty:
        return None
    return L.loc[L["Points"].idxmax()]


def winner_story(parsed: dict) -> dict:
    """How the winning lineup was built, ownership-wise (standings-only)."""
    w = _winner_row(parsed)
    if w is None or not w["Lineup_parsed"]:
        return {"gradable": False}
    fpts, own = _fpts_own_maps(parsed)
    roster = list(w["Lineup_parsed"])
    rows = []
    for p in roster:
        n = _norm_name(p)
        rows.append({"name": p, "own": own.get(n), "fpts": fpts.get(n)})
    known_own = [r["own"] for r in rows if r["own"] is not None]
    if not known_own:
        return {"gradable": False}

    field = len(parsed["lineups"])
    # Dupe risk the winner accepted: P(random field lineup = this roster) under
    # independence ~ product of ownerships; × field = expected duplicates.
    prod = 1.0
    for o in known_own:
        prod *= o / 100.0
    expected_dupes = prod * field

    low = [r for r in rows if r["own"] is not None and r["own"] < _LOW_OWN]
    # The leverage that WON: the low-owned piece with the biggest actual score
    # (fall back to lowest-owned when none scored).
    carrier = (max(low, key=lambda r: r["fpts"] or 0.0)
               if low else min(rows, key=lambda r: r["own"] if r["own"] is not None else 101))
    return {
        "gradable": True,
        "winner_points": float(w["Points"]),
        "winner_handle": str(w["EntryName"]).split("(")[0].strip(),
        "roster": rows,
        "avg_own": round(sum(known_own) / len(known_own), 1),
        "n_low_own": len(low),
        "carrier": carrier,  # the leverage piece that carried it
        "expected_dupes": round(expected_dupes, 2),
    }


def near_miss(parsed: dict, analysis: dict) -> dict:
    """Your best lineup vs the winner: gap, shared core, roster delta, the best
    single swap, and the minimum swaps that would have won it."""
    user_df = analysis.get("user_lineups_df")
    if user_df is None or user_df.empty:
        return {"gradable": False}
    w = _winner_row(parsed)
    if w is None or not w["Lineup_parsed"]:
        return {"gradable": False}

    # user_lineups_df is the PROFILED frame (lowercase schema: rank/points/players).
    best = user_df.loc[user_df["points"].idxmax()]
    your_pts = float(best["points"])
    win_pts = float(w["Points"])
    if your_pts >= win_pts:
        return {"gradable": True, "won": True, "your_points": your_pts,
                "winner_points": win_pts}

    fpts, _own = _fpts_own_maps(parsed)
    your_roster = {_norm_name(p): p for p in (best["players"] or [])}
    win_roster = {_norm_name(p): p for p in (w["Lineup_parsed"] or [])}
    shared = sorted(your_roster[k] for k in your_roster.keys() & win_roster.keys())
    your_uniq = [{"name": your_roster[k], "fpts": fpts.get(k)}
                 for k in your_roster.keys() - win_roster.keys()]
    win_uniq = [{"name": win_roster[k], "fpts": fpts.get(k)}
                for k in win_roster.keys() - your_roster.keys()]

    gap = win_pts - your_pts
    # Best single swap: your unique OUT → winner's unique IN, max FPTS gain.
    best_swap = None
    for o in your_uniq:
        for i in win_uniq:
            if o["fpts"] is None or i["fpts"] is None:
                continue
            gain = i["fpts"] - o["fpts"]
            if best_swap is None or gain > best_swap["gain"]:
                best_swap = {"out": o["name"], "in": i["name"],
                             "gain": round(gain, 1)}
    if best_swap:
        best_swap["would_have_won"] = best_swap["gain"] > gap

    # Minimum swaps to win: greedily pair your worst uniques out for the
    # winner's best uniques in until the cumulative gain clears the gap.
    swaps_needed = None
    outs = sorted((o for o in your_uniq if o["fpts"] is not None), key=lambda r: r["fpts"])
    ins = sorted((i for i in win_uniq if i["fpts"] is not None),
                 key=lambda r: r["fpts"], reverse=True)
    cum = 0.0
    for k, (o, i) in enumerate(zip(outs, ins), start=1):
        cum += i["fpts"] - o["fpts"]
        if cum > gap:
            swaps_needed = k
            break

    return {
        "gradable": True,
        "won": False,
        "your_points": your_pts,
        "winner_points": win_pts,
        "gap": round(gap, 1),
        "your_percentile": (round(float(best["rank"]) / len(parsed["lineups"]) * 100, 1)
                            if "rank" in best else None),
        "n_shared": len(shared),
        "shared": shared,
        "your_uniques": sorted(your_uniq, key=lambda r: -(r["fpts"] or 0)),
        "winner_uniques": sorted(win_uniq, key=lambda r: -(r["fpts"] or 0)),
        "best_swap": best_swap,
        "swaps_needed": swaps_needed,  # None = even swapping all deltas wouldn't win
    }


def counterfactual_md(story: dict, miss: dict) -> str | None:
    """Compact markdown block for the Autopsy tab. None when nothing gradable."""
    out: list[str] = []
    if story and story.get("gradable"):
        c = story["carrier"]
        c_bit = (f"**{c['name']}** ({c['own']:.0f}% own, {c['fpts']:.1f} FPTS)"
                 if c.get("own") is not None and c.get("fpts") is not None
                 else f"**{c['name']}**")
        out.append(
            f"**🏆 How the winner was built:** {story['winner_points']:.1f} pts by "
            f"`{story['winner_handle']}` — avg own {story['avg_own']}%, "
            f"{story['n_low_own']} sub-10% piece(s); the leverage that carried it: {c_bit}. "
            f"Dupe risk accepted: ~{story['expected_dupes']} expected duplicate(s) in this field."
        )
    if miss and miss.get("gradable"):
        if miss.get("won"):
            out.append(f"**🎯 You WON this contest** ({miss['your_points']:.1f} pts).")
        else:
            head = (f"**🎯 Near-miss:** your best lineup scored {miss['your_points']:.1f} "
                    f"({miss['gap']} back), sharing {miss['n_shared']} player(s) with the winner.")
            if miss.get("best_swap"):
                s = miss["best_swap"]
                verdict = ("**that ONE swap wins the contest**" if s["would_have_won"]
                           else "not enough alone")
                head += (f" Best single swap: {s['out']} → **{s['in']}** "
                         f"(+{s['gain']} pts — {verdict}).")
            if miss.get("swaps_needed"):
                head += f" Minimum swaps to win: **{miss['swaps_needed']}**."
            elif miss.get("best_swap"):
                head += " Even swapping every differing player wouldn't have won — structural, not marginal."
            out.append(head)
    return "\n\n".join(out) if out else None
