"""NFL Classic rulebook — the ONE definition of positions, games, stacks and
correlation loadings for DK NFL Classic (main slate), shared VERBATIM by the
Sim and the Analyzer.

Rules for this file (9/12/26, user directive: both tools must see the same
players, games and stacks):
  * Pure Python only — no pandas, no numpy, no `src` imports. The Analyzer
    keeps a byte-identical copy at src/nfl_classic_defs.py and its
    cross-repo parity test compares the two files' TEXT, so any edit here
    must be copied there (and vice versa) or the test fails by name.
  * Every Sim call site (builder, sim, field, export) and every Analyzer
    call site (counterfactual, autopsy) imports from here — never a private
    alias table or an inline '@'-strip again.

Stack definition (user decision 9/12/26): a QB's STACK MATE is ANY non-DST
teammate (RB, WR or TE); a BRING-BACK is ANY non-DST player from the
opposing team. ETR's published field-composition rates count pass-catchers
only, so a rate quoted from ETR is not directly comparable to one computed
here — the framework says so where it cites them.
"""
from __future__ import annotations

import re

# ---- Roster --------------------------------------------------------------
CLASSIC_SLOTS = ("QB", "RB", "RB", "WR", "WR", "WR", "TE", "FLEX", "DST")
FLEX_ELIGIBLE = ("RB", "WR", "TE")
CLASSIC_SIZE = len(CLASSIC_SLOTS)
CLASSIC_MIN_GAMES = 2
BASE_QUOTA = {"QB": 1, "RB": 2, "WR": 3, "TE": 1, "DST": 1}
SALARY_CAP = 50_000

# ---- Positions -----------------------------------------------------------
# Every spelling a vendor / DK export has used for the defense and the
# kicker, folded to the DK slot name.
POSITION_ALIASES = {
    "D": "DST", "DEF": "DST", "D/ST": "DST", "DS": "DST", "DEF/ST": "DST",
    "DST/D": "DST", "PK": "K",
}
KNOWN_POSITIONS = ("QB", "RB", "WR", "TE", "DST", "K")

# ---- Stacks --------------------------------------------------------------
STACK_MATE_POSITIONS = ("RB", "WR", "TE")   # a QB's teammate that counts as a stack
BRINGBACK_POSITIONS = ("RB", "WR", "TE")    # an opponent that counts as a bring-back
# The FIELD GENERATOR's stacking tilt boosts pass-catchers only: its
# multipliers were calibrated 9/12/26 against ETR's published field mix,
# which counts pass-catchers. This is how the modeled field is DRAWN; what
# counts as a stack when a lineup is READ is STACK_MATE_POSITIONS above.
FIELD_TILT_POSITIONS = ("WR", "TE")
STACK_ANCHORS = ("QB", "RB", "WR", "TE", "DST")
STACK_PARTNERS = ("QB", "RB", "WR", "TE", "DST")
STACK_QUANTS = ("At Least", "At Most", "Exactly")
STACK_RELATIONS = ("Same Team", "Opponent")

# ---- Correlation (factor loadings, fractions of each player's own stddev) --
# Implied pairwise correlations (loading products):
#   QB ↔ opp QB          0.62 × 0.62               ≈ +0.38  (target +0.3..0.5)
#   QB ↔ own WR/TE       0.62×0.40 + 0.45×0.25     ≈ +0.36  (target +0.3..0.4)
#   QB ↔ opp DST         0.62×(−0.20) + 0.45×(−0.50) ≈ −0.35 (target −0.3..−0.45)
NFL_GAME_LOADING = {          # loading on the shared game-environment shock
    "QB": 0.62, "WR": 0.45, "TE": 0.45, "RB": 0.30, "K": 0.30, "DST": -0.20,
}
NFL_TEAM_LOADING = {          # loading on the player's OWN team's offense shock
    "QB": 0.45, "WR": 0.25, "TE": 0.25, "RB": 0.25, "K": 0.15, "DST": 0.0,
}
NFL_DST_OPP_LOADING = -0.50   # DST loading on the OPPOSING team's offense shock
NFL_LOADING_FALLBACK = "RB"   # an unknown position (FB…) gets the RB profile

_BLANKS = ("", "NAN", "NONE", "NULL")
_OPP_PREFIX = re.compile(r"^(?:@|VS\.?|V\.?|AT(?=\s))\s*")


def _text(value) -> str:
    """Upper-cased, stripped text; None / NaN / blank → ''."""
    if value is None:
        return ""
    try:
        if value != value:  # NaN without numpy/pandas
            return ""
    except Exception:  # noqa: BLE001 — exotic objects compare oddly
        pass
    s = str(value).strip().upper()
    return "" if s in _BLANKS else s


def normalize_position(value) -> str:
    """DK position with every defense / kicker spelling folded ('' when blank)."""
    s = _text(value)
    return POSITION_ALIASES.get(s, s)


def normalize_team(value) -> str:
    """Team code, upper-cased ('' when blank)."""
    return _text(value)


def normalize_opponent(value) -> str:
    """Opponent code with the road / home markers stripped: '@KC', 'VS KC',
    'vs. KC', 'AT KC' → 'KC'. '' when blank."""
    s = _text(value)
    if not s:
        return ""
    s = _OPP_PREFIX.sub("", s).strip()
    return "" if s in _BLANKS else s


def game_key(team, opponent) -> tuple:
    """Game identity: the sorted (team, opponent) pair. Either side blank →
    (team,) — a one-sided key that never equals a real game."""
    t = normalize_team(team)
    o = normalize_opponent(opponent)
    if not o or not t or o == t:
        return (t,) if t else (o,)
    return tuple(sorted((t, o)))


def roster_legal(positions) -> bool:
    """True when a 9-position multiset fills QB, RB, RB, WR, WR, WR, TE,
    FLEX (RB/WR/TE), DST."""
    pos = [normalize_position(p) for p in positions]
    if len(pos) != CLASSIC_SIZE:
        return False
    counts: dict = {}
    for p in pos:
        counts[p] = counts.get(p, 0) + 1
    if any(counts.get(k, 0) < v for k, v in BASE_QUOTA.items()):
        return False
    if counts.get("QB", 0) != 1 or counts.get("DST", 0) != 1:
        return False
    if any(p not in BASE_QUOTA for p in counts):
        return False
    return sum(counts.get(k, 0) for k in FLEX_ELIGIBLE) == CLASSIC_SIZE - 2


def stack_shape(positions, teams, opponents) -> dict:
    """The stack read of ONE lineup (any order). Returns
      {"qb_team": str, "mates": int, "bringback": int, "dst_vs_qb": bool,
       "games": int, "shape": "naked" | "stack1" | "stack2" | "stack3plus"}
    mates = non-DST teammates of the QB (STACK_MATE_POSITIONS);
    bringback = non-DST players on the QB's opponent (BRINGBACK_POSITIONS);
    dst_vs_qb = the lineup's DST faces its own QB. No QB → mates/bringback 0."""
    pos = [normalize_position(p) for p in positions]
    tm = [normalize_team(t) for t in teams]
    op = [normalize_opponent(o) for o in opponents]
    keys = {game_key(t, o) for t, o in zip(tm, op)}
    qb = next((i for i, p in enumerate(pos) if p == "QB"), None)
    if qb is None:
        return {"qb_team": "", "mates": 0, "bringback": 0, "dst_vs_qb": False,
                "games": len(keys), "shape": "naked"}
    qb_team, qb_opp = tm[qb], op[qb]
    mates = sum(1 for i, p in enumerate(pos)
                if i != qb and p in STACK_MATE_POSITIONS and tm[i] == qb_team and qb_team)
    bring = sum(1 for i, p in enumerate(pos)
                if p in BRINGBACK_POSITIONS and qb_opp and tm[i] == qb_opp)
    dst_vs = any(p == "DST" and qb_opp and tm[i] == qb_opp for i, p in enumerate(pos))
    shape = "naked" if mates == 0 else "stack1" if mates == 1 else "stack2" if mates == 2 else "stack3plus"
    return {"qb_team": qb_team, "mates": mates, "bringback": bring,
            "dst_vs_qb": bool(dst_vs), "games": len(keys), "shape": shape}
