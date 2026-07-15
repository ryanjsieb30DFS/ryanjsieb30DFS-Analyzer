"""✅ Lineup grader — sport-calibrated pre-lock checks for HAND-BUILT lineups.

The user hand-builds in DK, pastes the lineups here, and gets an instant grade
BEFORE lock — leak-prevention at the moment where GPP EV is actually decided.
The tool still NEVER builds, selects, fixes, or swaps: it names weaknesses and
the user decides.

EVERY threshold is data-derived — never a hardcoded universal number (the retro
-audit proved universal thresholds false-positive on winning chalky MMA builds):

  - ownership target   ← the sport's observed shark envelope (shark_baseline)
                         and/or the WINNERS of your own logged contests
                         (field_tendencies winners_avg_own)
  - leverage flag      ← fires ONLY when the sport's sharks actually carry
                         sub-5% pieces (envelope leverage_pct >= _LEV_GATE);
                         in sports where the pros run pure chalk it stays
                         informational
  - fades / tiers      ← your own strategy contract + player-pool board
  - dupe risk          ← ownership product × declared field size, plus the
                         recurring crowded PAIRS from your logged contests

Per-lineup checks + portfolio checks (all-unique, competing-lineup overlap —
each bullet must answer a DIFFERENT what-if). Pure/deterministic; the optional
thesis check is a separate `claude -p` run wired in analysis_runner.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from src.autopsy import _norm_name

_REPO_ROOT = Path(__file__).parent.parent
_BASELINE_PATH = _REPO_ROOT / "rules" / "shared" / "shark_baseline.json"
_CONTRACT_DIR = _REPO_ROOT / "data" / "strategy_contract"
_DRAFT_DIR = _REPO_ROOT / "data" / "grade_drafts"

_LEV_GATE = 30.0     # shark leverage_pct below this → no-leverage stays info-only
_OWN_MARGIN = 1.2    # flag chalk-heavy only ABOVE target × margin (lenient on purpose)
_LOW_OWN = 10.0
_DART_OWN = 5.0
_SALARY_CAP = 50000  # DK classic cap, all five slates


# ------------------------------------------------------------------ parsing ----
def parse_lineups(text: str, pool) -> list[dict]:
    """One lineup per non-empty line; players split on comma/tab/semicolon/slash.
    Names are matched against the loaded projections pool (exact norm-name, then
    unique-substring like the strategy contract). Unmatched tokens are reported,
    never silently dropped."""
    if not text or pool is None or getattr(pool, "empty", True):
        return []
    universe: dict[str, dict] = {}
    for _, r in pool.iterrows():
        own_v = r.get("ownership")
        sal_v = r.get("salary")
        universe[_norm_name(str(r["name"]))] = {
            "name": str(r["name"]),
            "own": float(own_v) if own_v is not None and own_v == own_v else None,
            "salary": float(sal_v) if sal_v is not None and sal_v == sal_v else None,
        }
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        tokens = [t.strip() for t in re.split(r"[,\t;/·]+", line) if t.strip()]
        players, unmatched = [], []
        for t in tokens:
            key = _norm_name(t)
            hit = universe.get(key)
            if hit is None:
                subs = [v for k, v in universe.items() if key and key in k]
                hit = subs[0] if len(subs) == 1 else None
            (players if hit else unmatched).append(hit or t)
        if players or unmatched:
            out.append({"raw": line, "players": players, "unmatched": unmatched})
    return out


# -------------------------------------------------------------- calibration ----
def _baseline_key(slug: str, sport: str | None) -> str | None:
    # RD4 showdown has its own seed block; every other slug maps to its sport.
    return "showdown" if slug == "pga_rd4_sd" else sport


def calibration(slug: str, sport: str | None, contests: list[dict] | None) -> dict:
    """Everything the checks need, all read from the accumulated data."""
    cal: dict = {"slug": slug, "sport": sport}

    env = None
    try:
        sports = json.loads(_BASELINE_PATH.read_text()).get("sports") or {}
        env = (sports.get(_baseline_key(slug, sport)) or {}).get("shark_envelope")
    except Exception:  # noqa: BLE001
        pass
    cal["shark_own"] = env.get("own_per_slot") if env else None
    cal["shark_leverage_pct"] = env.get("leverage_pct") if env else None

    # Winners of YOUR logged contests — the most local calibration there is.
    winners_own = None
    try:
        from src import field_tendencies as ft
        vals = sorted(r["winners_avg_own"] for r in ft._load(slug)
                      if r.get("winners_avg_own") is not None)
        if vals:
            winners_own = round(vals[len(vals) // 2], 1)
    except Exception:  # noqa: BLE001
        pass
    cal["winners_own"] = winners_own

    targets = [t for t in (cal["shark_own"], winners_own) if t is not None]
    cal["own_flag_above"] = round(max(targets) * _OWN_MARGIN, 1) if targets else None

    # Strategy contract: the fades/under-owns YOUR strategy called.
    fades, soft = set(), set()
    try:
        c = json.loads((_CONTRACT_DIR / f"{slug}.json").read_text())
        for call in c.get("calls") or []:
            nk = _norm_name(call.get("name", ""))
            if call.get("verdict") == "fade":
                fades.add(nk)
            elif call.get("verdict") in ("lean_fade", "underweight", "pass", "pass_mix"):
                soft.add(nk)
    except Exception:  # noqa: BLE001
        pass
    cal["fades"], cal["soft_fades"] = fades, soft

    # The board's tiers (vocabulary-agnostic; last tier = the board's bottom).
    tiers, tier_order = {}, []
    try:
        from src import player_pool, pool_calibration
        saved = player_pool.load_pool(slug)
        if saved:
            for r in pool_calibration.parse_pool_tiers(saved["markdown"]):
                tiers[_norm_name(r["name"])] = r["tier"]
                if r["tier"] not in tier_order:
                    tier_order.append(r["tier"])
    except Exception:  # noqa: BLE001
        pass
    cal["tiers"], cal["bottom_tier"] = tiers, (tier_order[-1] if len(tier_order) >= 2 else None)

    # Recurring crowded players + PAIRS from your logged contests.
    crowded, pairs = set(), []
    try:
        from src import field_tendencies as ft
        seen_keys, seen_types = set(), set()
        for c in (contests or []):
            s = None
            key = ft.contest_key(c.get("name"))
            if key and key not in seen_keys:
                seen_keys.add(key)
                s = ft.summarize_contest(slug, c.get("name"))
            if s is None and c.get("type") and c["type"] not in seen_types:
                seen_types.add(c["type"])
                s = ft.summarize(slug, c.get("type"))
            if not s:
                continue
            for r in s.get("reliably_crowded") or []:
                crowded.add(_norm_name(r["name"]))
            for p in s.get("recurring_pairs") or []:
                pr = tuple(sorted(_norm_name(x) for x in p["players"]))
                if pr not in {tuple(sorted(q["norm"])) for q in pairs}:
                    pairs.append({"players": p["players"], "norm": list(pr),
                                  "in_n": p["in_n"], "of": p["of"]})
    except Exception:  # noqa: BLE001
        pass
    cal["crowded"], cal["pairs"] = crowded, pairs

    cal["field_size"] = max((c.get("field_size") or 0) for c in (contests or [])) \
        if contests else 0
    return cal


# ------------------------------------------------------------------ grading ----
def grade_lineup(lu: dict, cal: dict) -> dict:
    """All per-lineup checks. `flags` carry level 'warn' (calibrated violation)
    or 'info' (context the user should see)."""
    players = lu.get("players") or []
    owns = [p["own"] for p in players if p.get("own") is not None]
    sals = [p["salary"] for p in players if p.get("salary") is not None]
    norms = {_norm_name(p["name"]) for p in players}
    g: dict = {
        "raw": lu.get("raw"),
        "names": [p["name"] for p in players],
        "unmatched": lu.get("unmatched") or [],
        "n": len(players),
        "avg_own": round(sum(owns) / len(owns), 1) if owns else None,
        "n_sub10": sum(1 for o in owns if o < _LOW_OWN),
        "n_sub5": sum(1 for o in owns if o < _DART_OWN),
        "salary_used": int(sum(sals)) if sals else None,
        "flags": [],
    }

    # Dupe risk: expected duplicate lineups in the declared field.
    if owns and cal.get("field_size"):
        prod = 1.0
        for o in owns:
            prod *= max(o, 0.1) / 100.0
        g["expected_dupes"] = round(prod * cal["field_size"], 2)

    # 0) Salary sanity: DK wouldn't accept an over-cap lineup, so exceeding the
    # cap here almost always means a token matched the WRONG player.
    if g["salary_used"] is not None and g["salary_used"] > _SALARY_CAP:
        g["flags"].append({"level": "warn",
                           "msg": f"Salary ${g['salary_used']:,} exceeds the "
                                  f"${_SALARY_CAP:,} cap — DK wouldn't accept this; "
                                  f"check for a name matched to the wrong player"})

    # 1) Fade violations — your OWN strategy said zero exposure.
    fade_hits = [p["name"] for p in players if _norm_name(p["name"]) in cal.get("fades", set())]
    if fade_hits:
        g["flags"].append({"level": "warn",
                           "msg": f"Rosters your own FADE call(s): **{', '.join(fade_hits)}**"})
    soft_hits = [p["name"] for p in players if _norm_name(p["name"]) in cal.get("soft_fades", set())]
    if soft_hits:
        g["flags"].append({"level": "info",
                           "msg": f"Carries under-own call(s): {', '.join(soft_hits)} "
                                  f"(strategy said light, not zero)"})

    # 2) Board bottom-tier players.
    if cal.get("tiers") and cal.get("bottom_tier"):
        bottom = [p["name"] for p in players
                  if cal["tiers"].get(_norm_name(p["name"])) == cal["bottom_tier"]]
        if bottom:
            g["flags"].append({"level": "warn",
                               "msg": f"Board tiers **{', '.join(bottom)}** as "
                                      f"`{cal['bottom_tier']}` (its bottom tier)"})

    # 3) Ownership vs the calibrated target (shark envelope / your winners).
    if g["avg_own"] is not None and cal.get("own_flag_above") is not None:
        if g["avg_own"] > cal["own_flag_above"]:
            tgt = " / ".join(f"{v}" for v in (cal.get("shark_own"), cal.get("winners_own"))
                             if v is not None)
            g["flags"].append({"level": "warn",
                               "msg": f"Chalk-heavy: **{g['avg_own']}% avg own** vs your "
                                      f"contests' winning envelope ({tgt}%/slot)"})

    # 4) Leverage — flag ONLY where the sport's sharks actually carry it.
    lev = cal.get("shark_leverage_pct")
    if g["n_sub10"] == 0 and owns:
        if lev is not None and lev >= _LEV_GATE:
            g["flags"].append({"level": "warn",
                               "msg": f"No sub-10% piece — the {cal.get('sport')} sharks carry "
                                      f"leverage in {lev:.0f}% of lineups"})
        else:
            g["flags"].append({"level": "info",
                               "msg": "No sub-10% piece (info: this sport's observed pros run "
                                      "chalk-heavy, so not auto-flagged)"})

    # 5) Recurring crowded pairs — the dupe-magnet stacks of YOUR contests.
    for pr in cal.get("pairs") or []:
        if set(pr["norm"]) <= norms:
            g["flags"].append({"level": "warn",
                               "msg": f"Contains the field's recurring pair "
                                      f"**{pr['players'][0]} + {pr['players'][1]}** "
                                      f"(together in {pr['in_n']} of {pr['of']} of your logs "
                                      f"— a dupe magnet)"})
    crowded_hits = [p["name"] for p in players if _norm_name(p["name"]) in cal.get("crowded", set())]
    if crowded_hits:
        g["flags"].append({"level": "info",
                           "msg": f"Reliably-crowded players aboard: {', '.join(crowded_hits)}"})

    if g.get("unmatched"):
        g["flags"].append({"level": "info",
                           "msg": f"Not matched to projections (typo?): "
                                  f"{', '.join(str(u) for u in g['unmatched'])}"})
    return g


def grade_portfolio(grades: list[dict]) -> list[dict]:
    """Cross-lineup checks: duplicates + competing lineups (a portfolio's bullets
    must answer DIFFERENT what-ifs, not the same one twice)."""
    flags = []
    rosters = [frozenset(_norm_name(n) for n in g["names"]) for g in grades]
    for i in range(len(rosters)):
        for j in range(i + 1, len(rosters)):
            if not rosters[i] or not rosters[j]:
                continue
            if rosters[i] == rosters[j]:
                flags.append({"level": "warn",
                              "msg": f"Lineups {i + 1} and {j + 1} are IDENTICAL — "
                                     f"small-field bullets must be all-unique"})
            else:
                overlap = len(rosters[i] & rosters[j])
                size = min(len(rosters[i]), len(rosters[j]))
                if size >= 3 and overlap >= size - 1:
                    flags.append({"level": "warn",
                                  "msg": f"Lineups {i + 1} and {j + 1} differ by ONE player "
                                         f"— competing lineups answering the same what-if"})
    return flags


def grade_md(grades: list[dict], portfolio_flags: list[dict], cal: dict) -> str:
    """Render the whole grade as markdown for the tab."""
    out = []
    tgt_bits = []
    if cal.get("shark_own") is not None:
        tgt_bits.append(f"sharks {cal['shark_own']}%/slot")
    if cal.get("winners_own") is not None:
        tgt_bits.append(f"your contests' winners {cal['winners_own']}%/slot")
    if cal.get("shark_leverage_pct") is not None:
        tgt_bits.append(f"shark leverage rate {cal['shark_leverage_pct']:.0f}%")
    if tgt_bits:
        out.append(f"_Calibration ({cal.get('sport')}): " + " · ".join(tgt_bits) + "_")
    for i, g in enumerate(grades, 1):
        warns = [f for f in g["flags"] if f["level"] == "warn"]
        infos = [f for f in g["flags"] if f["level"] == "info"]
        head = "🟢" if not warns else ("🟡" if len(warns) == 1 else "🔴")
        stats = []
        if g["avg_own"] is not None:
            stats.append(f"{g['avg_own']}% avg own")
        stats.append(f"{g['n_sub10']} sub-10% / {g['n_sub5']} sub-5%")
        if g.get("salary_used") is not None:
            stats.append(f"${g['salary_used']:,} of ${_SALARY_CAP:,}")
        if g.get("expected_dupes") is not None:
            stats.append(f"~{g['expected_dupes']} expected dupes")
        out.append(f"**{head} Lineup {i}** — {', '.join(g['names'])}  \n"
                   f"_{' · '.join(stats)}_")
        for f in warns:
            out.append(f"- ⚠️ {f['msg']}")
        for f in infos:
            out.append(f"- ℹ️ {f['msg']}")
    for f in portfolio_flags:
        out.append(f"- {'⚠️' if f['level'] == 'warn' else 'ℹ️'} **Portfolio:** {f['msg']}")
    return "\n\n".join(out) if out else "_Nothing to grade yet._"


# --------------------------------------------------- grader self-validation ----
def retro_grade(records, cal: dict) -> dict:
    """Auto-grade the ENTERED lineups at autopsy time — the grader grading
    itself. Uses the same calibrated gates as the pre-lock grade, but against
    the ACTUAL ownership already computed into each lineup record (avg_own /
    low_own_count), and logs flags-vs-finish so results.jsonl accumulates the
    evidence: do flagged lineups really underperform clean ones? After enough
    slates the thresholds get validated (or corrected) by outcomes instead of
    margins. Never blocks the log."""
    lineups, seen = [], set()
    for r in (records or []):
        for ln in r.get("user_lineups") or []:
            roster = frozenset(_norm_name(p) for p in (ln.get("players") or []) if p)
            if roster and roster not in seen:
                seen.add(roster)
                lineups.append(ln)
    if not lineups:
        return {"gradable": False}

    lev_gated = (cal.get("shark_leverage_pct") is not None
                 and cal["shark_leverage_pct"] >= _LEV_GATE)
    pair_norms = [set(p["norm"]) for p in (cal.get("pairs") or [])]
    graded = []
    for ln in lineups:
        roster = {_norm_name(p) for p in (ln.get("players") or [])}
        flags = []
        avg_own = ln.get("avg_own")
        if (avg_own is not None and cal.get("own_flag_above") is not None
                and avg_own > cal["own_flag_above"]):
            flags.append("chalk_heavy")
        if lev_gated and (ln.get("low_own_count") or 0) == 0:
            flags.append("no_leverage")
        if roster & cal.get("fades", set()):
            flags.append("fade_violation")
        if any(pn <= roster for pn in pair_norms):
            flags.append("crowded_pair")
        graded.append({"players": sorted(ln.get("players") or []),
                       "percentile": ln.get("percentile"),
                       "flags": flags})
    flagged = [g["percentile"] for g in graded if g["flags"] and g["percentile"] is not None]
    clean = [g["percentile"] for g in graded if not g["flags"] and g["percentile"] is not None]
    return {
        "gradable": True,
        "n_lineups": len(graded),
        "lineups": graded,
        "flagged_pctiles": [round(p, 1) for p in flagged],
        "clean_pctiles": [round(p, 1) for p in clean],
    }


# ------------------------------------------------------------- draft persist ---
def load_draft(slug: str) -> str:
    p = _DRAFT_DIR / f"{slug}.txt"
    try:
        return p.read_text() if p.exists() else ""
    except OSError:
        return ""


def save_draft(slug: str, text: str) -> None:
    p = _DRAFT_DIR / f"{slug}.txt"
    try:
        if load_draft(slug) == text:
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    except OSError:
        pass


def clear_draft(slug: str) -> None:
    try:
        (_DRAFT_DIR / f"{slug}.txt").unlink(missing_ok=True)
    except OSError:
        pass
