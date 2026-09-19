"""MMA MME (150-max) portfolio autopsy — the field, the big stacks, and you.

Born 9/19/26 from the first two readable UFC $80K MEGA mini-MAX standings
files (9/5 and 9/12/26, 31,708 entries each). In a 150-max contest the
question is no longer "did my one lineup win" but "did my PORTFOLIO look
like the portfolios that win": how the 90-odd full-stake players spread
their entries, how chalky the top 1% was, how duplicated the winners were,
and where the user's stack sits against the big players on every axis.

SHARED VERBATIM between the Analyzer and the Sim (a cross-repo parity test
compares the two files byte for byte). Pure Python on purpose: no pandas,
so the same file runs in both repos and in a test with no fixtures.

Descriptive only. Nothing here is a rule — the Analyzer's post-autopsy
review reads the report and proposes lessons; the user approves them.

Inputs (both repos already have them from a parsed DK standings file):
  entries  — one dict per lineup: {"rank": int, "entry_name": str,
             "points": float, "players": [names]}. Empty rosters skipped.
  own_map  — {player name: field ownership %} keyed the SAME way as the
             names in `entries` (raw in the Sim, normalized in the Analyzer).
  is_user  — callable(entry_name) -> bool, the user's entries.
"""
from __future__ import annotations

import math
import re
from collections import Counter

# A field this size or larger is an MME field (matches the Sim's
# MMA_MME_FIELD_THRESHOLD routing cut). Smaller MMA contests are the SE /
# 3-max home game and get no portfolio read.
MME_FIELD_MIN = 5_000
# "Big player" = the stakes the user is now playing at (100 entries, 9/19/26).
BIG_PLAYER_MIN_ENTRIES = 100
# DK pays roughly the top 20% in the mini-MAX; used ONLY when the caller has
# no places-paid figure, and flagged as an estimate in the report.
CASH_SHARE_FALLBACK = 0.20
_ENTRY_SUFFIX = re.compile(r"\s*\(\d+/\d+\)\s*$")

_MIX_BUCKETS = (
    (1, 1, "1 entry"), (2, 5, "2-5"), (6, 20, "6-20"), (21, 50, "21-50"),
    (51, 100, "51-100"), (101, 149, "101-149"), (150, 10**9, "150 (full stake)"),
)


def strip_entry_suffix(name) -> str:
    """'RyvlesGaming30 (4/6)' -> 'RyvlesGaming30'."""
    return _ENTRY_SUFFIX.sub("", str(name or "")).strip()


def _median(vals) -> float | None:
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return None
    n = len(vals)
    mid = n // 2
    return float(vals[mid]) if n % 2 else float((vals[mid - 1] + vals[mid]) / 2)


def _mean(vals) -> float | None:
    vals = [v for v in vals if v is not None]
    return float(sum(vals) / len(vals)) if vals else None


def _pearson(xs, ys) -> float | None:
    if len(xs) < 3:
        return None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return round(sxy / math.sqrt(sxx * syy), 2)


def _r(v, nd=1):
    return None if v is None else round(float(v), nd)


def _shape(rows: list[dict]) -> dict:
    """Ownership shape of a set of lineups: how chalky, how low the lowest
    piece, how many true punts (under 10% owned)."""
    if not rows:
        return {"n": 0, "sum_own_med": None, "min_own_med": None, "sub10_mean": None}
    return {
        "n": len(rows),
        "sum_own_med": _r(_median(r["sum_own"] for r in rows)),
        "min_own_med": _r(_median(r["min_own"] for r in rows)),
        "sub10_mean": _r(_mean(r["sub10"] for r in rows), 2),
    }


def _portfolio(rows: list[dict], n_field: int, top1_cut: int, top10_cut: int,
               cash_cut: int, dup_counts: Counter) -> dict:
    """One user's stack: results + exposure structure."""
    n = len(rows)
    c = Counter(p for r in rows for p in r["players"])
    exps = sorted((v / n for v in c.values()), reverse=True)
    return {
        "n": n,
        "best_rank": min(r["rank"] for r in rows),
        "top1_pct": _r(100 * sum(r["rank"] <= top1_cut for r in rows) / n),
        "top10_pct": _r(100 * sum(r["rank"] <= top10_cut for r in rows) / n),
        "cash_pct": _r(100 * sum(r["rank"] <= cash_cut for r in rows) / n),
        "median_points": _r(_median(r["points"] for r in rows)),
        "max_exposure_pct": _r(100 * exps[0]) if exps else None,
        "n_over_50pct": int(sum(e > 0.5 for e in exps)),
        "n_over_30pct": int(sum(e > 0.3 for e in exps)),
        "fighters_used": len(c),
        "hhi": _r(sum(e * e for e in exps), 3),
        "own_med": _r(_median(r["sum_own"] for r in rows)),
        "min_own_med": _r(_median(r["min_own"] for r in rows)),
        "sub10_mean": _r(_mean(r["sub10"] for r in rows), 2),
        "field_copies_mean": _r(_mean(dup_counts[r["key"]] for r in rows)),
        "within_unique_pct": _r(100 * len({r["key"] for r in rows}) / n),
        "exposures": [{"name": p, "pct": _r(100 * v / n)}
                      for p, v in c.most_common(10)],
    }


def _thirds(items: list[dict], key: str, labels: tuple) -> list[dict]:
    """Split big players into three groups on `key` and average the results
    in each — the cheap, honest version of 'does X predict finishing well'."""
    ranked = sorted((i for i in items if i.get(key) is not None), key=lambda i: i[key])
    if len(ranked) < 6:
        return []
    k = len(ranked) // 3
    groups = [ranked[:k], ranked[k:2 * k], ranked[2 * k:]]
    out = []
    for label, g in zip(labels, groups):
        out.append({
            "group": label, "n": len(g),
            f"{key}_mean": _r(_mean(i[key] for i in g), 2),
            "top1_pct": _r(_mean(i["top1_pct"] for i in g)),
            "top10_pct": _r(_mean(i["top10_pct"] for i in g)),
            "cash_pct": _r(_mean(i["cash_pct"] for i in g)),
        })
    return out


def portfolio_report(entries: list[dict], own_map: dict, is_user=None,
                     places_paid: int | None = None,
                     min_field: int = MME_FIELD_MIN) -> dict:
    """The MME portfolio read for one contest. Returns {"gradable": False,
    "reason": ...} for a small field or when nothing parses."""
    rows = []
    for e in entries:
        players = [p for p in (e.get("players") or []) if p]
        if not players:
            continue
        owns = [float(own_map.get(p, 0) or 0) for p in players]
        rows.append({
            "rank": int(e["rank"]),
            "user": strip_entry_suffix(e.get("entry_name")),
            "entry_name": str(e.get("entry_name") or ""),
            "points": float(e.get("points") or 0),
            "players": tuple(players),
            "key": tuple(sorted(players)),
            "sum_own": sum(owns),
            "min_own": min(owns),
            "sub10": sum(o < 10 for o in owns),
        })
    n_field = len(rows)
    if n_field == 0:
        return {"gradable": False, "reason": "no lineups parsed", "n_field": 0}
    if n_field < min_field:
        return {"gradable": False, "n_field": n_field,
                "reason": f"field of {n_field:,} is below the MME cut ({min_field:,})"}

    top1_cut = max(1, round(0.01 * n_field))
    top10_cut = max(1, round(0.10 * n_field))
    cash_est = places_paid is None
    cash_cut = int(places_paid) if places_paid else max(1, round(CASH_SHARE_FALLBACK * n_field))
    dup_counts = Counter(r["key"] for r in rows)

    by_user: dict[str, list[dict]] = {}
    for r in rows:
        by_user.setdefault(r["user"], []).append(r)
    top1_rows = [r for r in rows if r["rank"] <= top1_cut]
    top10_rows = [r for r in rows if r["rank"] <= top10_cut]

    # --- who is in the field, by stake size ------------------------------
    mix = []
    for lo, hi, label in _MIX_BUCKETS:
        users = [u for u, rs in by_user.items() if lo <= len(rs) <= hi]
        n_ent = sum(len(by_user[u]) for u in users)
        n_top1 = sum(1 for r in top1_rows if lo <= len(by_user[r["user"]]) <= hi)
        mix.append({
            "bucket": label, "users": len(users), "entries": n_ent,
            "field_share_pct": _r(100 * n_ent / n_field),
            "top1_entries": n_top1,
            "top1_share_pct": _r(100 * n_top1 / len(top1_rows)) if top1_rows else None,
        })

    # --- lineup shape: winner / top 1% / top 10% / field ------------------
    winner = min(rows, key=lambda r: r["rank"])
    shape = {
        "winner": _shape([winner]), "top1": _shape(top1_rows),
        "top10": _shape(top10_rows), "field": _shape(rows),
    }

    # --- who the top 1% rostered vs the field -----------------------------
    t1c = Counter(p for r in top1_rows for p in r["players"])
    fighters = []
    for p, own in own_map.items():
        use = 100 * t1c.get(p, 0) / len(top1_rows) if top1_rows else 0
        own_f = float(own or 0)
        fighters.append({
            "name": p, "own_pct": _r(own_f), "top1_use_pct": _r(use),
            "leverage": _r(use / own_f, 2) if own_f > 0 else None,
        })
    fighters.sort(key=lambda f: -(f["top1_use_pct"] or 0))

    # --- duplication ------------------------------------------------------
    dupes = {
        "unique_lineups": len(dup_counts),
        "unique_pct": _r(100 * len(dup_counts) / n_field),
        "max_copies": max(dup_counts.values()),
        "winner_copies": dup_counts[winner["key"]],
        "top1_median_copies": _r(_median(dup_counts[r["key"]] for r in top1_rows)),
        "field_median_copies": _r(_median(dup_counts[r["key"]] for r in rows)),
        "top1_one_of_one_pct": _r(100 * sum(dup_counts[r["key"]] == 1 for r in top1_rows)
                                  / len(top1_rows)) if top1_rows else None,
        "field_one_of_one_pct": _r(100 * sum(dup_counts[r["key"]] == 1 for r in rows) / n_field),
    }

    # --- the big players (the user's stake class) -------------------------
    big = []
    for u, rs in by_user.items():
        if len(rs) >= BIG_PLAYER_MIN_ENTRIES:
            big.append({"user": u, **_portfolio(rs, n_field, top1_cut, top10_cut,
                                                cash_cut, dup_counts)})
    big_block = {"min_entries": BIG_PLAYER_MIN_ENTRIES, "n": len(big)}
    if big:
        top1s = [b["top1_pct"] for b in big]
        big_block.update({
            "top1_median": _r(_median(top1s)),
            "top1_best": _r(max(top1s)),
            "top10_median": _r(_median(b["top10_pct"] for b in big)),
            "cash_median": _r(_median(b["cash_pct"] for b in big)),
            "max_exposure_median": _r(_median(b["max_exposure_pct"] for b in big)),
            "fighters_used_median": _r(_median(b["fighters_used"] for b in big)),
            "own_med_median": _r(_median(b["own_med"] for b in big)),
            # Does an axis predict finishing well? Pearson over the big players.
            "corr_with_top1": {
                "own_med": _pearson([b["own_med"] for b in big], top1s),
                "max_exposure_pct": _pearson([b["max_exposure_pct"] for b in big], top1s),
                "hhi": _pearson([b["hhi"] for b in big], top1s),
                "field_copies_mean": _pearson([b["field_copies_mean"] for b in big], top1s),
                "fighters_used": _pearson([float(b["fighters_used"]) for b in big], top1s),
            },
            "corr_with_cash": {
                "own_med": _pearson([b["own_med"] for b in big],
                                    [b["cash_pct"] for b in big]),
                "max_exposure_pct": _pearson([b["max_exposure_pct"] for b in big],
                                             [b["cash_pct"] for b in big]),
            },
            "thirds_by_own": _thirds(big, "own_med", ("least chalky", "middle", "most chalky")),
            "thirds_by_hhi": _thirds(big, "hhi", ("most spread", "middle", "most concentrated")),
            "thirds_by_copies": _thirds(big, "field_copies_mean",
                                        ("most unique", "middle", "most copied")),
            "best": sorted(big, key=lambda b: (-b["top1_pct"], -b["top10_pct"]))[:5],
        })

    # --- the user --------------------------------------------------------
    user_block = None
    if is_user is not None:
        mine = [r for r in rows if is_user(r["entry_name"])]
        if mine:
            user_block = _portfolio(mine, n_field, top1_cut, top10_cut, cash_cut, dup_counts)
            if big:
                user_block["vs_big_median"] = {
                    k: _r(user_block[k] - big_block[m])
                    for k, m in (("top1_pct", "top1_median"), ("top10_pct", "top10_median"),
                                 ("cash_pct", "cash_median"),
                                 ("max_exposure_pct", "max_exposure_median"),
                                 ("fighters_used", "fighters_used_median"),
                                 ("own_med", "own_med_median"))
                    if user_block.get(k) is not None and big_block.get(m) is not None
                }

    return {
        "gradable": True,
        "n_field": n_field,
        "n_users": len(by_user),
        "top1_cut": top1_cut,
        "top10_cut": top10_cut,
        "cash_cut": cash_cut,
        "cash_cut_estimated": cash_est,
        "entrant_mix": mix,
        "shape": shape,
        "winner": {
            "entry_name": winner["entry_name"], "user": winner["user"],
            "user_entries": len(by_user[winner["user"]]),
            "points": _r(winner["points"]), "copies": dup_counts[winner["key"]],
            "sum_own": _r(winner["sum_own"]), "min_own": _r(winner["min_own"]),
            "players": [{"name": p, "own_pct": _r(own_map.get(p, 0))} for p in winner["players"]],
        },
        "fighters": fighters[:20],
        "dupes": dupes,
        "big_players": big_block,
        "user": user_block,
    }


def portfolio_summary(report: dict | None) -> str | None:
    """One line for results.jsonl / the archive index."""
    if not report or not report.get("gradable"):
        return None
    s = report["shape"]
    d = report["dupes"]
    line = (f"top 1% summed {s['top1']['sum_own_med']}% own vs field {s['field']['sum_own_med']}%, "
            f"{s['top1']['sub10_mean']} sub-10% pieces per lineup; winner copied "
            f"{d['winner_copies']}x; {d['top1_one_of_one_pct']}% of the top 1% were one-of-one")
    u = report.get("user")
    if u:
        line += (f"; you: {u['n']} entries, top-1% rate {u['top1_pct']}%, "
                 f"cash {u['cash_pct']}%")
        b = report.get("big_players") or {}
        if b.get("top1_median") is not None:
            line += f" (big-stack median {b['top1_median']}% / {b['cash_median']}%)"
    return line


def _pct(v) -> str:
    return "—" if v is None else f"{v:.0f}%"


def _num(v, nd=1) -> str:
    return "—" if v is None else f"{v:.{nd}f}"


def portfolio_md(report: dict | None, source_file: str | None = None) -> str:
    """The markdown block for autopsies.md and the Autopsy tab. Plain
    language: every DFS word gets its meaning next to it."""
    if not report:
        return ""
    title = "### 150-max portfolio read" + (f" — {source_file}" if source_file else "")
    if not report.get("gradable"):
        return f"{title}\n- Not graded: {report.get('reason', 'no data')}."
    L = [title,
         f"- Field: {report['n_field']:,} entries from {report['n_users']:,} people. "
         f"Top 1% = rank {report['top1_cut']:,} or better; cash line = rank "
         f"{report['cash_cut']:,}" + (" (estimated at 20% paid)" if report["cash_cut_estimated"] else "") + "."]

    L += ["", "**Who is in the field (by how many entries each person played)**", "",
          "| Entries per person | People | Share of field | Share of top 1% |",
          "|---|---:|---:|---:|"]
    for m in report["entrant_mix"]:
        L.append(f"| {m['bucket']} | {m['users']:,} | {_pct(m['field_share_pct'])} | "
                 f"{_pct(m['top1_share_pct'])} |")

    s = report["shape"]
    L += ["", "**Lineup shape — summed ownership (how chalky), lowest-owned piece, and punts "
          "(fighters under 10% owned)**", "",
          "| Group | Summed own (median) | Lowest piece (median) | Punts per lineup |",
          "|---|---:|---:|---:|"]
    for label, key in (("Winner", "winner"), ("Top 1%", "top1"), ("Top 10%", "top10"), ("Whole field", "field")):
        g = s[key]
        L.append(f"| {label} | {_pct(g['sum_own_med'])} | {_pct(g['min_own_med'])} | {_num(g['sub10_mean'], 2)} |")

    w = report["winner"]
    L += ["", f"**Winner:** {w['user']} ({w['user_entries']} entries), {_num(w['points'])} points, "
          f"this exact roster appeared {w['copies']}x in the field. "
          + " · ".join(f"{p['name']} {_pct(p['own_pct'])}" for p in w["players"])]

    d = report["dupes"]
    L += ["", f"**Duplication:** {d['unique_pct']}% of the field's lineups were unique "
          f"({d['unique_lineups']:,} distinct rosters; the most-copied roster appeared "
          f"{d['max_copies']}x). Top-1% lineups were copied a median {_num(d['top1_median_copies'], 0)}x "
          f"vs {_num(d['field_median_copies'], 0)}x for the field; {_pct(d['top1_one_of_one_pct'])} of "
          f"the top 1% were one-of-one vs {_pct(d['field_one_of_one_pct'])} of the field."]

    L += ["", "**Who the top 1% rostered (top-1% use vs field ownership; 'lift' = use ÷ own)**", "",
          "| Fighter | Field own | In top-1% lineups | Lift |", "|---|---:|---:|---:|"]
    for f in report["fighters"][:12]:
        L.append(f"| {f['name']} | {_pct(f['own_pct'])} | {_pct(f['top1_use_pct'])} | {_num(f['leverage'], 2)} |")

    b = report["big_players"]
    if b.get("n"):
        L += ["", f"**The big stacks ({b['n']} people with {b['min_entries']}+ entries)** — "
              f"median top-1% rate {_pct(b['top1_median'])} (best {_pct(b['top1_best'])}), "
              f"top-10% {_pct(b['top10_median'])}, cash {_pct(b['cash_median'])}; typical stack: "
              f"biggest single exposure {_pct(b['max_exposure_median'])}, "
              f"{_num(b['fighters_used_median'], 0)} fighters used, summed own {_pct(b['own_med_median'])}."]
        c1, c2 = b["corr_with_top1"], b["corr_with_cash"]
        L.append(f"- Correlation with top-1% rate (−1 to +1; near 0 = no link): chalkiness "
                 f"{_num(c1['own_med'], 2)}, biggest exposure {_num(c1['max_exposure_pct'], 2)}, "
                 f"concentration {_num(c1['hhi'], 2)}, field copies {_num(c1['field_copies_mean'], 2)}, "
                 f"fighters used {_num(c1['fighters_used'], 2)}. With cash rate: chalkiness "
                 f"{_num(c2['own_med'], 2)}, biggest exposure {_num(c2['max_exposure_pct'], 2)}.")
        for key, label in (("thirds_by_own", "Split by chalkiness"),
                           ("thirds_by_hhi", "Split by concentration"),
                           ("thirds_by_copies", "Split by how copied their lineups were")):
            t = b.get(key) or []
            if t:
                L.append(f"- {label}: " + "; ".join(
                    f"{g['group']} → top-1% {_pct(g['top1_pct'])}, cash {_pct(g['cash_pct'])}" for g in t))
        L += ["", "| Best big stacks | Entries | Best rank | Top 1% | Top 10% | Cash | Max exposure | Fighters used | Summed own |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for p in b["best"]:
            L.append(f"| {p['user']} | {p['n']} | {p['best_rank']:,} | {_pct(p['top1_pct'])} | "
                     f"{_pct(p['top10_pct'])} | {_pct(p['cash_pct'])} | {_pct(p['max_exposure_pct'])} | "
                     f"{p['fighters_used']} | {_pct(p['own_med'])} |")

    u = report.get("user")
    if u:
        L += ["", f"**You:** {u['n']} entries, best rank {u['best_rank']:,}; top-1% rate {_pct(u['top1_pct'])}, "
              f"top-10% {_pct(u['top10_pct'])}, cash {_pct(u['cash_pct'])}; biggest exposure "
              f"{_pct(u['max_exposure_pct'])} ({u['n_over_50pct']} fighters over 50%), {u['fighters_used']} "
              f"fighters used, summed own {_pct(u['own_med'])}, lowest piece {_pct(u['min_own_med'])}, "
              f"{_num(u['sub10_mean'], 2)} punts per lineup, your lineups appeared {_num(u['field_copies_mean'])}x "
              f"each in the field, {_pct(u['within_unique_pct'])} distinct within your own set."]
        if u.get("exposures"):
            L.append("- Your top exposures: " + ", ".join(
                f"{e['name']} {_pct(e['pct'])}" for e in u["exposures"][:8]))
        v = u.get("vs_big_median") or {}
        if v:
            L.append("- You minus the big-stack median: " + ", ".join(
                f"{k.replace('_pct', '').replace('_', ' ')} {'+' if val >= 0 else ''}{val}"
                for k, val in v.items()))
    else:
        L += ["", "- None of your entries were found in this file (check the DK username)."]
    L += ["", "_Descriptive only: this reads how the field and the winners built. It is not a rule._"]
    return "\n".join(L)
