"""🎯 Per-contest entry picking over the Sim's pushed pool.

**Selection is not construction (8/9/26).** This module never authors, edits,
swaps, or fixes a roster. Every lineup it handles was BUILT AND SIMMED by the
Sim tool and arrived via `data/sim_pool/<slug>.json`.

Per-contest flow (8/9/26 evening rework — the user's contests are all small
single-entry GPPs but NOT interchangeable: different field sizes, payout
shapes, and histories, so every contest gets its own pick and its own grade):

1. `candidate_slice` deterministically cuts THAT contest's top ~500 pool rows
   in two stages (8/29/26): a blend-ranked prefilter over the whole pool, then
   a coverage-greedy fill so the table holds different IDEAS rather than 500
   variations of one. The blend is weighted by measured predictive power —
   projection and cash% lead, ownership is a real positive term, win% is out
   (see `blend_scores`). `lineup_families` groups the result into a dozen
   theses so the table is readable at that size.
2. `slice_digest_md` renders the slice as one id-keyed markdown table; the
   `run_contest_selection` claude pass reads it (plus the strategy, board,
   and open lessons) and PICKS exactly `my_entries` rows BY ID.
3. `parse_pick` validates the pick hard: every id must be a slice row, the
   listed players must match that row exactly, the count must equal
   `my_entries`. Any violation → errors, nothing saved. A selection can
   choose; it can never invent. Breaking a STRATEGY rule is no longer a
   violation — it is an OVERRIDE, legal when the why names it, and written to
   `rules/<slug>/strategy_overrides.jsonl` so the autopsy can eventually score
   overridden picks against clean ones (`log_override` / `override_report`).
4. `save_contest_pick` persists picks per contest (schema v2) so the Grade
   tab can one-click them into that contest's grade box.

**One lineup, one contest (user directive 8/15/26).** Across every contest on
a slate (all sports), a pool lineup may be picked ONCE. `taken_roster_keys`
reads the picks already saved for the slate's OTHER contests; `candidate_slice`
drops those rosters from the slice so the claude pass never sees them, and
`parse_pick` rejects one that slips through by roster identity — so the same
six players can't be re-picked at a different pool index. DK allows the reuse;
the user does not want it.

**Two opinions per contest (8/22/26).** The Sim also pushes its DIVERSIFIED
portfolio (`data/sim_entries/<slug>.json`), and the Grade tab shows it beside
this module's pick for the same contest, with `compare_sets` counting how many
lineups the two chose in common. The pick above stays deliberately BLIND to
that file — it is never read into the slice, the prompt, or the validation.
That blindness is the whole point: two processes that never saw each other's
answer landing on the same six players is evidence; an informed pick agreeing
with what it was shown is just anchoring. Overlap is a fine outcome, never an
error, and the Sim's entries are never gated away — a diversifier entry that
breaks the slate strategy is FLAGGED in the panel and still gradeable, because
the override is the user's to make.

Crowd/trap discipline still applies: a trap is a price, not a player, and
nothing here carries player-name quality signals across slates.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

_SELECTION_DIR = Path(__file__).parent.parent / "data" / "lineup_selection"

# Sim contest_type -> Analyzer declared type vocabulary.
_TYPE_MAP = {"se": "SE", "3max": "3-Max", "5max": "5-Max",
             "20max": "20-Max", "mme": "150-Max", "150max": "150-Max"}
_SMALL_FIELD_TYPES = {"se", "3max", "5max"}

# Fields under this many entries play like SE — a validated finding
# (docs/mme_plan.md: "Under ~2,500 entries plays like SE").
_PLAYS_LIKE_SE_FIELD = 2_500

_SLICE_CAP = 500  # user directive 8/29/26: 50 -> 100 (8/15) -> 500, all sports
# Measured on 27 archived pools / 25 contests with a known winning score: a
# lineup that would have WON the contest reached the old ~100-row slice in
# 2 of 25 (8%). At ~500 coverage-selected rows it reaches 8 of 25 (32%); the
# full pool holds one in 18 of 25 (72%). Size is the dominant term — the same
# 72 rows chosen for coverage instead of sim rank scored WORSE (1 of 25), so
# diversity only pays once there is room for it.
_SLICE_PREFILTER = 2_000   # stage 1: quality cut over the WHOLE pool


_CONTRACT_DIR = Path(__file__).parent.parent / "data" / "strategy_contract"


def strategy_slice_names(slug: str) -> dict:
    """Names the strategy-aware slice angle seats: the contract's leverage
    candidates + its UNDERWEIGHT calls (underweight means never zero — the
    slice must always offer a lineup carrying each such player). Empty dict
    when no contract exists; the slice then runs on the numbers angles only."""
    p = _CONTRACT_DIR / f"{slug}.json"
    try:
        d = json.loads(p.read_text())
    except Exception:  # noqa: BLE001 — missing/bad contract → no angle
        return {}
    lev = [str(c.get("name")) for c in d.get("leverage_candidates") or []
           if c.get("name")]
    uw = [str(c.get("name")) for c in d.get("calls") or []
          if c.get("verdict") == "underweight" and c.get("name")]
    return {"leverage": lev, "underweight": uw} if (lev or uw) else {}


def strategy_gate(slug: str) -> dict:
    """The slate strategy's rules, as an ENFORCEABLE gate (user directive
    8/15/26: "the lineups that are picked HAVE TO FOLLOW THE SLATE STRATEGY").

    Everything here is read from `data/strategy_contract/<slug>.json`, which the
    strategy generation writes — nothing is hardcoded per sport. The rules:

    * `fade` / `lean_fade` calls  — the strategy said play him nowhere / mostly
      avoid. A lineup carrying one is out. This rule NEVER relaxes.
    * `underweight` calls — "less than the crowd, never zero". A SOFT rule
      (8/28/26): carriers stay pickable, flagged ⚠ as a cost and priced in
      `gate_summary`; the only hard stop is the same underweight player in
      EVERY entry of a multi-entry contest (`parse_pick`). The old hard
      exclusion collapsed the verdict to zero and deleted the 8/23 Clinch
      winner from the pool.
    * `leverage_candidates` — NOT A RULE AT ALL (8/28/26, user directive:
      "the point of the grade tab is to ensure lineups are following the
      CURRENT SLATE STRATEGY"). This list is not a strategy decision — it is
      a mechanical screen (`landscape.leverage_candidates`, ownership < 10%).
      The strategy must ADDRESS each candidate in prose; addressing one is
      not playing one. So carrying none costs a lineup NOTHING here: no
      exclusion, no flag, no warning. The names still ride the `strategy`
      column as INFORMATION (this lineup carries a play the strategy
      surfaced) and still earn slice seats, so leverage builds stay
      available to pick — they are never required.
    * `Core` tier from the board — at least two, the strategy's own anchors.
    * `chalk_pairs[0]` — the top duplicated pair, "what a sharp refuses".

    Returns `{"has_contract": bool, ...}`; an empty gate (no contract) filters
    nothing, and the caller decides whether to run at all."""
    p = _CONTRACT_DIR / f"{slug}.json"
    try:
        d = json.loads(p.read_text())
    except Exception:  # noqa: BLE001 — no contract → no gate
        return {"has_contract": False, "fade": {}, "underweight": {},
                "leverage": {}, "core": {}, "chalk_pair": [], "slate": ""}
    fade, uw = {}, {}
    for c in d.get("calls") or []:
        nm, v = c.get("name"), c.get("verdict")
        if not nm:
            continue
        if v in ("fade", "lean_fade"):
            fade[_strat_norm(nm)] = (str(nm), v)
        elif v == "underweight":
            uw[_strat_norm(nm)] = str(nm)
    lev = {_strat_norm(c["name"]): str(c["name"])
           for c in d.get("leverage_candidates") or [] if c.get("name")}
    core = {_strat_norm(r["name"]): str(r["name"])
            for r in d.get("board") or []
            if r.get("name") and str(r.get("tier")).strip().lower() == "core"}
    pair = []
    for cp in d.get("chalk_pairs") or []:
        names = [str(x) for x in (cp.get("players") or []) if x]
        if len(names) == 2:
            pair = names
            break
    return {"has_contract": True, "fade": fade, "underweight": uw,
            "leverage": lev, "core": core, "chalk_pair": pair,
            # The card this contract was written for — the override log keys
            # on it so overrides can be joined to results.jsonl by slate.
            "slate": str(d.get("slate") or "")}


def contract_conflicts(gate: dict) -> list[str]:
    """Rules in the contract that CANNOT be satisfied together, in plain words.

    Found 8/29/26. That card's contract said, at the same time:

        Core tier (hold at least 2 of): Umar Nurmagomedov, Liu Ce
        chalk_pair (never hold both) : Umar Nurmagomedov, Liu Ce

    The Core tier had exactly two names and the forbidden pair was the SAME
    two names, so "hold both" and "never hold both" were asked at once. The
    full gate returned **0 of 7,500** lineups. `eligible_indexes` then did its
    job and relaxed `core` — the safety valve worked — but it reported only
    "relaxed: core", which reads as "the pool was thin". It was not thin. The
    contract was self-cancelling, and nothing said so.

    A relaxation caused by a CONTRADICTION and one caused by a THIN POOL need
    opposite responses: thin means trust the remaining rows, contradictory
    means go fix the strategy. So they must never render the same way.

    Returns [] when the contract is coherent (the normal case)."""
    if not gate.get("has_contract"):
        return []
    out: list[str] = []
    core = gate.get("core") or {}
    pair = gate.get("chalk_pair") or []
    fade = gate.get("fade") or {}
    uw = gate.get("underweight") or {}

    # Core needs min(2, len(core)) names. When Core holds 2 or fewer, meeting
    # it means holding ALL of them — so a forbidden pair inside Core is a
    # straight contradiction. (With 3+ Core names another legal pair exists.)
    if len(pair) == 2 and core and len(core) <= 2:
        pair_norm = {_strat_norm(pair[0]), _strat_norm(pair[1])}
        if pair_norm <= set(core):
            out.append(
                f"the strategy names only two must-have players "
                f"({', '.join(sorted(core.values()))}) and asks every lineup to "
                f"hold {min(2, len(core))} of them. It ALSO says never hold "
                f"{pair[0]} and {pair[1]} together, because too many other teams "
                "will. Those are the same two players. So the strategy asks for "
                "both and bans both at the same time, and no lineup on earth can "
                "do it. Fix it by naming a third must-have player, or by taking "
                "one of these two off the must-have list.")

    # A player the strategy both anchors on and tells you to avoid.
    both = set(core) & set(fade)
    for k in sorted(both):
        out.append(f"the strategy lists {core[k]} as a must-have player AND tells "
                   f"you to {'mostly avoid' if fade[k][1] == 'lean_fade' else 'never play'} "
                   "him. Both cannot be true. One of the two calls has to go.")

    # FADE beats UNDERWEIGHT — "nowhere" and "less than the crowd, never zero"
    # cannot both hold. The gate honors the FADE, which silently voids the
    # softer call, so say which one is actually running.
    for k in sorted(set(uw) & set(fade)):
        out.append(f"the strategy says to use {uw[k]} LESS than the crowd, and "
                   "also says to "
                   f"{'mostly avoid' if fade[k][1] == 'lean_fade' else 'never play'} "
                   "him. The stronger call wins, so the 'less than the crowd' "
                   "note is doing nothing here.")
    return out


# Rules are dropped in THIS order when the pool can't fill a slice under the
# full gate. `fade` is absent on purpose — "play him nowhere" never relaxes.
# `underweight` is absent for the OPPOSITE reason (8/28/26, codified from
# mma-se-2026-08-23-underweight-gate-deletes-a-whole-pool-branch): it is not a
# hard rule at all. UNDERWEIGHT means "less than the crowd, never zero" — the
# strategy's own definition — and excluding every carrier collapsed a 60/40
# read into a 100/0 ban: the 8/23 Clinch pool held a lineup scoring exactly
# the winning 720.92, and the gate removed it over one UNDERWEIGHT call
# (Padilla, 111.35, in two of the three winning lineups). The cost was
# asymmetric: the call being right saves a few ownership points, the call
# being wrong deletes the winner. Underweight is now a SOFT rule — carriers
# stay pickable, flagged ⚠ as a cost (`soft_notes`), priced in the gate
# summary, and capped at pick time (`parse_pick`: never the same underweight
# player in EVERY entry of a multi-entry contest).
# `leverage` left this tuple 8/28/26 and is not a rule of any strength —
# not hard, not soft, not a warning (user directive: "i really dont think
# that should be a hard and fast rule… the point of the grade tab is to
# ensure lineups are following the CURRENT SLATE STRATEGY"). Two reasons,
# and the second is the deciding one:
#   1. The ledger: `mma-se-2026-07-19-sharp-envelope-is-a-rate-not-a-per-
#      bullet-quota` — the sharks carry a low-owned piece at a ~15% RATE,
#      so a per-lineup version inflates their real behavior ~7x, and both
#      7/19 contest winners carried ZERO sub-10% pieces.
#   2. It was never a strategy call. `leverage_candidates` is a mechanical
#      ownership screen (`landscape.py`, own < 10%). The strategy has to
#      ADDRESS each name in prose; addressing is not playing. Enforcing it
#      here made the gate impose a universal ownership rule while claiming
#      to enforce THIS slate's strategy — the thing the gate exists to do.
_RELAX_ORDER = ("core", "chalk_pair")
_GATE_MIN_ROWS = 25   # below this the slice stops being a real choice


def compliance(roster: list, gate: dict, relaxed: tuple = ()) -> list[str]:
    """The strategy rules THIS roster breaks, in plain words.

    **THE STRATEGY IS A GUIDE, NOT A GATE (user directive 8/29/26).** This
    function still NAMES every rule a roster breaks — that has not changed and
    is what the cost column and the override log are built on. What changed is
    that a non-empty result no longer DELETES the lineup: `eligible_indexes`
    keeps every row and prices the breaks instead (see `strategy_costs`).

    Why the reversal, and it IS a reversal of the emphatic 8/15/26 directive:
    across 14 archived cards the hard gate kept 96.9% of pool ceiling (median),
    so it was never the main leak — but it allowed ZERO lineups on 3 of those
    14 cards, cost 87 points of ceiling on 8/09 MMA, and on 8/29 it deleted
    BOTH contest winners over one LEAN FADE call. And the deciding argument:
    while the strategy could never be violated, there was no way to measure
    whether following it wins. Overrides are now logged (`log_override`) so
    that question gets an answer instead of an assumption.

    UNDERWEIGHT and LEVERAGE remain outside this list — they were demoted
    8/28/26 for the same reason, one step earlier."""
    if not gate.get("has_contract"):
        return []
    names = {_strat_norm(str(p)) for p in roster}
    out = []
    # "fade" in `relaxed` is honored ONLY so `rule_price` can isolate one rule
    # at a time — the gate itself never relaxes fade (`_RELAX_ORDER` omits it,
    # and no gate path passes it here). Before this, pricing the Core or
    # chalk-pair rule also counted every fade-carrying lineup, so their
    # "removes N of M" numbers were inflated whenever a fade call existed.
    if "fade" not in relaxed:
        hit_fade = [gate["fade"][n] for n in names & set(gate.get("fade") or {})]
        for nm, verdict in hit_fade:
            out.append(f"carries {nm} — the strategy calls him "
                       f"{'LEAN FADE' if verdict == 'lean_fade' else 'FADE'}")
    core = gate.get("core") or {}
    if "core" not in relaxed and core:
        need = min(2, len(core))
        have = len(names & set(core))
        if have < need:
            out.append(f"has {have} Core-tier player(s), the strategy's anchors "
                       f"— it needs {need}")
    pair = gate.get("chalk_pair") or []
    if "chalk_pair" not in relaxed and len(pair) == 2:
        if {_strat_norm(pair[0]), _strat_norm(pair[1])} <= names:
            out.append(f"carries both {pair[0]} and {pair[1]} — the most "
                       "duplicated pair, the one a sharp refuses")
    return out


def soft_notes(roster: list, gate: dict) -> list[str]:
    """The SOFT strategy costs this roster carries — UNDERWEIGHT calls only.
    These never reject a pick or remove a pool row; they are shown as ⚠ so
    the cost of a soft call is visible wherever the lineup appears.

    Carrying no leverage-list player is deliberately NOT here (8/28/26): the
    list is an ownership screen, not a strategy call, so its absence is not a
    cost of any size (see `_RELAX_ORDER`)."""
    if not gate.get("has_contract"):
        return []
    names = {_strat_norm(str(p)) for p in roster}
    return [f"carries {gate['underweight'][n]} — an UNDERWEIGHT call (less "
            "than the crowd, never zero; a carrier must earn its seat on "
            "sim numbers)"
            for n in sorted(names & set(gate.get("underweight") or {}))]


def eligible_indexes(pool: dict, gate: dict,
                     min_rows: int = _GATE_MIN_ROWS) -> dict:
    """Which pool rows the picker may see — since 8/29/26, ALL of them.

    The strategy is a guide, not a gate (user directive). `allowed` is now the
    whole pool and `relaxed` is always empty; what the rules produce instead is
    a per-row COST (`strategy_costs`) that rides the table, has to be argued
    against in writing, and is logged when overridden.

    `full` is retained and still means "rows that break NO strategy rule" —
    it is the honest headline number ("N of M follow the strategy outright")
    and the denominator the override log is read against. `_RELAX_ORDER` and
    `min_rows` are dead as filters and kept only so old callers don't break.

    Returns `{"allowed", "relaxed", "full", "total", "conflicts", "clean"}`."""
    rosters = pool.get("rosters") or []
    everything = set(range(len(rosters)))
    if not gate.get("has_contract"):
        return {"allowed": everything, "relaxed": [], "full": len(rosters),
                "total": len(rosters), "conflicts": [], "clean": everything}
    clean = {i for i, r in enumerate(rosters) if not compliance(r, gate)}
    return {"allowed": everything, "relaxed": [], "full": len(clean),
            "total": len(rosters), "conflicts": contract_conflicts(gate),
            "clean": clean}


def strategy_costs(roster: list, gate: dict) -> list[str]:
    """Every strategy cost this roster carries — hard-rule breaks AND soft
    ones — in one list, because since 8/29/26 they are the same KIND of thing:
    a price the pick has to be worth, not a reason the row cannot exist."""
    return compliance(roster, gate) + soft_notes(roster, gate)


def cost_tag(roster: list, gate: dict) -> str | None:
    """The short `strategy cost` cell for the slice table. None = no cost."""
    hard = compliance(roster, gate)
    soft = soft_notes(roster, gate)
    bits = ["‼ " + _cost_head(h) for h in hard] + ["⚠ " + _cost_head(x) for x in soft]
    return "; ".join(bits) if bits else None


def _cost_head(text: str) -> str:
    """First clause of a rule description — the table needs a label, not prose."""
    return str(text).split(" — ")[0].split(" (")[0].strip()


_OVERRIDE_FILE = "strategy_overrides.jsonl"


def log_override(slug: str, slate: str, contest: str, index: int,
                 roster: list, costs: list, reason: str,
                 rules_dir: Path | None = None) -> Path:
    """Record that a pick knowingly broke the slate strategy, and why.

    This is the whole point of softening the gate. A rule that can never be
    broken generates no evidence about whether it was worth following; one
    logged override per pick turns "does the strategy win?" into a question
    the autopsy can answer. Scored later against the entry's real finish —
    the record deliberately carries no result field, because the result is
    already in results.jsonl keyed by the same slate.

    Append-only, one JSON object per line, next to the other learning logs."""
    base = rules_dir or (Path(__file__).parent.parent / "rules")
    path = base / slug / _OVERRIDE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    rec = {"slate": slate, "contest": contest, "index": int(index),
           "roster": list(roster), "costs": list(costs),
           "reason": str(reason or "").strip()}
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return path


def override_report(slug: str, rules_dir: Path | None = None) -> dict:
    """How often the strategy has been overridden, and on which rules.

    Read this beside results.jsonl in the autopsy: if overridden picks finish
    better than clean ones over enough slates, the strategy is costing upside;
    if worse, the gate was earning its keep. Neither answer is available while
    the rule is absolute, which is why it no longer is."""
    base = rules_dir or (Path(__file__).parent.parent / "rules")
    path = base / slug / _OVERRIDE_FILE
    if not path.exists():
        return {"n": 0, "slates": [], "by_rule": {}, "rows": []}
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    by_rule: dict = {}
    for r in rows:
        for c in r.get("costs") or []:
            head = _cost_head(c)
            by_rule[head] = by_rule.get(head, 0) + 1
    return {"n": len(rows),
            "slates": sorted({r.get("slate") for r in rows if r.get("slate")}),
            "by_rule": by_rule, "rows": rows}


def _contest_join_key(name: str) -> str:
    """Join key between a Sim contest label and a results-ledger contest name.
    The Sim label carries a trailing type tag the ledger drops —
    'UFC $3K Clinch [Single Entry] (SE)' vs 'UFC $3K Clinch [Single Entry]'."""
    s = re.sub(r"\s*\((se|3-?max|5-?max|20-?max|150-?max|mme)\)\s*$", "",
               str(name or ""), flags=re.I)
    return re.sub(r"\s+", " ", s).casefold().strip()


def override_outcomes(slug: str, rules_dir: Path | None = None) -> dict:
    """Overridden picks vs clean picks, joined to REAL finishes — the readout
    the 8/29/26 gate-softening exists to feed.

    `log_override` records that a pick knowingly broke the strategy;
    `override_report` counts those records. Neither answers the question that
    justified the whole change: DO overridden picks finish better or worse
    than clean ones? This walks every archived slate in `rules/<slug>/history/`
    and joins, per contest:

        lineup_selection.json  — the picks; each carries `override` (the rules
                                 it broke) when it was an override, nothing
                                 when it was clean
        results.json           — the same contest's real finish
                                 (`best_percentile`, LOWER is better)

    enriched with the written whys from strategy_overrides.jsonl where the
    slate matches. A contest counts as OVERRIDDEN when any of its picks broke
    a rule.

    Returns {"rows", "clean", "override", "by_rule", "n_slates"} where `clean`
    and `override` are {"n", "median_pctile", "mean_pctile"} (None until data
    exists) and `by_rule` maps each broken rule to its finish percentiles.
    Read it with the sample size showing — a handful of overrides proves
    nothing yet, and the panel that renders this says so."""
    base = rules_dir or (Path(__file__).parent.parent / "rules")
    hist_root = base / slug / "history"
    reasons: dict = {}
    for r in override_report(slug, rules_dir=rules_dir)["rows"]:
        key = (str(r.get("slate") or ""), _contest_join_key(r.get("contest")))
        if r.get("reason"):
            reasons[key] = r["reason"]
    rows: list[dict] = []
    if hist_root.exists():
        for hist in sorted(hist_root.iterdir()):
            try:
                sel = json.loads((hist / "lineup_selection.json").read_text())
                res = json.loads((hist / "results.json").read_text())
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(sel, dict) or sel.get("schema_version") != 2:
                continue
            finishes = {_contest_join_key(c.get("name")): c
                        for c in res.get("contests") or [] if c.get("name")}
            slate = str(res.get("slate_label") or "")
            for label, rec in (sel.get("contests") or {}).items():
                fin = finishes.get(_contest_join_key(label))
                if not fin or fin.get("best_percentile") is None:
                    continue   # never entered / never logged — nothing to score
                picks = (rec or {}).get("picked") or []
                broken = sorted({_cost_head(rule) for p in picks
                                 for rule in (p.get("override") or [])})
                rows.append({
                    "date": str(res.get("date") or ""),
                    "slate": slate,
                    "contest": str(label),
                    "n_picks": len(picks),
                    "n_override": sum(1 for p in picks if p.get("override")),
                    "overridden": bool(broken),
                    "rules": broken,
                    "why": reasons.get((slate, _contest_join_key(label))),
                    "pctile": float(fin["best_percentile"]),
                    "field_size": fin.get("field_size"),
                })

    def _agg(sub: list[dict]) -> dict:
        p = sorted(r["pctile"] for r in sub)
        if not p:
            return {"n": 0, "median_pctile": None, "mean_pctile": None}
        mid = len(p) // 2
        med = p[mid] if len(p) % 2 else (p[mid - 1] + p[mid]) / 2
        return {"n": len(p), "median_pctile": round(med, 1),
                "mean_pctile": round(sum(p) / len(p), 1)}

    by_rule: dict = {}
    for r in rows:
        for rule in r["rules"]:
            by_rule.setdefault(rule, []).append(r["pctile"])
    return {"rows": rows,
            "clean": _agg([r for r in rows if not r["overridden"]]),
            "override": _agg([r for r in rows if r["overridden"]]),
            "by_rule": {k: sorted(v) for k, v in sorted(by_rule.items())},
            "n_slates": len({r["slate"] for r in rows})}


def override_outcomes_md(data: dict) -> str:
    """The override-outcome panel, in plain words. Percentile: LOWER is
    better — 5 means the entry beat 95% of the field."""
    cl, ov = data.get("clean") or {}, data.get("override") or {}
    if not data.get("rows"):
        return ("No archived contest has both a saved pick and a logged "
                "result yet. Picks made from the Grade tab and logged in the "
                "Autopsy start filling this in automatically.")
    lines = [
        "Every archived contest, split by whether the pick knowingly broke "
        "the slate strategy. Finish is a percentile of the field — **lower "
        "is better** (5 means the entry beat 95% of the field).",
        "",
        "| picks | contests | median finish | average finish |",
        "|---|---:|---:|---:|",
        f"| followed the strategy | {cl.get('n', 0)} | "
        f"{cl.get('median_pctile') if cl.get('n') else '—'} | "
        f"{cl.get('mean_pctile') if cl.get('n') else '—'} |",
        f"| overrode a rule | {ov.get('n', 0)} | "
        f"{ov.get('median_pctile') if ov.get('n') else '—'} | "
        f"{ov.get('mean_pctile') if ov.get('n') else '—'} |",
        "",
    ]
    if data.get("by_rule"):
        lines.append("Finishes when each rule was the one overridden:")
        for rule, pcts in data["by_rule"].items():
            shown = ", ".join(f"{p:g}" for p in pcts[:8])
            lines.append(f"- **{rule}** — {len(pcts)} contest(s), "
                         f"finish percentile(s): {shown}")
        lines.append("")
    n_ov = ov.get("n", 0)
    if n_ov < 8:
        lines.append(
            f"**UNDECIDED — only {n_ov} override(s) so far.** The house rule "
            "applies here too: no verdict before ~8 samples. Keep overriding "
            "when the argument is real; this table is how we find out whether "
            "those arguments win.")
    elif ov.get("median_pctile") is not None and cl.get("median_pctile") is not None:
        better = ov["median_pctile"] < cl["median_pctile"]
        lines.append(
            "**Read:** overridden picks have finished "
            + ("BETTER" if better else "WORSE")
            + " than clean ones so far. "
            + ("The strategy may be costing upside — worth a framework "
               "review." if better else
               "The strategy has been earning its keep — overrides need a "
               "higher bar."))
    return "\n".join(lines)


def rule_price(gate: dict, pool: dict, rule: str,
               contest: dict | None = None) -> dict:
    """What one hard rule costs, in lineups AND in sim quality.

    Counting alone is not a price. On 8/29/26 the LEAN FADE call on Sean
    Woodson removed **1,899 of 7,500** lineups — a quarter of the pool — and
    both contest winners were inside the removed quarter. The count was
    already shown. What was not shown is that the deleted branch held some of
    the pool's strongest simmed rows, which is the part that would have made
    the call worth a second look BEFORE lock.

    So when `contest` carries metrics, this also reports how many of the
    pool's top 50 by Top-1% and by ROI the rule deletes, and the best simmed
    row it takes with it. All of it is available pre-lock — no result data.

    Returns {"n", "total", "pct", "top50_top1", "top50_roi",
    "best_top1", "best_roi"}; the sim-quality keys are None without metrics."""
    rosters = (pool or {}).get("rosters") or []
    out = {"n": 0, "total": len(rosters), "pct": 0.0, "top50_top1": None,
           "top50_roi": None, "best_top1": None, "best_roi": None}
    if not rosters:
        return out
    # Isolate ONE rule by relaxing the others — the same trick `_price` used.
    others = tuple(r for r in ("core", "chalk_pair")
                   if r != rule) + (("fade",) if rule != "fade" else ())
    removed = [i for i, r in enumerate(rosters)
               if compliance(r, gate, relaxed=others)]
    out["n"] = len(removed)
    out["pct"] = round(100 * len(removed) / len(rosters), 1)
    m = (contest or {}).get("metrics") or {}
    if not removed or not m:
        return out
    rem = set(removed)
    for key, top_k, best_k in (("top1_pct", "top50_top1", "best_top1"),
                               ("roi_pct", "top50_roi", "best_roi")):
        vals = m.get(key)
        if not vals or len(vals) < len(rosters):
            continue
        order = sorted(range(len(rosters)), key=lambda i: -(vals[i] or 0))
        out[top_k] = sum(1 for i in order[:50] if i in rem)
        out[best_k] = round(float(max((vals[i] or 0) for i in removed)), 2)
    return out


def gate_summary(gate: dict, elig: dict, pool: dict | None = None,
                 contest: dict | None = None) -> str:
    """One plain-language block naming the rules every slice row satisfies —
    rendered into the digest Claude reads and into the app. When `pool` is
    given, each rule is PRICED: how many pooled lineups it alone removes, and
    how many carry each underweight name — so the cost of every call is
    visible before the pick (the 8/23 lesson: an unpriced soft call silently
    deleted the branch holding the Clinch winner). With `contest` the price
    also names the SIM QUALITY the rule deletes (8/29/26 — see `rule_price`).

    A self-cancelling contract (`contract_conflicts`) leads the block, because
    it means the relaxation below was forced by a contradiction rather than by
    a thin pool, and those two need opposite responses from the reader."""
    if not gate.get("has_contract"):
        return ("No slate strategy contract was found, so no strategy rules "
                "could be enforced on this table.")

    rosters = (pool or {}).get("rosters") or []
    norms = [{_strat_norm(str(p)) for p in r} for r in rosters]

    def _price(rule: str) -> str:
        """' — removes N of the M pooled lineups' for one hard rule alone,
        plus the sim quality it takes with them when metrics are available."""
        if not rosters:
            return ""
        pr = rule_price(gate, pool or {}, rule, contest)
        txt = (f" — removes {pr['n']:,} of the {pr['total']:,} pooled lineups "
               f"({pr['pct']}%)")
        bits = []
        if pr["top50_top1"]:
            bits.append(f"{pr['top50_top1']} of the pool's 50 best rows by Top-1%")
        if pr["top50_roi"]:
            bits.append(f"{pr['top50_roi']} of the 50 best by ROI")
        if bits:
            txt += ", including " + " and ".join(bits)
        if pr["best_top1"] is not None:
            txt += (f"; the best lineup it removes had a {pr['best_top1']}% chance "
                    "of finishing first — about 1 in "
                    f"{max(1, round(100 / max(pr['best_top1'], 0.01)))}")
        return txt

    rules = []
    if gate.get("fade"):
        rules.append("no player the strategy called FADE or LEAN FADE ("
                     + ", ".join(sorted(nm for nm, _v in gate["fade"].values()))
                     + ")" + _price("fade"))
    if gate.get("core") and "core" not in elig.get("relaxed", []):
        rules.append(f"at least {min(2, len(gate['core']))} Core-tier players "
                     "(the strategy's anchors)" + _price("core"))
    if len(gate.get("chalk_pair") or []) == 2 \
            and "chalk_pair" not in elig.get("relaxed", []):
        rules.append(f"never both {gate['chalk_pair'][0]} and "
                     f"{gate['chalk_pair'][1]} (the most duplicated pair)"
                     + _price("chalk_pair"))
    lines = []
    conflicts = elig.get("conflicts") or contract_conflicts(gate)
    if conflicts:
        lines += [
            "🛑 THIS SLATE'S STRATEGY CONTRADICTS ITSELF. The rules below "
            "cannot all be true at once, so the app had to drop one to leave "
            "anything pickable. This is NOT a thin pool — it is a contract "
            "that needs fixing before the next slate:",
        ]
        lines += [f"  - {c}" for c in conflicts]
        lines += ["Read every rule below knowing one of them was never "
                  "enforceable.", ""]
    lines += ["THE SLATE STRATEGY IS A GUIDE, NOT A GATE (8/29/26). Every "
              "lineup in the pool is on the table below — nothing was deleted "
              "for breaking a rule. What each rule costs, instead:"]
    lines += [f"- {r}" for r in rules]
    lines.append(
        f"\n{elig.get('full', 0):,} of {elig.get('total', 0):,} pooled lineups "
        "break NO strategy rule. The rest are still pickable and carry their "
        "price in the `cost` column: `‼` is a rule the strategy stated "
        "outright, `⚠` is a softer call. **You may pick a row with a cost — "
        "but the why must NAME the player and the rule and say what makes the "
        "lineup worth it.** An unexplained break is rejected, because the "
        "point of allowing overrides is to learn from them: every one is "
        "logged and scored against your real finish over the coming slates.")
    if gate.get("underweight"):
        uw_lines = []
        for key in sorted(gate["underweight"]):
            nm = gate["underweight"][key]
            cnt = (f" ({sum(1 for ns in norms if key in ns):,} pooled "
                   "lineups carry them)") if rosters else ""
            uw_lines.append(f"{nm}{cnt}")
        lines.append(
            "⚠️ SOFT RULE — UNDERWEIGHT means less than the crowd, NEVER "
            "zero, so these players stay pickable and their lineups are in "
            "the table, marked ⚠ in the `strategy` column: "
            + "; ".join(uw_lines) + ". A ⚠ row is carrying a cost — pick it "
            "only when its sim edge over the clean rows is real, and NEVER "
            "put the same underweight player in every entry of a "
            "multi-entry contest (the app rejects that).")
    if gate.get("leverage"):
        lines.append(
            "ℹ️ LEVERAGE IS NOT A RULE HERE. These low-owned players ("
            + ", ".join(sorted(gate["leverage"].values()))
            + ") are a screen the app runs on ownership, not a call the "
            "strategy made — the strategy has to TALK about each one, which "
            "is not the same as playing one. So a lineup carrying none of "
            "them breaks nothing and costs nothing. Where a lineup does "
            "carry one, the `strategy` column says so, as information.")
    if elig.get("relaxed"):
        why = ("the contradiction above made them impossible to satisfy"
               if conflicts else "too few lineups passed to fill the table")
        tail = ("" if conflicts else " Prefer rows that still honor them.")
        lines.append(f"⚠️ These rules had to be dropped because {why}: "
                     + ", ".join(elig["relaxed"]) + "." + tail)
    return "\n".join(lines)


def _strat_norm(name: str) -> str:
    """Join key for strategy-contract names vs Sim roster names (case,
    periods, hyphens — 'J.T. Poston' == 'JT Poston', 'Macintyre' ==
    'MacIntyre'). Kept local + tiny; both sides are already clean vendor
    names, unlike DK standings parsing."""
    s = re.sub(r"[.']", "", str(name))          # J.T. -> JT, O'Neal -> ONeal
    return re.sub(r"[\-\s]+", " ", s).casefold().strip()


def roster_key(names) -> str:
    """Order-insensitive identity of one roster: 'a|b|c…' over sorted names.

    RAW names on purpose — this key is persisted in the picks file and read
    back by `taken_roster_keys`, so normalizing it would orphan every pick
    already on disk. For comparing two sets that may spell a name differently,
    use `compare_sets` (which normalizes)."""
    return "|".join(sorted(str(n) for n in names))


def match_key(names) -> str:
    """Normalized roster identity, for COMPARING two sets of rosters (never
    persisted). Folds accents/periods/suffixes via the autopsy normalizer so a
    spelling difference can't fake a disagreement."""
    from src.autopsy import _norm_name
    return "|".join(sorted(_norm_name(n) for n in names))


def compare_sets(sim_rosters: list, claude_rosters: list) -> dict:
    """How much two independently-chosen entry sets for the SAME contest agree.

    `{n_sim, n_claude, n_match, matched}` — `matched` is the set of normalized
    roster keys present in both. The Sim's diversifier picks on sim math; the
    Analyzer's pick runs strategy-gated and BLIND to the Sim's set, so an
    overlap means two independent processes landed on the same six players.
    Agreement is a signal, never a conflict."""
    sim_keys = {match_key(r) for r in sim_rosters or [] if r}
    cl_keys = {match_key(r) for r in claude_rosters or [] if r}
    return {
        "n_sim": len(sim_keys),
        "n_claude": len(cl_keys),
        "matched": sim_keys & cl_keys,
        "n_match": len(sim_keys & cl_keys),
    }


# ---------------------------------------------------------------------------
# Paths + persistence (schema v2: per-contest picks)
# ---------------------------------------------------------------------------

def _path(slug: str) -> Path:
    return _SELECTION_DIR / f"{slug}.json"


def contest_file_key(label, declared: dict | None) -> str:
    """Stable per-contest file/session key: the declared contest's 8-hex id
    when matched, else a slugified sim label (deterministic, fs-safe)."""
    if declared and declared.get("id"):
        return str(declared["id"])
    s = re.sub(r"[^a-z0-9]+", "-", str(label or "").lower()).strip("-")
    return s[:40] or "contest"


def pick_path(slug: str, key: str) -> Path:
    return _SELECTION_DIR / f"{slug}__{key}_pick.md"


def slice_path(slug: str, key: str) -> Path:
    return _SELECTION_DIR / f"{slug}__{key}_slice.md"


def load_selection(slug: str) -> dict | None:
    """The per-contest picks file, or None (absent, unreadable, pre-v2 —
    old files simply regenerate; the store is slate-scoped)."""
    p = _path(slug)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict) or data.get("schema_version") != 2:
        return None
    return data if data.get("contests") else None


def save_contest_pick(slug: str, pool: dict, label: str, declared: dict | None,
                      picks: list[dict], why: str | None) -> dict:
    """Persist one contest's validated picks into the v2 selection file.
    Returns the full payload after the write."""
    data = load_selection(slug) or {
        "schema_version": 2,
        "slug": slug,
        "pool_fp": pool.get("pool_fp"),
        "pool_len": pool.get("pool_len"),
        "contests": {},
    }
    # A pick belongs to ONE pool; a re-sent pool invalidates old picks.
    if data.get("pool_fp") != pool.get("pool_fp"):
        data = {"schema_version": 2, "slug": slug,
                "pool_fp": pool.get("pool_fp"),
                "pool_len": pool.get("pool_len"), "contests": {}}
    data["contests"][str(label)] = {
        "picked": picks,
        "why": why,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "declared_contest_id": (declared or {}).get("id"),
    }
    _SELECTION_DIR.mkdir(parents=True, exist_ok=True)
    _path(slug).write_text(json.dumps(data, indent=2))
    return data


def taken_roster_keys(slug: str, pool: dict | None,
                      exclude_label: str | None = None) -> dict:
    """`{roster_key: contest label}` for every lineup already picked in one of
    THIS slate's other contests — the one-lineup-one-contest rule (user
    directive 8/15/26, all sports).

    `exclude_label` is the contest being picked right now: its own saved picks
    never block it, so re-running a pick is always allowed. Picks made against
    a different pool fingerprint are stale and count as nothing (the Sim re-sent
    the pool, so the indexes no longer mean anything)."""
    data = load_selection(slug)
    if not data:
        return {}
    if pool and data.get("pool_fp") != pool.get("pool_fp"):
        return {}
    rosters = (pool or {}).get("rosters") or []
    taken: dict = {}
    for label, rec in (data.get("contests") or {}).items():
        if exclude_label is not None and str(label) == str(exclude_label):
            continue
        for p in (rec or {}).get("picked") or []:
            key = p.get("roster_key")
            if not key:  # older row / hand-edited file — rebuild from the pool
                i = p.get("index")
                if i is None or i >= len(rosters):
                    continue
                key = roster_key(rosters[i])
            taken.setdefault(key, str(label))
    return taken


def clear_selection(slug: str) -> None:
    """Slate-scoped cleanup — the picks file plus every per-contest pick and
    slice digest."""
    if not _SELECTION_DIR.exists():
        return
    for p in [_path(slug)] + list(_SELECTION_DIR.glob(f"{slug}__*_pick.md")) \
            + list(_SELECTION_DIR.glob(f"{slug}__*_slice.md")):
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Contest matching (Sim payload contest -> declared contest)
# ---------------------------------------------------------------------------

def match_contests(pool_contests: list[dict], declared: list[dict],
                   tol: float = 0.15) -> dict:
    """{sim contest label -> declared contest dict or None}, one-to-one.

    Same idea as `contests.auto_link`: exact type match preferred, then
    field-size closeness (within `tol`). A sim contest whose type maps to a
    different declared type is never matched to it."""
    result = {str(c.get("label")): None for c in (pool_contests or [])}
    pairs = []
    for c in pool_contests or []:
        cf = c.get("field_size") or 0
        ctype = _TYPE_MAP.get(str(c.get("contest_type") or "").lower())
        for d in declared or []:
            df = d.get("field_size") or 0
            type_match = 0 if (ctype and d.get("type") == ctype) else 1
            if cf and df:
                rel = abs(cf - df) / df
                if rel > tol:
                    continue
            elif type_match:
                continue  # no field sizes AND no type match — nothing to go on
            else:
                rel = 1.0  # type matches but a field size is missing
            pairs.append((type_match, rel, str(c.get("label")), d))
    pairs.sort(key=lambda p: (p[0], p[1], p[2]))
    used_label, used_declared = set(), set()
    for _tm, _rel, label, d in pairs:
        did = d.get("id") or d.get("name")
        if label in used_label or did in used_declared:
            continue
        result[label] = d
        used_label.add(label)
        used_declared.add(did)
    return result


def as_declared(sim_contest: dict) -> dict:
    """A sim-pool contest expressed in declared-contest vocabulary, for
    contests the user never declared (grading still needs field size, type,
    and entry count)."""
    return {
        "id": None,
        "name": sim_contest.get("label"),
        "type": _TYPE_MAP.get(str(sim_contest.get("contest_type") or "").lower()),
        "field_size": sim_contest.get("field_size"),
        "my_entries": sim_contest.get("my_entries"),
        "entry_fee": sim_contest.get("entry_fee"),
        "prize_pool": sim_contest.get("prize_pool"),
        "payout_shape": None,
    }


# ---------------------------------------------------------------------------
# Candidate slice (deterministic top cut of THIS contest's pool)
# ---------------------------------------------------------------------------

def _norm(vals: list) -> list[float]:
    """Min-max normalize to [0,1]; None -> 0; constant array -> all 0.5."""
    nums = [float(v) if v is not None else None for v in vals]
    present = [v for v in nums if v is not None]
    if not present:
        return [0.0] * len(nums)
    lo, hi = min(present), max(present)
    if hi - lo < 1e-12:
        return [0.5 if v is not None else 0.0 for v in nums]
    return [((v - lo) / (hi - lo)) if v is not None else 0.0 for v in nums]


def _top_idx(vals: list, n: int, reverse: bool = True,
             universe: list | None = None) -> list[int]:
    """Indexes of the best n values (None last; ties by index — deterministic).

    `universe` restricts the ranking to those indexes, so every angle ranks the
    lineups the strategy ALLOWS. Ranking the whole pool and filtering afterwards
    is what shrank a 100-row slice to 16 — the top of the pool is mostly rows
    the gate cut."""
    idxs = range(len(vals)) if universe is None else universe
    order = sorted(idxs,
                   key=lambda i: ((vals[i] is None),
                                  -(vals[i] or 0) if reverse else (vals[i] or 0),
                                  i))
    return order[:n]


def blend_scores(pool: dict, contest: dict) -> list:
    """The ranking score. **Top-1% leads. Projection does NOT** (user directive
    8/29/26: "the picker's number 1 item to choose from should NOT be projected
    points").

        top 1 %            0.45   <- the chance this lineup WINS
        cash %             0.28
        projected points   0.17
        average ownership  0.10

    **Why projection was demoted, in one measurement.** Scale every slate so
    its best possible salary-capped lineup = 100 points. Across 14 slates:

        the typical contest WINNER projected   94
        the typical contest ENTRY  projected   94

    Winners are not further up the projection scale than the field. They sit
    in the same place. Projection is a QUALIFIER — it tells you a lineup is
    strong enough to be legal company — and it is not a DIFFERENTIATOR. What
    separates the winner is which specific plays it was right about, and the
    metric that prices that is the chance of finishing first.

    That is also why an earlier version of this function had it backwards.
    Projection has the best correlation with a lineup's FINAL SCORE (+0.179,
    ahead of cash% +0.177 and top1% +0.108) and those weights were set from
    exactly that table. But correlation-with-score is a MEAN metric, and a
    top-heavy tournament does not pay the mean. On the metric that matters —
    does a lineup that would have WON reach the picker's table at all —
    measured over 19 contests:

        top1/cash/proj/own
        0.20/0.30/0.30/0.20   47%   the old weights, projection first
        0.30/0.30/0.20/0.20   47%
        0.45/0.28/0.17/0.10   58%   <- live
        0.60/0.20/0.12/0.08   58%
        0.85/0.08/0.05/0.02   58%
        1.00/0.00/0.00/0.00   42%   top1 alone, with nothing behind it

    A broad plateau from 0.45 to 0.85, and a real fall-off at 1.00 — so top1%
    must LEAD but must not be alone. The live weights are the conservative end
    of that plateau, deliberately not its argmax. Raising ownership above 0.10
    costs a contest (0.45/0.25/0.15/0.15 → 53%), which is why it sits low
    despite being a real signal in isolation.

    **Do not re-tune this on correlation-with-score.** It is the wrong metric
    and it argues for the wrong answer: pure projection scores BEST on
    correlation (+0.160) and WORST on winner capture (27%). Optimise the tail.

    One blend for every field size (the old small-field branch existed to add
    tail weight where the payout is top-heavy; the tail now leads everywhere,
    so the branch had nothing left to do). Returns one score per pool index.

    **No-sim pool (8/29/26).** A pool can now arrive with `metrics: None` —
    built from projections and ownership, never simmed. There is no Top-1%
    or Cash% to lead with, so the two surviving signals keep their same
    RELATIVE importance: projection 0.63, ownership 0.37 (the live 0.17:0.10
    renormalized — and the same ~63:37 ratio their measured correlations
    with lineup score carry, proj +0.179 vs own +0.103). This is a weaker
    ranking, on purpose: nothing is invented to stand in for the sim.
    """
    rosters = pool.get("rosters") or []
    n = len(rosters)
    m = contest.get("metrics") or {}
    pj = _norm((pool.get("proj") or [None] * n)[:n])
    ow = _norm((pool.get("avg_own") or [None] * n)[:n])
    t1_raw = (m.get("top1_pct") or [None] * n)[:n]
    ca_raw = (m.get("cash_pct") or [None] * n)[:n]
    if not any(v is not None for v in t1_raw) \
            and not any(v is not None for v in ca_raw):
        return [0.63 * pj[i] + 0.37 * ow[i] for i in range(n)]
    t1 = _norm(t1_raw)
    ca = _norm(ca_raw)
    return [0.45 * t1[i] + 0.28 * ca[i] + 0.17 * pj[i] + 0.10 * ow[i]
            for i in range(n)]


def _coverage_fill(rosters: list, candidates: list, blend: list,
                   seats: int) -> list:
    """Fill `seats` from `candidates` for PLAYER COVERAGE, not rank order.

    Greedy: repeatedly take the highest-blend row whose players are least
    represented in what has already been chosen. Deterministic — ties break on
    blend then index, and the input order is fixed by the caller.

    Why coverage and not simply "the next 400 by blend": every angle feeding
    the slice ranks on correlated sim metrics, so rank order returns near
    duplicates of one idea. Coverage buys DIFFERENT ideas, which is the thing
    a tournament pick actually needs — and measurably: at ~500 rows, coverage
    selection reached a winning lineup in 8 of 25 contests against 6 of 25 for
    a same-sized rank cut.

    Note the ORDER of operations matters. Coverage at the old ~72-row size did
    WORSE than rank order (1 of 25 vs 2 of 25) — too few seats to cover
    anything, and spending them on spread costs quality for nothing. Coverage
    is a large-slice technique; do not apply it to a small one."""
    if seats <= 0 or not candidates:
        return []
    ranked = sorted(candidates, key=lambda i: (-blend[i], i))
    if len(ranked) <= seats:
        return ranked
    sets = {i: set(rosters[i]) for i in ranked}
    chosen = [ranked[0]]
    used = {p: 1 for p in sets[ranked[0]]}
    remaining = ranked[1:]
    # A single pass over a shrinking list; the cost term is recomputed per
    # pick because it depends on everything already chosen.
    while len(chosen) < seats and remaining:
        best_at, best_key = 0, None
        for pos, i in enumerate(remaining):
            key = (sum(used.get(p, 0) for p in sets[i]), -blend[i], i)
            if best_key is None or key < best_key:
                best_at, best_key = pos, key
        pick = remaining.pop(best_at)
        chosen.append(pick)
        for p in sets[pick]:
            used[p] = used.get(p, 0) + 1
    return chosen


def candidate_slice(pool: dict, contest: dict, k: int = _SLICE_CAP,
                    strategy: dict | None = None,
                    taken: dict | set | None = None,
                    allowed: set | None = None,
                    gate: dict | None = None) -> list[dict]:
    """THIS contest's top pool rows, deterministically: the union of the best
    lineups by each of the contest's own sim metrics, plus projection,
    low-ownership / low-duplication standouts, and (8/15/26) a STRATEGY-AWARE
    angle — lineups carrying the contract's named leverage candidates or
    UNDERWEIGHT-call players get seats even when they sim mid-pack, closing
    the numbers-only blind spot (a thesis lineup the strategy argued for must
    be pickable). Capped at `k` by a blend score with all standout/strategy
    seats reserved. Same inputs in, same slice out — the claude pass only
    ever chooses among these real rows.

    `taken` (roster_key -> contest label, from `taken_roster_keys`) removes the
    lineups already picked for another contest on this slate, so one lineup is
    only ever entered once (user directive 8/15/26).

    `allowed` (from `eligible_indexes`) is the pickable universe. Since
    8/29/26 that is the WHOLE pool — the strategy is a guide, not a gate, so a
    rule-breaking lineup reaches the table carrying its price in the `cost`
    column rather than being deleted before anyone sees it. The parameter is
    kept because "one lineup, one contest" and any future hard exclusion still
    flow through it.

    `gate` (from `strategy_gate`) prices each row. Pass it whenever there is a
    contract; without it the `cost` column is empty and a break is invisible."""
    rosters = pool.get("rosters") or []
    n = len(rosters)
    if n == 0:
        return []
    m = contest.get("metrics") or {}
    top1 = (m.get("top1_pct") or [None] * n)[:n]
    win = (m.get("win_pct") or [None] * n)[:n]
    cash = (m.get("cash_pct") or [None] * n)[:n]
    roi = (m.get("roi_pct") or [None] * n)[:n]
    proj = (pool.get("proj") or [None] * n)[:n]
    avg_own = (pool.get("avg_own") or [None] * n)[:n]
    dupes = contest.get("exp_dupes")

    # One lineup, one contest: rosters already picked elsewhere on this slate
    # never enter the slice, whatever index they sit at in the pool.
    taken_keys = set(taken or ())
    blocked = {i for i in range(n) if roster_key(rosters[i]) in taken_keys} \
        if taken_keys else set()
    # The strategy gate: anything it excluded can never be chosen by any angle.
    if allowed is not None:
        blocked |= {i for i in range(n) if i not in allowed}

    chosen: list[int] = []
    seen: set = set(blocked)

    def _add(idxs):
        for i in idxs:
            if i not in seen:
                seen.add(i)
                chosen.append(i)

    # Every angle ranks only the lineups still standing after the gate + the
    # one-per-contest cut, so the slice is the top of what is ACTUALLY pickable.
    universe = [i for i in range(n) if i not in blocked]
    if not universe:
        return []
    u = len(universe)

    # Angle sizes scale with the cap so a 500-row slice is not 120 ranked rows
    # plus 380 coverage picks. **Seat order matches `blend_scores`: the chance
    # of WINNING leads, projection does not** (user directive 8/29/26). The
    # first-listed angle claims its seats first, so this order is not cosmetic
    # — an earlier version seated projection first and handed the top of the
    # table to lineups that project like the field median, which is where the
    # field median already is.
    _a = max(1, k // 10)

    def _has(arr) -> bool:
        return any(v is not None for v in arr)

    # A no-sim pool (metrics: None, 8/29/26) has no sim angles to seat — an
    # angle over an all-None column would just seat rows by pool index.
    has_sim = _has(top1) or _has(cash) or _has(roi) or _has(win)
    if _has(top1):
        _add(_top_idx(top1, _a, universe=universe))
    if _has(cash):
        _add(_top_idx(cash, _a, universe=universe))
    if _has(roi):
        _add(_top_idx(roi, _a, universe=universe))
    # Projection still earns seats — a lineup has to be strong enough to be
    # legal company, and projection is what says so — but it qualifies rather
    # than leads, so it gets a half seat like win%. With NO sim numbers it is
    # the strongest signal left and takes the full seat instead.
    _add(_top_idx(proj, _a if not has_sim else max(1, _a // 2),
                  universe=universe))
    if _has(win):
        _add(_top_idx(win, max(1, _a // 2), universe=universe))
    # Ownership: BOTH ends get seats. The most-owned rows are not a mistake to
    # be screened out and the least-owned are not a bonus — it is a real but
    # minor signal (NASCAR's best at +0.121, worth nothing in PGA Classic).
    # With no sim it is the only other signal, so both ends widen a step.
    _own_seats = max(1, (_a // 2) if not has_sim else (_a // 4))
    _add(_top_idx(avg_own, _own_seats, universe=universe))
    _add(_top_idx(avg_own, _own_seats, universe=universe, reverse=False))
    # Standouts within the top quartile by this contest's top1: the
    # lowest-owned (leverage) and, when dupe data exists, least-duplicated.
    # These carry reserved seats through the cap below — they were added for
    # their angle, not their blend score, and the blend must not evict them.
    standouts: set = set()
    # The quartile that anchors the standouts ranks on this contest's top1;
    # a no-sim pool ranks it on the blend (projection + ownership) instead.
    blend = blend_scores(pool, contest)
    basis = top1 if _has(top1) else blend
    q_list = sorted(_top_idx(basis, max(1, u // 4), universe=universe))
    lev = [q_list[j] for j in _top_idx([avg_own[i] for i in q_list], 20,
                                       reverse=False)]
    _add(lev)
    standouts.update(lev)
    if dupes:
        low_dupe = [q_list[j] for j in _top_idx([dupes[i] for i in q_list], 20,
                                                reverse=False)]
        _add(low_dupe)
        standouts.update(low_dupe)

    # Strategy-aware angle (8/15/26): seat the thesis lineups the numbers
    # angles can miss. Restricted to the top HALF by this contest's top1 so a
    # named player can't drag a genuinely dead lineup into the slice.
    strat = strategy or {}
    lev_norm = {_strat_norm(nm): nm for nm in strat.get("leverage") or []}
    uw_norm = {_strat_norm(nm): nm for nm in strat.get("underweight") or []}
    strat_hits: dict[int, list] = {}
    if lev_norm or uw_norm:
        roster_norms = [{_strat_norm(p) for p in r} for r in rosters]
        top_half = set(_top_idx(basis, max(1, u // 2), universe=universe))
        for i in top_half:
            # Leverage names are what the strategy ASKED for; an underweight
            # name is a COST, flagged ⚠ so the table can never read as an
            # endorsement (8/15/26 — the old "(UW)" label did exactly that,
            # and both NASCAR picks came back carrying an underweight call).
            hit = ([lev_norm[m] for m in roster_norms[i] & set(lev_norm)]
                   + ["⚠ " + uw_norm[m] + " (UNDERWEIGHT)"
                      for m in roster_norms[i] & set(uw_norm)])
            if hit:
                strat_hits[i] = sorted(hit)
        if lev_norm:
            cov = sorted((i for i in strat_hits
                          if any(not h.startswith("⚠") for h in strat_hits[i])),
                         key=lambda i: (-len(strat_hits[i]), -(basis[i] or 0), i))
            _add(cov[:20])
            standouts.update(cov[:20])

    if len(chosen) > k:
        # Over the cap: reserved seats survive, the rest are coverage-filled.
        keep = [i for i in chosen if i in standouts]
        rest = [i for i in chosen if i not in standouts]
        rest.sort(key=lambda i: (-blend[i], i))
        chosen = keep + _coverage_fill(rosters, rest[:_SLICE_PREFILTER], blend,
                                       max(0, k - len(keep)))
    elif len(chosen) < k:
        # UNDER the cap — the normal case, and the one the first cut of this
        # rework got wrong. However wide the angles are set they produce only
        # ~200 unique rows, because they all rank correlated metrics and
        # overlap heavily. Left there, raising the cap buys nothing: the slice
        # stalls at ~200 near-identical rows (measured: diversity got WORSE
        # than the old 100-row slice, 1.74 shared players per pair vs 1.59).
        #
        # Stage 1 of the two-stage design: rank the whole pickable universe by
        # blend, keep the top `_SLICE_PREFILTER`, then coverage-fill the empty
        # seats from it. That is what buys DIFFERENT ideas instead of more of
        # the same one — and the prefilter is also what keeps the O(seats x
        # candidates) coverage pass fast on a 20,000-row pool.
        already = set(chosen)
        pre = [i for i in universe if i not in already]
        pre.sort(key=lambda i: (-blend[i], i))
        chosen = chosen + _coverage_fill(rosters, pre[:_SLICE_PREFILTER],
                                         blend, k - len(chosen))
    chosen.sort(key=lambda i: (-blend[i], i))

    def _val(arr, i, nd=2):
        v = arr[i] if arr and i < len(arr) else None
        return round(float(v), nd) if v is not None else None

    out = []
    for i in chosen:
        names = [str(x) for x in rosters[i]]
        # No marker for rows without a leverage name (8/28/26): the column
        # reports what a lineup HAS, never scolds it for what it lacks.
        hits = list(strat_hits.get(i) or [])
        out.append({
            "index": i,
            "roster": names,
            "roster_key": roster_key(names),
            "salary": (pool.get("salary") or [None] * n)[i],
            "proj": _val(proj, i),
            "avg_own": _val(avg_own, i, 1),
            "win_pct": _val(win, i),
            "top1_pct": _val(top1, i),
            "top10_pct": _val(m.get("top10_pct") or [], i, 1),
            "cash_pct": _val(cash, i, 1),
            "roi_pct": _val(roi, i, 1),
            "exp_dupes": _val(dupes or [], i),
            "strategy": ", ".join(hits) if hits else None,
            # The strategy is a guide now, so every row is pickable and each
            # carries its PRICE instead of being deleted (8/29/26).
            "cost": cost_tag(names, gate) if gate else None,
        })
    return out


def lineup_families(rows: list[dict], max_families: int = 12) -> list[dict]:
    """Group the slice into FAMILIES — sets of rows built on the same core.

    500 rows is past what anyone reads row by row, and the rows are not 500
    ideas: they are a dozen theses with variations. A family is defined by its
    CORE — the players most of its members share — so the picker chooses a
    thesis first and a row second, instead of scanning a table and taking
    whatever sits at the top of one column.

    Deterministic: seeded by the highest-blend unassigned row, grown by roster
    overlap, ties broken by index. Same slice in, same families out.

    Returns one dict per family: {core, n, ids, best_*, avg_own, example}."""
    if not rows:
        return []
    sets = [set(r.get("roster") or []) for r in rows]
    size = max((len(x) for x in sets), default=6)
    # Two rows are the same thesis when they share most of a lineup.
    need = max(2, round(size * 0.5))
    unassigned = list(range(len(rows)))
    families = []
    while unassigned and len(families) < max_families:
        seed = unassigned[0]
        members = [i for i in unassigned if len(sets[i] & sets[seed]) >= need]
        if not members:
            members = [seed]
        counts: dict = {}
        for i in members:
            for pl in sets[i]:
                counts[pl] = counts.get(pl, 0) + 1
        core = sorted((pl for pl, c in counts.items() if c >= len(members) * 0.6),
                      key=lambda pl: (-counts[pl], pl))[:4]
        families.append({
            "core": core or sorted(sets[seed])[:3],
            "n": len(members),
            "ids": [rows[i]["index"] for i in members],
            "best_top1": _fam_best(rows, members, "top1_pct"),
            "best_cash": _fam_best(rows, members, "cash_pct"),
            "best_proj": _fam_best(rows, members, "proj"),
            "avg_own": _fam_avg(rows, members, "avg_own"),
            "example": rows[members[0]]["index"],
        })
        drop = set(members)
        unassigned = [i for i in unassigned if i not in drop]
    if unassigned:   # everything past the family cap, kept honest
        families.append({"core": ["(other)"], "n": len(unassigned),
                         "ids": [rows[i]["index"] for i in unassigned],
                         "best_top1": _fam_best(rows, unassigned, "top1_pct"),
                         "best_cash": _fam_best(rows, unassigned, "cash_pct"),
                         "best_proj": _fam_best(rows, unassigned, "proj"),
                         "avg_own": _fam_avg(rows, unassigned, "avg_own"),
                         "example": rows[unassigned[0]]["index"]})
    return families


def _fam_best(rows, members, key):
    vals = [rows[i].get(key) for i in members if rows[i].get(key) is not None]
    return round(max(vals), 2) if vals else None


def _fam_avg(rows, members, key):
    vals = [rows[i].get(key) for i in members if rows[i].get(key) is not None]
    return round(sum(vals) / len(vals), 1) if vals else None


def families_md(families: list[dict]) -> str:
    """The family summary the picker reads BEFORE the row table."""
    if not families:
        return ""
    lines = [
        "## The theses on this slate",
        "",
        "The rows below are not independent lineups — they are a handful of "
        "theses with variations. Choose a THESIS first, then the row inside it "
        "that best fits the contest. Do not scan the table and take whatever "
        "sits at the top of one column.",
        "",
        "| # | core players | rows | best top1% | best cash% | best proj | avg own% | example id |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for j, f in enumerate(families, 1):
        lines.append(
            f"| {j} | {', '.join(f['core'])} | {f['n']} | {f['best_top1']} | "
            f"{f['best_cash']} | {f['best_proj']} | {f['avg_own']} | {f['example']} |")
    lines.append("")
    return "\n".join(lines)


# How far below the best row a lineup can sit and still be a statistical tie.
# Two standard errors of an independently-sampled rate — see `metric_resolution`.
_TIE_BAND_SE = 2.0


def metric_resolution(rows: list[dict], sims: int | None,
                      metric: str = "top1_pct") -> dict:
    """How big a Top-1% gap has to be before it means anything — and which
    slice rows are inside a statistical tie with the best one.

    **Why this exists (8/29/26).** The picker read the slice as an ORDERED
    LIST and only ever argued against rows ABOVE its choice on Top-1%. Both
    written rationales that night rejected a rival on a Top-1% gap of 0.08
    and 0.59 points. Meanwhile a row sitting 0.38 points BELOW the pick —
    Hasan/Gomes/Nuzzi/Liu Ce/Tsuruya/Song, 10th of 7,500 by Cash% and 13th by
    ROI — scored **696.1**, forty-seven points more than the score that won
    the contest. It was in the slice. It was never mentioned, because it
    ranked lower on the one metric the picker sorted by.

    A rate estimated from `sims` Monte Carlo runs has a standard error of
    `sqrt(p(1-p)/sims)`. At 3% on 10,000 sims that is 0.17 points, so a
    two-SE band is ±0.34 — wider than both gaps the 8/29 picker treated as
    decisive. Rows inside that band are not ranked; they are TIED, and a tie
    has to be broken on what the lineups actually are.

    *Honest caveat, stated in the output too:* every row is simmed against
    the same draws, so a PAIRED difference is measured more precisely than
    two independent standard errors imply. The band is therefore a
    conservative width, not an exact test. It is still the right instrument
    for the failure it addresses — a gap this small is never a reason to
    dismiss a roster shape you would otherwise want.

    Returns {"sims", "band", "best", "tied_ids", "spread", "known"}.
    `known` is False when the payload carried no sim count; nothing is
    invented in that case."""
    vals = [(r.get("index"), r.get(metric)) for r in rows or []
            if r.get(metric) is not None]
    if not vals:
        # `no_metric` (8/29/26): the pool was never simmed, so the metric
        # itself is absent — a different statement from "simmed, but the sim
        # count didn't ride along", and the reader note says which it is.
        return {"sims": sims, "band": None, "best": None, "tied_ids": [],
                "spread": None, "known": False, "no_metric": True}
    best = max(v for _i, v in vals)
    lo = min(v for _i, v in vals)
    out = {"sims": sims, "best": round(float(best), 2),
           "spread": round(float(best - lo), 2), "known": bool(sims)}
    if not sims or sims <= 0:
        out["band"] = None
        out["tied_ids"] = []
        return out
    # Clamp into [0, 1] before the variance term: a rate outside it makes
    # p(1-p) negative and `** 0.5` returns a COMPLEX number, which then blows
    # up on round(). Rates arrive as percentages from the sim and are normally
    # well inside range, but a hand-edited or mis-scaled column must degrade
    # to a usable band rather than crash the digest.
    p = min(max(float(best) / 100.0, 0.0), 1.0)
    se = (p * (1 - p) / float(sims)) ** 0.5 * 100.0
    # A degenerate rate (0% or 100%) has zero sampling variance, which would
    # claim infinite precision. Floor the band at the metric's own printed
    # resolution instead — two rows that round to the same value are tied.
    band = max(round(_TIE_BAND_SE * se, 2), 0.01)
    out["band"] = band
    out["tied_ids"] = [i for i, v in vals if v >= best - band]
    return out


def resolution_md(res: dict, metric_label: str = "Top-1%") -> str:
    """The resolution note the picker reads, in plain words."""
    if res.get("no_metric"):
        return (f"**There are no {metric_label} numbers on this table.** This "
                "pool was built from projections and ownership only — no "
                "simulation was run. The table is ranked on projected points "
                "and ownership, which say a lineup is strong and different, "
                "not that it wins. Decide on the lineups themselves: which "
                "plays they take, how the crowd is likely to line up against "
                "them, and what has to happen for each to pay.")
    if not res.get("known"):
        return (f"**{metric_label} resolution: unknown.** This pool was sent "
                "without its simulation count, so there is no way to say how "
                f"big a {metric_label} gap has to be to mean anything. Treat "
                "small gaps as ties and decide on the lineups themselves.")
    n = len(res.get("tied_ids") or [])
    return (
        f"**A {metric_label} gap under {res['band']} points is a TIE, not a "
        f"ranking.** These rates come from {res['sims']:,} simulations, so a "
        f"rate near {res['best']}% carries about ±{res['band']} points of "
        f"sampling noise. Across this whole table {metric_label} spans only "
        f"{res['spread']} points, so most of the table is within a few bands "
        "of everything else.\n\n"
        f"**{n} row(s) are tied with the best one** (ids: "
        + ", ".join(str(i) for i in sorted(res.get("tied_ids") or [])) + "). "
        "Choose among them on what the lineups ARE — which fights they take, "
        "which shapes they give you — never on the decimal.\n\n"
        "Two rules follow, and the second is the one that was broken on "
        "8/29/26:\n"
        f"1. Never reject a lineup because another row is {res['band']} points "
        f"higher on {metric_label}. That is noise. Say something about the "
        "lineup instead.\n"
        "2. **Look DOWN the table, not just up.** The band applies to ANY two "
        f"rows, not only to the best one: a row within {res['band']} points of "
        "the one you are leaning toward is tied with it, whether it sits above "
        "or below. Before you commit, read the rows just under your choice and "
        "say why their shape is worse. On 8/29 the row that would have won the "
        "contest by 47 points sat 0.38 points below the pick — about one band — "
        "and was never mentioned in the rationale.\n\n"
        "*Caveat: all rows share the same simulated draws, so a paired "
        "difference is measured a little more precisely than this band "
        "implies. The band is deliberately conservative.*")


def slice_digest_md(slug: str, label: str, contest: dict, declared: dict | None,
                    rows: list[dict], ownership: dict,
                    gate_md: str | None = None,
                    sims: int | None = None) -> str:
    """The candidate table the claude pass reads and picks ids from.

    `sims` (8/29/26) is the pool payload's `num_simulations`. With it the
    digest carries a RESOLUTION BAND and marks every row tied with the best
    on Top-1%, so the table reads as a set of near-equal candidates rather
    than a strict ranking — see `metric_resolution`."""
    shape = (declared or {}).get("payout_shape") or "not declared"
    my = contest.get("my_entries")
    no_sim = all(r.get("top1_pct") is None for r in rows) if rows else False
    lines = [
        f"# Candidate lineups — {label}",
        f"Contest: field {int(contest.get('field_size') or 0):,} entries · "
        f"${contest.get('entry_fee')} entry · payout shape {shape} · "
        f"you are entering {my} lineup(s).",
        ("Every lineup below was built by the Sim tool from projections and "
         "ownership — NO simulation was run, so the win/top1/cash/roi "
         "columns are empty. "
         if no_sim else
         "Every lineup below was built and simmed by the Sim tool. ")
        + "Pick ONLY from this table, by id.",
        "",
    ]
    if gate_md:
        lines += ["## The strategy gate", "", gate_md, ""]
    res = metric_resolution(rows, sims)
    tied = set(res.get("tied_ids") or [])
    fam = families_md(lineup_families(rows))
    if fam:
        lines += [fam, ""]
    lines += [("## What the table is ranked on" if no_sim
               else "## How much a Top-1% gap is worth"),
              "", resolution_md(res), ""]
    lines += [
        "## Every candidate", "",
        "| id | tie | salary | proj | avg own% | win% | top1% | cash% | roi% | dupes | cost | strategy | players |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    def _cell(v):
        return v if v is not None else "—"

    for r in rows:
        players = ", ".join(
            f"{nm} ({ownership.get(nm)}%)" if ownership.get(nm) is not None else nm
            for nm in r["roster"])
        lines.append(
            f"| {r['index']} | {'=' if r['index'] in tied else ''} | "
            f"{_cell(r.get('salary'))} | {_cell(r.get('proj'))} | "
            f"{_cell(r.get('avg_own'))} | {_cell(r.get('win_pct'))} | "
            f"{_cell(r.get('top1_pct'))} | "
            f"{_cell(r.get('cash_pct'))} | {_cell(r.get('roi_pct'))} | "
            f"{_cell(r.get('exp_dupes'))} | "
            f"{r.get('cost') or '—'} | "
            f"{r.get('strategy') or '—'} | "
            f"{players} |")
    lines.append("")
    lines.append("The `cost` column is what this lineup costs against the "
                 "slate strategy — `‼` a stated rule, `⚠` a softer call, `—` "
                 "nothing. A cost is a PRICE, not a ban: pick a costed row "
                 "whenever it is worth the price, and name the player and the "
                 "rule in your why when you do. Picking one without saying so "
                 "is rejected.")
    lines.append("")
    if not no_sim:
        lines.append("A `=` in the `tie` column means this row is "
                     "statistically TIED with the best row on Top-1% — its "
                     "number is not worse, it is the same number inside "
                     "sampling noise. Pick among the `=` rows on lineup "
                     "shape, and never write a rationale that rejects one "
                     "for a decimal.")
        lines.append("")
    lines.append("")
    lines.append("The `strategy` column names the leverage-list players this "
                 "lineup carries — the strategy asked for those, so those rows "
                 "are here for their thesis, not just their sim numbers. A ⚠ "
                 "entry is the opposite: a player the strategy called "
                 "UNDERWEIGHT (less than the crowd, never zero). Those rows "
                 "are allowed, but the ⚠ is a COST — pick one only when its "
                 "sim edge over the clean rows is real, and never put the "
                 "same underweight player in every entry of a multi-entry "
                 "contest. An EMPTY `strategy` cell means nothing is wrong "
                 "with the lineup — carrying no low-owned (leverage) name "
                 "is not a flaw, a cost, or a tiebreaker. Never prefer a row "
                 "because it holds a leverage name or reject one because it "
                 "doesn't.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pick parsing + validation — a selection can choose, never invent
# ---------------------------------------------------------------------------

def _strip_own(cell: str) -> list[str]:
    """Player names from a table cell, ownership parentheticals removed."""
    return [re.sub(r"\s*\([^)]*\)\s*$", "", p).strip()
            for p in str(cell).split(",") if p.strip()]


def _extract_why(md: str) -> str | None:
    """The pick file's **Why** block, whitespace-collapsed."""
    m = re.search(r"^\*\*Why[^\n]*\*\*:?\s*(.*?)(?=\n\s*\n|\Z)",
                  md or "", re.M | re.S)
    return (" ".join(m.group(1).split()) or None) if m else None


def _reason_covers(why: str | None, roster: list, broken: list[str]) -> bool:
    """Does the written reason actually ADDRESS the rule this pick breaks?

    Deliberately shallow: it checks that the named player (or, for the rules
    that name no player, a recognizable phrase) appears in the why. It is not
    trying to judge whether the argument is GOOD — that is the user's job when
    they read it. It only stops the failure mode this whole change would
    otherwise create, which is a pick quietly breaking the strategy and
    nobody, including the autopsy, ever knowing it happened."""
    if not why:
        return False
    low = why.lower()
    for rule in broken:
        rl = rule.lower()
        named = [p for p in roster if str(p).lower() in rl]
        if named:
            if not any(str(p).lower() in low for p in named):
                return False
        elif "core" in rl:
            if "core" not in low and "anchor" not in low:
                return False
        elif "duplicated pair" in rl:
            if "pair" not in low and "duplicat" not in low:
                return False
    return True


def parse_pick(md: str, slice_rows: list[dict], my_entries: int,
               taken: dict | None = None, gate: dict | None = None,
               relaxed: tuple = ()) -> dict:
    """Validate the claude pick file against the slice it was given.

    Returns {"picks": [{"index", "roster_key"}], "why": str|None,
    "errors": [str]}. Non-empty errors => the picks are unusable and the
    caller must save NOTHING (selection is not construction — a pick that
    isn't a real slice row, or that lists different players than its row,
    is rejected outright).

    `taken` (roster_key -> contest label) enforces one-lineup-one-contest by
    ROSTER, not by id: the same players picked for another contest are rejected
    even if the pool holds them at a second index.

    `gate` (from `strategy_gate`) is the last line of the strategy rules: a pick
    that breaks one is rejected with the broken rule named, even if it somehow
    reached the table. `relaxed` mirrors whatever `eligible_indexes` had to drop
    so the check and the table agree."""
    from src.autopsy import _norm_name

    by_index = {int(r["index"]): r for r in slice_rows}
    # Parsed BEFORE the pick loop: since 8/29/26 an override is legal only if
    # the why explains it, so the loop has to be able to read it.
    why = _extract_why(md)
    picks: list[dict] = []
    errors: list[str] = []
    seen_ids: set = set()
    seen_rosters: dict = {}
    taken = taken or {}

    lines = (md or "").splitlines()
    cols: list[str] | None = None
    table_done = False
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            if cols is not None:
                table_done = True
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        low = [c.lower() for c in cells]
        if cols is None:
            if "id" in low:
                cols = low
            continue
        if table_done:
            continue
        if set("".join(cells)) <= {"-", " ", ":"}:
            continue  # separator row
        row = dict(zip(cols, cells))
        raw_id = row.get("id", "")
        try:
            rid = int(re.sub(r"[^\d-]", "", raw_id) or "x")
        except ValueError:
            errors.append(f"'{raw_id}' is not a lineup id from the candidate table.")
            continue
        if rid not in by_index:
            errors.append(f"id {rid} is not in the candidate table — a pick "
                          "must be a real row (fabricated ids are rejected).")
            continue
        if rid in seen_ids:
            errors.append(f"id {rid} was picked twice.")
            continue
        seen_ids.add(rid)
        srow = by_index[rid]
        players_cell = row.get("players")
        if players_cell:
            listed = {_norm_name(p) for p in _strip_own(players_cell)}
            actual = {_norm_name(p) for p in srow["roster"]}
            if listed != actual:
                errors.append(
                    f"the players listed for id {rid} do not match that "
                    "lineup — a selection may never modify a roster.")
                continue
        rkey = srow["roster_key"]
        if rkey in taken:
            errors.append(f"id {rid} is the same lineup you already picked for "
                          f"\"{taken[rkey]}\" — a lineup can only be picked once.")
            continue
        if rkey in seen_rosters:
            errors.append(f"id {rid} has the same players as id "
                          f"{seen_rosters[rkey]} — a lineup can only be picked once.")
            continue
        # THE STRATEGY IS A GUIDE, NOT A GATE (8/29/26). A pick that breaks a
        # rule is no longer rejected — it is an OVERRIDE, and the only thing
        # required of it is that the pick file say why in writing. Silent
        # overrides ARE still rejected: an unexplained break generates no
        # evidence, which is the one thing this change exists to produce.
        broken = compliance(srow["roster"], gate or {}, relaxed) if gate else []
        pick = {"index": rid, "roster_key": rkey}
        if broken:
            if not _reason_covers(why, srow["roster"], broken):
                errors.append(
                    f"id {rid} breaks the slate strategy — it "
                    + "; ".join(broken) + ". That is allowed, but the pick has "
                    "to SAY SO: name the player and the rule in the why, and "
                    "give the reason the lineup is worth the cost.")
                continue
            pick["override"] = broken
        seen_rosters[rkey] = rid
        picks.append(pick)

    if len(picks) != int(my_entries):
        errors.append(f"{len(picks)} valid pick(s) but this contest takes "
                      f"exactly {my_entries} — nothing was saved.")

    # UNDERWEIGHT soft cap (8/28/26): "less than the crowd, never zero." A
    # single carrier among several entries is exactly what the verdict asks
    # for; the same underweight player in EVERY entry of a multi-entry
    # contest cannot be "less" and is rejected. Carriage otherwise only
    # WARNS — the old hard rejection here is the bug that deleted the 8/23
    # Clinch winner from all three contests.
    warnings: list[str] = []
    if gate and gate.get("has_contract") and picks and not errors:
        rosters_n = [{_strat_norm(str(p)) for p in by_index[pk["index"]]["roster"]}
                     for pk in picks]
        uw = gate.get("underweight") or {}
        if uw:
            for key in sorted(uw):
                n_carry = sum(1 for ns in rosters_n if key in ns)
                if n_carry == 0:
                    continue
                if int(my_entries) >= 2 and n_carry == len(picks):
                    errors.append(
                        f"every entry carries {uw[key]} — the strategy calls "
                        "them UNDERWEIGHT (less than the crowd, never zero), "
                        "and holding them in ALL your entries is not less. "
                        "Swap at least one lineup off them.")
                else:
                    warnings.append(
                        f"{n_carry} of {len(picks)} entr"
                        f"{'y carries' if n_carry == 1 else 'ies carry'} "
                        f"{uw[key]} — an UNDERWEIGHT call; allowed, priced "
                        "as a cost.")
        # NO leverage check of any kind (8/28/26). A pick set carrying zero
        # low-owned players is a complete, valid answer — the 7/19 winners
        # were exactly that — so it earns no error and no warning.

    return {"picks": picks if not errors else [], "why": why,
            "errors": errors, "warnings": warnings if not errors else []}
