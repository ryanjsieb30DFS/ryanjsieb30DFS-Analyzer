"""Field / Fish analysis — how opponents play a contest, so future builds can
leverage AWAY from the crowd.

The inverse of `shark_gap`: instead of "what did the sharks do," this profiles
(a) where the WHOLE FIELD converges — the chalk players and roster combinations
so many entries share that they're dupe magnets — and (b) the FISH specifically —
the bottom finishers vs the winners, and the plays the losing crowd loved that
winners faded. Standings-only (Rank, EntryName, Lineup, field `actual_own`), so it
fits the "autopsy = standings only" rule.

Pure functions. The Autopsy tab renders it as a "leverage away from this" fade
board; `field_tendencies` accumulates it per contest type for the forward-looking
picture ("this contest type reliably crowds X").
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations

import pandas as pd

from src.autopsy import _norm_name, is_user_entry

_DART_OWN = 5.0        # a sub-this-% field-owned play is a leverage "dart"
_WINNER_FRAC = 0.01    # top 1% by rank = "winners"


def _profile(rosters: list[list[str]], own_map: dict) -> dict | None:
    """Structural fingerprint of a set of lineups: avg field-own per slot, share
    carrying a sub-5% dart, unique %, from field ownership alone."""
    if not rosters:
        return None
    per_own, dart_hits = [], 0
    for lp in rosters:
        owns = [own_map.get(_norm_name(p)) for p in lp]
        owns = [o for o in owns if o is not None]
        if owns:
            per_own.append(sum(owns) / len(owns))
            if any(o < _DART_OWN for o in owns):
                dart_hits += 1
    n = len(rosters)
    uniq = len({frozenset(_norm_name(p) for p in lp) for lp in rosters})
    return {
        "n": n,
        "avg_own_per_slot": round(sum(per_own) / len(per_own), 1) if per_own else None,
        "dart_pct": round(dart_hits / n * 100, 1),
        "unique_pct": round(uniq / n * 100, 1),
    }


def field_profile(parsed: dict, sport: str, contest_type: str | None = None,
                  fish_frac: float = 0.5, top_k: int = 10) -> dict:
    """Profile the field + fish for one contest's standings. See module docstring."""
    lineups = parsed["lineups"]
    players = parsed["players"]
    own_map = dict(zip(players["name"].apply(_norm_name), players["actual_own"]))
    fpts_map = dict(zip(players["name"].apply(_norm_name), players["actual_fpts"]))
    display = {_norm_name(n): n for n in players["name"]}

    valid = lineups[lineups["Lineup_parsed"].apply(len) > 0].copy()
    field_size = int(len(valid))
    if field_size == 0:
        return {"gradable": False, "field_size": 0}

    # Everyone but us = the field. Fish = the bottom fraction; winners = top 1%.
    non_user = valid[~valid["EntryName"].apply(is_user_entry)]
    field_rosters = list(non_user["Lineup_parsed"])

    # ---- Crowd convergence -------------------------------------------------
    # Crowded players: highest field ownership (the chalk the crowd piles on),
    # tagged with actual fpts so a chalk trap (owned + dud) stands out.
    crowded_players = [
        {"name": display.get(nm, nm), "field_own": round(float(o), 1),
         "actual_fpts": round(float(fpts_map.get(nm, 0.0)), 1)}
        for nm, o in sorted(own_map.items(), key=lambda x: -x[1])[:top_k]
    ]
    # Crowded pairs: player duos many field lineups share = dupe magnets.
    pair_ct: Counter = Counter()
    for lp in field_rosters:
        norms = sorted({_norm_name(p) for p in lp})
        for a, b in combinations(norms, 2):
            pair_ct[(a, b)] += 1
    nf = len(field_rosters) or 1
    crowded_combos = [
        {"players": [display.get(a, a), display.get(b, b)],
         "field_pct": round(c / nf * 100, 1), "count": c}
        for (a, b), c in pair_ct.most_common(top_k)
    ]
    # Dupe magnets: the exact rosters the most field entries share.
    roster_ct = Counter(frozenset(_norm_name(p) for p in lp) for lp in field_rosters)
    dupe_magnets = [
        {"players": sorted(display.get(n, n) for n in rs), "count": c,
         "field_pct": round(c / nf * 100, 1)}
        for rs, c in roster_ct.most_common(5) if c > 1
    ]

    # ---- Fish vs winners ---------------------------------------------------
    ranked = non_user.sort_values("Rank")
    n_win = max(1, round(_WINNER_FRAC * field_size))
    winners_rosters = list(ranked.head(n_win)["Lineup_parsed"])
    n_fish = max(1, round(fish_frac * len(ranked)))
    fish_rosters = list(ranked.tail(n_fish)["Lineup_parsed"])
    winners_profile = _profile(winners_rosters, own_map)
    fish_profile = _profile(fish_rosters, own_map)

    def _exposure(rosters):
        n = len(rosters) or 1
        ct: Counter = Counter()
        for lp in rosters:
            for p in {_norm_name(x) for x in lp}:
                ct[p] += 1
        return {p: c / n for p, c in ct.items()}

    win_exp, fish_exp = _exposure(winners_rosters), _exposure(fish_rosters)
    fish_traps = sorted(
        ({"name": display.get(p, p),
          "fish_pct": round(fish_exp[p] * 100, 1),
          "winner_pct": round(win_exp.get(p, 0.0) * 100, 1),
          "gap": round((fish_exp[p] - win_exp.get(p, 0.0)) * 100, 1),
          "actual_fpts": round(float(fpts_map.get(p, 0.0)), 1)}
         for p in fish_exp),
        key=lambda d: -d["gap"],
    )
    fish_traps = [t for t in fish_traps if t["gap"] > 0][:top_k]

    # ---- Auto read ---------------------------------------------------------
    read = []
    if crowded_players:
        cp = crowded_players[0]
        read.append(f"Field crowded **{cp['name']}** at {cp['field_own']}% "
                    f"({cp['actual_fpts']} fpts) — the chalk to consider fading.")
    if crowded_combos and crowded_combos[0]["field_pct"] >= 8:
        cc = crowded_combos[0]
        read.append(f"**{cc['players'][0]} + {cc['players'][1]}** were together in "
                    f"{cc['field_pct']}% of field lineups — a dupe magnet; break the pair.")
    if fish_traps:
        ft = fish_traps[0]
        read.append(f"**{ft['name']}** was a fish trap: {ft['fish_pct']}% of the fish, "
                    f"only {ft['winner_pct']}% of winners.")
    if fish_profile and winners_profile and fish_profile.get("avg_own_per_slot") and winners_profile.get("avg_own_per_slot"):
        d = round(fish_profile["avg_own_per_slot"] - winners_profile["avg_own_per_slot"], 1)
        if d > 0:
            read.append(f"Fish ran {d} pts/slot more chalk than winners "
                        f"({fish_profile['avg_own_per_slot']}% vs {winners_profile['avg_own_per_slot']}%).")

    # ---- Recurring opponents: the handles that finished HIGH in THIS contest
    # (the players you're actually up against), best rank per handle. Accumulated
    # per contest by field_tendencies to surface who recurs week to week.
    def _handle(entry_name) -> str:
        return str(entry_name).split("(")[0].strip()

    top_opponents, _seen_h = [], set()
    for _, orow in ranked.iterrows():
        h = _handle(orow["EntryName"])
        hn = h.casefold()
        if not h or hn in _seen_h:
            continue
        _seen_h.add(hn)
        top_opponents.append({
            "handle": h,
            "best_rank": int(orow["Rank"]),
            "percentile": round(100.0 * int(orow["Rank"]) / field_size, 1),
        })
        if len(top_opponents) >= 15:
            break

    return {
        "gradable": True,
        "field_size": field_size,
        "contest_type": contest_type,
        "crowded_players": crowded_players,
        "crowded_combos": crowded_combos,
        "dupe_magnets": dupe_magnets,
        "winners_profile": winners_profile,
        "fish_profile": fish_profile,
        "fish_traps": fish_traps,
        "top_opponents": top_opponents,
        "read": read,
    }
