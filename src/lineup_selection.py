"""🎯 Per-contest entry picking over the Sim's pushed pool.

**Selection is not construction (8/9/26).** This module never authors, edits,
swaps, or fixes a roster. Every lineup it handles was BUILT AND SIMMED by the
Sim tool and arrived via `data/sim_pool/<slug>.json`.

Per-contest flow (8/9/26 evening rework — the user's contests are all small
single-entry GPPs but NOT interchangeable: different field sizes, payout
shapes, and histories, so every contest gets its own pick and its own grade):

1. `candidate_slice` deterministically cuts THAT contest's top ~100 pool rows
   (by that contest's own sim metrics — top1/win/cash/roi — plus projection,
   low-ownership and low-dupe standouts).
2. `slice_digest_md` renders the slice as one id-keyed markdown table; the
   `run_contest_selection` claude pass reads it (plus the strategy, board,
   and open lessons) and PICKS exactly `my_entries` rows BY ID.
3. `parse_pick` validates the pick hard: every id must be a slice row, the
   listed players must match that row exactly, the count must equal
   `my_entries`. Any violation → errors, nothing saved. A selection can
   choose; it can never invent.
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

_SLICE_CAP = 100  # user directive 8/15/26: expanded from 50, all sports

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
    * `leverage_candidates` — every lineup must carry at least one. This is the
      recurring miss the strategy names on its own leverage screen.
    * `Core` tier from the board — at least two, the strategy's own anchors.
    * `chalk_pairs[0]` — the top duplicated pair, "what a sharp refuses".

    Returns `{"has_contract": bool, ...}`; an empty gate (no contract) filters
    nothing, and the caller decides whether to run at all."""
    p = _CONTRACT_DIR / f"{slug}.json"
    try:
        d = json.loads(p.read_text())
    except Exception:  # noqa: BLE001 — no contract → no gate
        return {"has_contract": False, "fade": {}, "underweight": {},
                "leverage": {}, "core": {}, "chalk_pair": []}
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
            "leverage": lev, "core": core, "chalk_pair": pair}


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
_RELAX_ORDER = ("core", "chalk_pair", "leverage")
_GATE_MIN_ROWS = 25   # below this the slice stops being a real choice


def compliance(roster: list, gate: dict, relaxed: tuple = ()) -> list[str]:
    """The HARD strategy rules THIS roster breaks, in plain words. Empty list =
    the lineup may be picked. `relaxed` names rules to skip (see
    `_RELAX_ORDER`). UNDERWEIGHT is deliberately NOT here — it is a soft cost
    (`soft_notes`), never a break (8/28/26; a compliance entry rejects picks
    and deletes pool branches, which is the exact bug the change removes)."""
    if not gate.get("has_contract"):
        return []
    names = {_strat_norm(str(p)) for p in roster}
    out = []
    hit_fade = [gate["fade"][n] for n in names & set(gate.get("fade") or {})]
    for nm, verdict in hit_fade:
        out.append(f"carries {nm} — the strategy calls him "
                   f"{'LEAN FADE' if verdict == 'lean_fade' else 'FADE'}")
    if "leverage" not in relaxed and gate.get("leverage"):
        if not (names & set(gate["leverage"])):
            out.append("carries no driver/player from the strategy's leverage "
                       "list (every lineup needs one)")
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
    """The SOFT strategy costs this roster carries — underweight calls. These
    never reject a pick or remove a pool row; they are shown as ⚠ so the cost
    of a soft call is visible wherever the lineup appears."""
    if not gate.get("has_contract"):
        return []
    names = {_strat_norm(str(p)) for p in roster}
    return [f"carries {gate['underweight'][n]} — an UNDERWEIGHT call (less "
            "than the crowd, never zero; a carrier must earn its seat on "
            "sim numbers)"
            for n in sorted(names & set(gate.get("underweight") or {}))]


def eligible_indexes(pool: dict, gate: dict,
                     min_rows: int = _GATE_MIN_ROWS) -> dict:
    """Which pool rows the slate strategy actually allows.

    Returns `{"allowed": set[int], "relaxed": [rule], "full": int, "total": int}`.
    If the full gate leaves fewer than `min_rows` lineups, rules are dropped one
    at a time in `_RELAX_ORDER` and every drop is REPORTED — the picker and the
    app both say so out loud rather than quietly loosening the strategy."""
    rosters = pool.get("rosters") or []
    if not gate.get("has_contract"):
        return {"allowed": set(range(len(rosters))), "relaxed": [],
                "full": len(rosters), "total": len(rosters)}

    def _pass(relaxed):
        return {i for i, r in enumerate(rosters) if not compliance(r, gate, relaxed)}

    allowed = _pass(())
    full = len(allowed)
    relaxed: list = []
    for rule in _RELAX_ORDER:
        if len(allowed) >= min_rows:
            break
        relaxed.append(rule)
        allowed = _pass(tuple(relaxed))
    return {"allowed": allowed, "relaxed": relaxed, "full": full,
            "total": len(rosters)}


def gate_summary(gate: dict, elig: dict, pool: dict | None = None) -> str:
    """One plain-language block naming the rules every slice row satisfies —
    rendered into the digest Claude reads and into the app. When `pool` is
    given, each rule is PRICED: how many pooled lineups it alone removes, and
    how many carry each underweight name — so the cost of every call is
    visible before the pick (the 8/23 lesson: an unpriced soft call silently
    deleted the branch holding the Clinch winner)."""
    if not gate.get("has_contract"):
        return ("No slate strategy contract was found, so no strategy rules "
                "could be enforced on this table.")

    rosters = (pool or {}).get("rosters") or []
    norms = [{_strat_norm(str(p)) for p in r} for r in rosters]

    def _price(rule: str) -> str:
        """' — removes N of the M pooled lineups' for one hard rule alone."""
        if not rosters:
            return ""
        others = tuple(r for r in ("leverage", "core", "chalk_pair")
                       if r != rule) + (("fade",) if rule != "fade" else ())
        n = sum(1 for r in rosters if compliance(r, gate, relaxed=others))
        return f" — removes {n:,} of the {len(rosters):,} pooled lineups"

    rules = []
    if gate.get("fade"):
        rules.append("no player the strategy called FADE or LEAN FADE ("
                     + ", ".join(sorted(nm for nm, _v in gate["fade"].values()))
                     + ")" + _price("fade"))
    if gate.get("leverage") and "leverage" not in elig.get("relaxed", []):
        rules.append("at least one player off the strategy's leverage list"
                     + _price("leverage"))
    if gate.get("core") and "core" not in elig.get("relaxed", []):
        rules.append(f"at least {min(2, len(gate['core']))} Core-tier players "
                     "(the strategy's anchors)" + _price("core"))
    if len(gate.get("chalk_pair") or []) == 2 \
            and "chalk_pair" not in elig.get("relaxed", []):
        rules.append(f"never both {gate['chalk_pair'][0]} and "
                     f"{gate['chalk_pair'][1]} (the most duplicated pair)"
                     + _price("chalk_pair"))
    lines = ["Every lineup in the table below ALREADY follows the slate "
             "strategy's hard rules. The app removed the ones that did not:"]
    lines += [f"- {r}" for r in rules]
    lines.append(f"\n{elig.get('full', 0):,} of {elig.get('total', 0):,} pooled "
                 "lineups pass the full strategy gate.")
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
    if elig.get("relaxed"):
        lines.append("⚠️ Too few lineups passed, so these rules had to be "
                     "dropped to fill the table: "
                     + ", ".join(elig["relaxed"])
                     + ". Prefer rows that still honor them.")
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


def candidate_slice(pool: dict, contest: dict, k: int = _SLICE_CAP,
                    strategy: dict | None = None,
                    taken: dict | set | None = None,
                    allowed: set | None = None) -> list[dict]:
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

    `allowed` (from `eligible_indexes`) is the STRATEGY GATE: only lineups that
    already follow the slate strategy may enter the slice. Rows outside it are
    invisible to every angle below, so no sim score can promote a lineup the
    strategy ruled out."""
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

    _add(_top_idx(top1, 30, universe=universe))
    _add(_top_idx(win, 30, universe=universe))
    _add(_top_idx(cash, 20, universe=universe))
    _add(_top_idx(roi, 20, universe=universe))
    _add(_top_idx(proj, 20, universe=universe))
    # Standouts within the top quartile by this contest's top1: the
    # lowest-owned (leverage) and, when dupe data exists, least-duplicated.
    # These carry reserved seats through the cap below — they were added for
    # their angle, not their blend score, and the blend must not evict them.
    standouts: set = set()
    q_list = sorted(_top_idx(top1, max(1, u // 4), universe=universe))
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
        top_half = set(_top_idx(top1, max(1, u // 2), universe=universe))
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
                         key=lambda i: (-len(strat_hits[i]), -(top1[i] or 0), i))
            _add(cov[:20])
            standouts.update(cov[:20])

    # Cap by blend score (small fields lean on win% — plays like SE), with the
    # leverage/low-dupe standouts guaranteed to survive the cut.
    t1n, wn, cn = _norm(top1), _norm(win), _norm(cash)
    field = int(contest.get("field_size") or 0)
    if field and field < _PLAYS_LIKE_SE_FIELD:
        blend = [0.4 * t1n[i] + 0.4 * wn[i] + 0.2 * cn[i] for i in range(n)]
    else:
        blend = [0.5 * t1n[i] + 0.3 * wn[i] + 0.2 * cn[i] for i in range(n)]
    if len(chosen) > k:
        keep = [i for i in chosen if i in standouts]
        rest = [i for i in chosen if i not in standouts]
        rest.sort(key=lambda i: (-blend[i], i))
        chosen = keep + rest[:max(0, k - len(keep))]
    chosen.sort(key=lambda i: (-blend[i], i))

    def _val(arr, i, nd=2):
        v = arr[i] if arr and i < len(arr) else None
        return round(float(v), nd) if v is not None else None

    out = []
    for i in chosen:
        names = [str(x) for x in rosters[i]]
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
            "strategy": ", ".join(strat_hits[i]) if strat_hits.get(i) else None,
        })
    return out


def slice_digest_md(slug: str, label: str, contest: dict, declared: dict | None,
                    rows: list[dict], ownership: dict,
                    gate_md: str | None = None) -> str:
    """The candidate table the claude pass reads and picks ids from."""
    shape = (declared or {}).get("payout_shape") or "not declared"
    my = contest.get("my_entries")
    lines = [
        f"# Candidate lineups — {label}",
        f"Contest: field {int(contest.get('field_size') or 0):,} entries · "
        f"${contest.get('entry_fee')} entry · payout shape {shape} · "
        f"you are entering {my} lineup(s).",
        "Every lineup below was built and simmed by the Sim tool. "
        "Pick ONLY from this table, by id.",
        "",
    ]
    if gate_md:
        lines += ["## The strategy gate", "", gate_md, ""]
    lines += [
        "| id | salary | proj | avg own% | win% | top1% | cash% | roi% | dupes | strategy | players |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        players = ", ".join(
            f"{nm} ({ownership.get(nm)}%)" if ownership.get(nm) is not None else nm
            for nm in r["roster"])
        lines.append(
            f"| {r['index']} | {r.get('salary')} | {r.get('proj')} | "
            f"{r.get('avg_own')} | {r.get('win_pct')} | {r.get('top1_pct')} | "
            f"{r.get('cash_pct')} | {r.get('roi_pct')} | "
            f"{r.get('exp_dupes') if r.get('exp_dupes') is not None else '—'} | "
            f"{r.get('strategy') or '—'} | "
            f"{players} |")
    lines.append("")
    lines.append("The `strategy` column names the leverage-list players this "
                 "lineup carries — the strategy asked for those, so those rows "
                 "are here for their thesis, not just their sim numbers. A ⚠ "
                 "entry is the opposite: a player the strategy called "
                 "UNDERWEIGHT (less than the crowd, never zero). Those rows "
                 "are allowed, but the ⚠ is a COST — pick one only when its "
                 "sim edge over the clean rows is real, and never put the "
                 "same underweight player in every entry of a multi-entry "
                 "contest.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Pick parsing + validation — a selection can choose, never invent
# ---------------------------------------------------------------------------

def _strip_own(cell: str) -> list[str]:
    """Player names from a table cell, ownership parentheticals removed."""
    return [re.sub(r"\s*\([^)]*\)\s*$", "", p).strip()
            for p in str(cell).split(",") if p.strip()]


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
        broken = compliance(srow["roster"], gate or {}, relaxed) if gate else []
        if broken:
            errors.append(f"id {rid} does not follow the slate strategy — it "
                          + "; ".join(broken) + ".")
            continue
        seen_rosters[rkey] = rid
        picks.append({"index": rid, "roster_key": rkey})

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
        uw = gate.get("underweight") or {}
        if uw:
            rosters_n = [{_strat_norm(str(p)) for p in by_index[pk["index"]]["roster"]}
                         for pk in picks]
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

    why = None
    m = re.search(r"^\*\*Why[^\n]*\*\*:?\s*(.*?)(?=\n\s*\n|\Z)",
                  md or "", re.M | re.S)
    if m:
        why = " ".join(m.group(1).split()) or None

    return {"picks": picks if not errors else [], "why": why,
            "errors": errors, "warnings": warnings if not errors else []}
