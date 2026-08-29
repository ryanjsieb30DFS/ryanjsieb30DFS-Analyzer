"""✅ Lineup grader — sport-calibrated pre-lock checks for HAND-BUILT lineups.

The user hand-builds in DK, pastes the lineups here, and gets an instant grade
BEFORE lock — leak-prevention at the moment where GPP EV is actually decided.
The tool still NEVER builds, fixes, or swaps: it names weaknesses and
the user decides. (The Grade tab's separate Entry-options section — see
src/lineup_selection.py — displays candidate sets selected from the Sim's
pool; this module itself still only grades.)

WHAT MAY COST A LETTER (user directive, 8/28-29/26): only a call THIS slate's
strategy actually made, plus the DK salary cap. A statistic — an ownership
screen, a cross-sport shark average, a count of player names from past
standings — is reported as INFO and never lowers a grade. Every slate is
different; the grade measures whether a lineup follows the slate's own
strategy, not whether it matches a population average.

  Letter-costing:
  - fade violation     ← your strategy contract said zero on that player.
                         Hard F. This is the model the others follow
  - salary over cap    ← a DK rule (in practice, a wrong-name match). Hard F
  - board bottom tier  ← your player-pool board tagged them `Fade` this slate.
                         Matched by NAME, never positionally (see calibration)

  Info only, never a letter:
  - leverage           ← 8/28/26. "Carry a sub-10% player" is a cross-sport
                         shark RATE the pros are under most of the time, not
                         a call this strategy made
  - ownership vs the   ← 8/29/26. A shark envelope + the median of past
    observed envelope     winners. Ownership is an OUTCOME of picking players,
                         not an input; chalk is often simply right
  - recurring pairs    ← 8/29/26. A cross-slate count of player NAMES, which
                         the trap rule (a trap is a price, not a player)
                         already rules out as evidence. It also warned once
                         per pair uncapped, so four made an automatic F
  - dupe risk          ← ownership product × declared field size

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

_OWN_MARGIN = 1.2    # chalk-heavy INFO note fires only above target × margin
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
            if hit is None and len(key) >= 4:
                # Substring fallback only on fragments long enough to be a
                # real surname — a 2-3 letter scrap resolving to one random
                # player silently grades the wrong lineup.
                subs = [v for k, v in universe.items() if key in k]
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
    # Focus-gated like every other small-field benchmark: legacy rows from
    # 20-Max/MME standings (contest_type "unknown") used to leak a 23k-entry
    # contest's winner ownership into the SE/3-Max chalk gate.
    winners_own = None
    try:
        from src import field_tendencies as ft
        from src.contests import FOCUS_CONTEST_TYPES
        # Comparable fields only (8/9/26): a 1,470-entry contest's winner
        # ownership must not calibrate a sub-600 SE gate. Target = the biggest
        # declared focus contest; ft._size_ok applies the 0.5x-2x band.
        _target_fs = max((int(c.get("field_size") or 0) for c in (contests or [])
                          if c.get("type") in FOCUS_CONTEST_TYPES), default=0)
        vals = sorted(r["winners_avg_own"] for r in ft._load(slug)
                      if r.get("winners_avg_own") is not None
                      and r.get("contest_type") in FOCUS_CONTEST_TYPES
                      and ft._size_ok(r.get("field_size"), _target_fs))
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
    # The bottom tier is the board's explicit FADE tier, matched by name — not
    # whichever tier happened to appear last (fixed 8/29/26). Positional
    # detection was a live bug: the board's vocabulary is Core / Good / Okay /
    # Fade, so on any slate whose board tagged nobody Fade, `Okay` became the
    # "bottom tier" and every Okay-tier player silently cost a letter grade.
    # No Fade rows => no bottom-tier check, which is the honest answer.
    _fade_tiers = [t for t in tier_order if "fade" in str(t).strip().lower()]
    cal["tiers"], cal["bottom_tier"] = tiers, (_fade_tiers[-1] if _fade_tiers else None)

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
                s = ft.summarize_contest(slug, c.get("name"),
                                         target_field_size=c.get("field_size"))
            if s is None and c.get("type") and c["type"] not in seen_types:
                seen_types.add(c["type"])
                s = ft.summarize(slug, c.get("type"),
                                 target_field_size=c.get("field_size"))
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


def contest_calibration(slug: str, sport: str | None, contest: dict) -> dict:
    """Calibration for ONE contest — not every contest is the same (user
    directive 8/9/26): field size, winners-own gate, dupe field, and
    crowded/pairs history all come from THIS contest (a single-contest list
    already makes `calibration` do that), plus its payout shape and entry
    count for the letter grade."""
    cal = calibration(slug, sport, [contest])
    cal.update(
        contest_name=contest.get("name"),
        contest_id=contest.get("id"),
        payout_shape=contest.get("payout_shape"),
        my_entries=contest.get("my_entries"),
    )
    return cal


def sim_standing(pool: dict, contest: dict, roster_key: str) -> dict | None:
    """Where this EXACT roster ranks inside the Sim's pool FOR THIS CONTEST.
    None when the roster isn't a pool row (hand-edited lineups get no sim
    adjustment). Percentile = share of pool lineups strictly below it."""
    rosters = pool.get("rosters") or []
    idx = None
    for i, r in enumerate(rosters):
        if "|".join(sorted(str(n) for n in r)) == roster_key:
            idx = i
            break
    if idx is None:
        return None
    m = contest.get("metrics") or {}

    def _pct(arr):
        if not arr or idx >= len(arr) or arr[idx] is None:
            return None
        vals = [v for v in arr if v is not None]
        if len(vals) <= 1:
            return 100.0
        below = sum(1 for v in vals if v < arr[idx])
        return round(100.0 * below / (len(vals) - 1), 1)

    return {"index": idx,
            "pct_top1": _pct(m.get("top1_pct")),
            "pct_cash": _pct(m.get("cash_pct"))}


_LETTERS = ["F", "D", "C", "B", "A"]


def letter_grade(grade: dict, cal: dict, sim: dict | None = None) -> dict:
    """A/B/C/D/F for one lineup in ONE contest. Deterministic and explainable:

    - Hard F (final): a FADE violation (your own strategy said zero), a
      salary over the cap (almost always a wrong-player match), or 4+
      calibrated warnings.
    - Otherwise the warning count sets the base: 0→A, 1→B, 2→C, 3→D.
    - When the pasted roster IS a Sim pool row, its sim standing in THIS
      contest adjusts ONE step: the metric follows the payout shape
      (top-heavy → chance of 1st, flat/balanced → chance of any payout,
      undeclared → the average of both); ≥90th percentile bumps up,
      <25th bumps down. Exactly one step, never past A, D drops to F.

    Returns {letter, base, why: [plain-language lines], sim_pct, sim_metric}."""
    flags = grade.get("flags") or []
    warns = [f for f in flags if f.get("level") == "warn"]
    codes = {f.get("code") for f in warns}
    why: list[str] = []

    hard_f = ("fade" in codes or "salary_cap" in codes or len(warns) >= 4)
    if hard_f:
        base = "F"
        if "fade" in codes:
            why.append("F is final: it rosters a player your own strategy "
                       "said to zero (a fade violation).")
        elif "salary_cap" in codes:
            why.append("F is final: the salary is over the cap — almost "
                       "certainly a name matched to the wrong player.")
        else:
            why.append(f"F is final: {len(warns)} calibrated warnings.")
    else:
        base = {0: "A", 1: "B", 2: "C", 3: "D"}[len(warns)]
        if warns:
            why.append(f"{len(warns)} warning{'s' if len(warns) != 1 else ''} "
                       f"from the calibrated checks → starts at {base}.")
        else:
            why.append("No calibrated warnings → starts at A.")
    for f in warns:
        why.append(f.get("msg", ""))

    letter = base
    sim_pct = sim_metric = None
    if not hard_f and sim is not None:
        shape = cal.get("payout_shape")
        if shape == "Top-heavy":
            sim_pct, sim_metric = sim.get("pct_top1"), "chance of finishing 1st (top1%)"
        elif shape in ("Flat", "Balanced"):
            sim_pct, sim_metric = sim.get("pct_cash"), "chance of any payout (cash%)"
        else:
            pts = [v for v in (sim.get("pct_top1"), sim.get("pct_cash"))
                   if v is not None]
            sim_pct = round(sum(pts) / len(pts), 1) if pts else None
            sim_metric = "blend of first-place and any-payout chances"
        if sim_pct is not None:
            pos = _LETTERS.index(letter)
            if sim_pct >= 90.0 and letter != "A":
                letter = _LETTERS[pos + 1]
                why.append(f"Its {sim_metric} beats {sim_pct:.0f} of every 100 "
                           f"lineups the Sim built for this contest → one step "
                           f"up to {letter}.")
            elif sim_pct < 25.0:
                letter = _LETTERS[pos - 1]
                why.append(f"Its {sim_metric} beats only {sim_pct:.0f} of every "
                           f"100 lineups the Sim built for this contest → one "
                           f"step down to {letter}.")
    elif not hard_f and sim is None:
        why.append("This exact lineup is not in the Sim's pool, so no sim "
                   "adjustment was applied.")

    return {"letter": letter, "base": base, "why": [w for w in why if w],
            "sim_pct": sim_pct, "sim_metric": sim_metric}


def worst_letter(letters: list[str]) -> str | None:
    """The section's headline: the WORST lineup letter (conservative)."""
    ranked = [l for l in letters if l in _LETTERS]
    return min(ranked, key=_LETTERS.index) if ranked else None


def contest_grade_md(grades: list[dict], letters: list[dict],
                     portfolio_flags: list[dict], cal: dict) -> str:
    """Per-contest grade markdown: each lineup headed by its LETTER, the
    calibration line naming the contest."""
    out = []
    bits = []
    if cal.get("field_size"):
        bits.append(f"field {int(cal['field_size']):,}")
    if cal.get("payout_shape"):
        bits.append(f"payout {cal['payout_shape']}")
    if cal.get("winners_own") is not None:
        bits.append(f"your comparable winners ~{cal['winners_own']}%/slot")
    if cal.get("shark_own") is not None:
        bits.append(f"sharks {cal['shark_own']}%/slot")
    if bits:
        out.append(f"_Calibration for **{cal.get('contest_name') or 'this contest'}** — "
                   + " · ".join(bits) + "_")
    for i, (g, lt) in enumerate(zip(grades, letters), 1):
        warns = [f for f in g["flags"] if f["level"] == "warn"]
        infos = [f for f in g["flags"] if f["level"] == "info"]
        stats = []
        if g["avg_own"] is not None:
            stats.append(f"{g['avg_own']}% avg own")
        stats.append(f"{g['n_sub10']} sub-10% / {g['n_sub5']} sub-5%")
        if g.get("salary_used") is not None:
            stats.append(f"${g['salary_used']:,} of ${_SALARY_CAP:,}")
        if g.get("expected_dupes") is not None:
            _how = ("corpus-corrected" if g.get("dupes_corrected")
                    else "raw independence estimate")
            stats.append(f"~{g['expected_dupes']} expected dupes ({_how})")
        out.append(f"**Grade {lt['letter']} — Lineup {i}** — {', '.join(g['names'])}  \n"
                   f"_{' · '.join(stats)}_")
        for w in lt.get("why") or []:
            out.append(f"- {w}")
        for f in infos:
            out.append(f"- ℹ️ {f['msg']}")
    for f in portfolio_flags:
        out.append(f"- {'⚠️' if f['level'] == 'warn' else 'ℹ️'} **Within this contest:** {f['msg']}")
    return "\n\n".join(out) if out else "_Nothing to grade yet._"


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

    # Dupe risk: expected duplicate lineups in the declared field. The naive
    # per-player independence product UNDER-predicts real duplication, because
    # entrants converge on the same chalk rosters instead of drawing players
    # independently — measured 1.7-6.6× for MMA/NASCAR over the Sim's corpus.
    # `dupe_correction` scales it where the corpus evidence is tight, and
    # returns None (keep the naive number) for golf, whose ratio spans three
    # orders of magnitude. `dupes_corrected` drives the label in grade_md — a
    # corrected number and a naive one must never look alike on a pre-lock
    # screen.
    if owns and cal.get("field_size"):
        prod = 1.0
        for o in owns:
            prod *= max(o, 0.1) / 100.0
        naive = prod * cal["field_size"]
        try:
            from src.sim_link import dupe_correction
            factor = dupe_correction(cal.get("slug") or "", cal["field_size"])
        except Exception:  # noqa: BLE001
            factor = None
        g["expected_dupes"] = round(naive * factor if factor else naive, 2)
        g["dupes_corrected"] = bool(factor)
        g["dupes_factor"] = factor

    # 0) Salary sanity: DK wouldn't accept an over-cap lineup, so exceeding the
    # cap here almost always means a token matched the WRONG player.
    if g["salary_used"] is not None and g["salary_used"] > _SALARY_CAP:
        g["flags"].append({"level": "warn", "code": "salary_cap",
                           "msg": f"Salary ${g['salary_used']:,} exceeds the "
                                  f"${_SALARY_CAP:,} cap — DK wouldn't accept this; "
                                  f"check for a name matched to the wrong player"})

    # 1) Fade violations — your OWN strategy said zero exposure.
    fade_hits = [p["name"] for p in players if _norm_name(p["name"]) in cal.get("fades", set())]
    if fade_hits:
        g["flags"].append({"level": "warn", "code": "fade",
                           "msg": f"Rosters your own FADE call(s): **{', '.join(fade_hits)}**"})
    soft_hits = [p["name"] for p in players if _norm_name(p["name"]) in cal.get("soft_fades", set())]
    if soft_hits:
        g["flags"].append({"level": "info", "code": "soft_fade",
                           "msg": f"Carries under-own call(s): {', '.join(soft_hits)} "
                                  f"(strategy said light, not zero)"})

    # 2) Board bottom-tier players.
    if cal.get("tiers") and cal.get("bottom_tier"):
        bottom = [p["name"] for p in players
                  if cal["tiers"].get(_norm_name(p["name"])) == cal["bottom_tier"]]
        if bottom:
            g["flags"].append({"level": "warn", "code": "bottom_tier",
                               "msg": f"Your own player-pool board for THIS slate tiers "
                                      f"**{', '.join(bottom)}** as `{cal['bottom_tier']}` — "
                                      f"the tier you said to avoid"})

    # 3) Ownership vs the observed envelope — INFO ONLY (8/29/26, user
    # directive). This compares a lineup to a cross-sport shark average and the
    # median of past winners: both are statistics, not calls THIS slate's
    # strategy made, so neither may cost a letter. Ownership is an OUTCOME of
    # which players you picked, never an input to build toward (the same
    # reasoning applied to the framework files the same day). A slate where the
    # chalk is simply correct must be gradeable as an A.
    if g["avg_own"] is not None and cal.get("own_flag_above") is not None:
        if g["avg_own"] > cal["own_flag_above"]:
            tgt = " / ".join(f"{v}" for v in (cal.get("shark_own"), cal.get("winners_own"))
                             if v is not None)
            g["flags"].append({"level": "info", "code": "chalk_heavy",
                               "msg": f"Runs chalkier than usual: **{g['avg_own']}% avg own** "
                                      f"vs the {tgt}%/slot your past winners and the tracked "
                                      f"pros averaged. Worth a look — more of the field will "
                                      f"hold these players — but this does not lower the "
                                      f"grade, and chalk is often simply right."})

    # 4) Leverage — INFO ONLY, always. Never costs a letter (8/28/26, user
    # directive: the grade must measure THIS slate's strategy, and "carry a
    # sub-10% player" is not a strategy call — it is a cross-sport shark
    # average. Docking a letter for it turned a RATE (the pros carry one in
    # ~15-47% of lineups, sport-depending) into a per-lineup requirement,
    # the same rate-not-quota bug the pick gate had. A lineup with no
    # low-owned piece is a normal lineup; contest winners regularly are one.
    lev = cal.get("shark_leverage_pct")
    if g["n_sub10"] == 0 and owns:
        rate = (f"the {cal.get('sport')} sharks carry one in about "
                f"{lev:.0f}% of their lineups — so most of the time they "
                "don't either") if lev is not None else \
               "this sport's observed pros run chalk-heavy"
        g["flags"].append({"level": "info", "code": "no_leverage",
                           "msg": f"No sub-10%-owned player (just so you know: "
                                  f"{rate}). This does not lower the grade."})

    # 5) Recurring crowded pairs — INFO ONLY (8/29/26, user directive). This is
    # a cross-slate count of PLAYER NAMES from past standings, which the trap
    # rule (8/9/26) already says is never evidence: a trap is a price, not a
    # player, and those prices reset every slate. It also warned once PER
    # matched pair with no cap, so four historical pairs produced an automatic
    # F with zero input from the current strategy. Kept as a read — knowing
    # where your opponents reliably go is useful — but it costs no letter.
    for pr in cal.get("pairs") or []:
        if set(pr["norm"]) <= norms:
            g["flags"].append({"level": "info", "code": "crowded_pair",
                               "msg": f"Your past fields liked pairing "
                                      f"**{pr['players'][0]} + {pr['players'][1]}** "
                                      f"({pr['in_n']} of {pr['of']} logged contests). That is "
                                      f"opponent behaviour from other slates, not a verdict on "
                                      f"these two today — expect company if both play well."})
    crowded_hits = [p["name"] for p in players if _norm_name(p["name"]) in cal.get("crowded", set())]
    if crowded_hits:
        g["flags"].append({"level": "info", "code": "crowded_info",
                           "msg": f"Reliably-crowded players aboard: {', '.join(crowded_hits)}"})

    if g.get("unmatched"):
        g["flags"].append({"level": "info", "code": "unmatched",
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
            # Say WHICH number this is. A corrected estimate (scaled by the
            # Sim's measured concentration corpus) and a raw independence
            # estimate can differ several-fold, and the user is about to lock
            # lineups on it.
            if g.get("dupes_corrected"):
                _f = g.get("dupes_factor")
                _how = (f"corpus-corrected, {_f}× the independence estimate"
                        if _f else "corpus-corrected")
            else:
                _how = "raw independence estimate, no corpus correction"
            stats.append(f"~{g['expected_dupes']} expected dupes ({_how})")
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

    # no_leverage is NOT graded here (8/28/26) — it is info-only in the live
    # grader, and the self-validation has to measure the same thing the
    # grader actually costs a lineup for. chalk_heavy and crowded_pair joined
    # no_leverage as info-only on 8/29/26, so they are not graded here either —
    # otherwise this loop would report "flagged lineups finish worse" about
    # flags that cost nothing, and the process trend would keep arguing for
    # rules the grader no longer applies.
    graded = []
    for ln in lineups:
        roster = {_norm_name(p) for p in (ln.get("players") or [])}
        flags = []
        if roster & cal.get("fades", set()):
            flags.append("fade_violation")
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


def clear_drafts(slug: str) -> None:
    """Slate-scoped: the legacy single draft plus every per-contest draft
    (`<slug>__<contest key>.txt`)."""
    clear_draft(slug)
    if _DRAFT_DIR.exists():
        for p in _DRAFT_DIR.glob(f"{slug}__*.txt"):
            try:
                p.unlink()
            except OSError:
                pass


def leverage_md(lineups: list[dict]) -> str | None:
    """The sharp's final pre-lock review, per player: how much of YOUR entry
    set holds him vs how much of the field will (projected ownership), and the
    gap (leverage). Display-only — grades nothing, builds nothing. Plain
    language per the 7/27/26 output directive."""
    if not lineups:
        return None
    n = len(lineups)
    counts: dict[str, dict] = {}
    for lu in lineups:
        for p in lu.get("players") or []:
            e = counts.setdefault(p["name"], {"n": 0, "own": p.get("own")})
            e["n"] += 1
    if not counts:
        return None
    out = ["### Your exposure vs the field (the leverage read)",
           "This table shows, for each player you used: the share of your entries "
           "that hold him (yours), the share of the field expected to hold him "
           "(the projected ownership), and the gap between the two (the leverage). "
           "A positive gap means you beat the field when he hits. A big negative "
           "gap means the field gains on you when he hits.",
           "",
           "| Player | Yours | Field | Gap |", "|---|---|---|---|"]
    rows = sorted(counts.items(), key=lambda kv: -kv[1]["n"])
    for name, e in rows:
        mine = e["n"] / n * 100
        own = e.get("own")
        if own is not None and own == own:
            out.append(f"| {name} | {mine:.0f}% | {own:.1f}% | {mine - own:+.1f}% |")
        else:
            out.append(f"| {name} | {mine:.0f}% | — | — |")
    return "\n".join(out)
