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

Salary (8/11/26): DK standings carry no salaries, but when the slate's
projections are still loaded at autopsy time, analyze_contest passes a
`salary_map` through — and then every proposed swap is checked against the
$50K cap (the Ventura→James lesson: the points-best swap cost $1,900 more
than the lineup had left, so "one swap away" was impossible). Without salary
data the module degrades to the old points-only read, flagged
`salary_checked: False`. Ownership + FPTS are real actuals, so everything
here is ground truth. Pure/deterministic; synthesis only — it explains what
happened, it never commands a play.
"""
from __future__ import annotations

from itertools import combinations

from src.autopsy import _norm_name

_SALARY_CAP = 50_000

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

    # Salary feasibility: available only when analyze_contest ran with the
    # slate's projections still loaded. A swap must keep the lineup ≤ $50K —
    # salary_checked requires YOUR full roster priced plus every candidate.
    salary_map = analysis.get("salary_map") or {}
    your_sal = [salary_map.get(k) for k in your_roster]
    your_total = sum(your_sal) if all(s is not None for s in your_sal) else None
    for o in your_uniq:
        o["salary"] = salary_map.get(_norm_name(o["name"]))
    for i in win_uniq:
        i["salary"] = salary_map.get(_norm_name(i["name"]))
    salary_checked = (your_total is not None
                      and all(i["salary"] is not None for i in win_uniq))

    def _fits(outs_, ins_) -> bool:
        if not salary_checked:
            return True
        delta = sum(i["salary"] for i in ins_) - sum(o["salary"] for o in outs_)
        return your_total + delta <= _SALARY_CAP

    # Best single swap: your unique OUT → winner's unique IN, max FPTS gain
    # among the swaps the salary cap actually allows. The points-best-but-
    # over-cap swap is kept separately so the display can say why it's absent.
    best_swap = None
    blocked_swap = None
    for o in your_uniq:
        for i in win_uniq:
            if o["fpts"] is None or i["fpts"] is None:
                continue
            cand = {"out": o["name"], "in": i["name"],
                    "gain": round(i["fpts"] - o["fpts"], 1)}
            if _fits([o], [i]):
                if best_swap is None or cand["gain"] > best_swap["gain"]:
                    best_swap = cand
            elif blocked_swap is None or cand["gain"] > blocked_swap["gain"]:
                over = (your_total - o["salary"] + i["salary"]) - _SALARY_CAP
                blocked_swap = {**cand, "over_cap_by": int(over)}
    if best_swap:
        best_swap["would_have_won"] = best_swap["gain"] > gap
    # Only surface the blocked swap when it out-gains every legal one — that's
    # exactly the case where the old points-only read told a false story.
    if blocked_swap and best_swap and blocked_swap["gain"] <= best_swap["gain"]:
        blocked_swap = None

    # Minimum swaps to win: exact search over swap SETS (≤6 uniques a side, so
    # brute force is cheap) — points gained and salary delta both depend only
    # on WHICH players move, not how they pair up. Without salary data this
    # reduces to the best-gain-per-k check (same result as the old greedy).
    swaps_needed = None
    outs = [o for o in your_uniq if o["fpts"] is not None]
    ins = [i for i in win_uniq if i["fpts"] is not None]
    for k in range(1, min(len(outs), len(ins)) + 1):
        found = False
        for out_set in combinations(outs, k):
            for in_set in combinations(ins, k):
                gain = sum(i["fpts"] for i in in_set) - sum(o["fpts"] for o in out_set)
                if gain > gap and _fits(out_set, in_set):
                    found = True
                    break
            if found:
                break
        if found:
            swaps_needed = k
            break

    return {
        "salary_checked": salary_checked,
        "blocked_swap": blocked_swap,
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
            if miss.get("blocked_swap"):
                b = miss["blocked_swap"]
                head += (f" The points-best swap ({b['out']} → {b['in']}, +{b['gain']} pts) "
                         f"did NOT fit under the $50K salary cap (over by ${b['over_cap_by']:,}).")
            if miss.get("best_swap"):
                s = miss["best_swap"]
                verdict = ("**that ONE swap wins the contest**" if s["would_have_won"]
                           else "not enough alone")
                fit = " that fits the cap" if miss.get("salary_checked") else ""
                head += (f" Best single swap{fit}: {s['out']} → **{s['in']}** "
                         f"(+{s['gain']} pts — {verdict}).")
            elif miss.get("blocked_swap"):
                head += " No single swap fits under the cap."
            if miss.get("swaps_needed"):
                cap_note = (" (salary-cap checked)" if miss.get("salary_checked")
                            else " (salary not checked — projections were cleared)")
                head += f" Minimum swaps to win: **{miss['swaps_needed']}**{cap_note}."
            elif miss.get("best_swap") or miss.get("blocked_swap"):
                head += " Even swapping every differing player wouldn't have won — structural, not marginal."
            out.append(head)
    return "\n\n".join(out) if out else None
