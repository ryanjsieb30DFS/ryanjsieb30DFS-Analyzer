"""Landscape computations: chalk tiers, leverage, anchor-equivalence, plus
golf-GPP breakdowns (mispricing, value-by-tier, tee-wave, boom/bust, edge flags)
that surface non-obvious edges from a single vendor's projection pool."""
from __future__ import annotations

import pandas as pd


def has_real_ceiling(df: pd.DataFrame) -> bool:
    """True only when the vendor shipped a real `ceiling` column (golf: ETR/Ship It;
    NASCAR (DailyFan) and names-only vendors ship none — we never
    fabricate one, so ceiling-based views must gate on this."""
    return "ceiling" in df.columns and pd.to_numeric(df["ceiling"], errors="coerce").notna().any()


def _upside(df: pd.DataFrame) -> pd.Series:
    """Per-player ceiling = the vendor's REAL `ceiling` if present, else just
    `proj_points`. We do NOT fabricate a ceiling from a derived stddev — a flat
    30%-of-proj guess is identical for every player and carries zero information.
    Callers must gate ceiling-based panels on `has_real_ceiling(df)`."""
    if has_real_ceiling(df):
        ceil = pd.to_numeric(df["ceiling"], errors="coerce")
        return ceil.fillna(df["proj_points"])
    return df["proj_points"]


def _own_tier(o: float) -> str:
    """Ownership tier label for one player (the chalk-tier bins)."""
    if o >= 25: return "Mega-chalk (25%+)"
    if o >= 15: return "Chalk (15-25%)"
    if o >= 8:  return "Mid-own (8-15%)"
    if o >= 3:  return "Low-own (3-8%)"
    return "Punt (<3%)"


def chalk_tiers(projections: pd.DataFrame) -> pd.DataFrame:
    """Bin players by ownership tier."""
    df = projections.copy()
    own = df["ownership"].fillna(0)
    df["tier"] = own.apply(_own_tier)
    return df


def chalk_summary(projections: pd.DataFrame) -> pd.DataFrame:
    """Counts and avg proj/salary per tier."""
    df = chalk_tiers(projections)
    aggs = dict(
        n=("name", "count"),
        avg_proj=("proj_points", "mean"),
        avg_salary=("salary", "mean"),
        avg_own=("ownership", "mean"),
    )
    t10 = top10_count_column(df)
    if t10:  # ETR digest 9/12/26 Section E item 1 — only when the vendor ships it
        df["top10_count"] = pd.to_numeric(df[t10], errors="coerce")
        aggs["top10_count"] = ("top10_count", "sum")
    grp = df.groupby("tier").agg(**aggs).round(2).reset_index()
    order = ["Mega-chalk (25%+)", "Chalk (15-25%)", "Mid-own (8-15%)", "Low-own (3-8%)", "Punt (<3%)"]
    grp["tier"] = pd.Categorical(grp["tier"], categories=order, ordered=True)
    return grp.sort_values("tier").reset_index(drop=True)


def leverage_table(projections: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Leverage = upside / (ownership + 1). `upside` is the real ceiling when the
    vendor ships one; otherwise upside == proj_points and the redundant `upside`
    column is dropped (leverage_score is then proj ÷ (own+1))."""
    df = projections.copy()
    real_ceil = has_real_ceiling(df)
    df["upside"] = _upside(df)
    df["leverage_score"] = df["upside"] / (df["ownership"].fillna(0) + 1)
    cols = ["name", "salary", "proj_points"]
    if real_ceil:
        cols.append("upside")
    cols.append("ownership")
    if "current_score" in df.columns:  # golf RD4 SD live leaderboard position
        cols.append("current_score")
    t10 = top10_count_column(df)
    if t10:  # vendor-projected top-10 finishes (Section E item 1); absent → skipped silently
        df["top10_count"] = pd.to_numeric(df[t10], errors="coerce")
        cols.append("top10_count")
    cols.append("leverage_score")
    return df.sort_values("leverage_score", ascending=False).head(top_n)[cols].reset_index(drop=True)


def leverage_candidates(projections: pd.DataFrame, own_max: float = 10.0,
                        top_n: int = 12) -> pd.DataFrame:
    """The sub-`own_max`%-owned, high-ceiling plays the strategy MUST address.

    Ranked by ceiling (`_upside`, which degrades to proj_points when no vendor
    ships ceiling) descending. These are the coverage-guard candidates: each must
    be an explicit PLAY/PASS in the strategy + player pool — the Kaan Ofli leak
    was one of these going unmentioned. Columns: name, salary, ownership,
    proj_points, upside."""
    df = projections.copy()
    if df.empty or "ownership" not in df.columns or "proj_points" not in df.columns:
        return pd.DataFrame()
    df["upside"] = _upside(df)
    own = pd.to_numeric(df["ownership"], errors="coerce")
    df = df[own.notna() & (own < own_max)]
    if df.empty:
        return pd.DataFrame()
    cols = [c for c in ["name", "salary", "ownership", "proj_points", "upside"] if c in df.columns]
    return df.sort_values("upside", ascending=False).head(top_n)[cols].reset_index(drop=True)


def chalky_combos(projections: pd.DataFrame, min_own: float = 15.0,
                  top_pairs: int = 6) -> list[dict]:
    """THIS slate's likely-duplicated chalk PAIRS — the combinations the field
    will most often roster together, estimated from projected ownership
    (co-occurrence ≈ own_a × own_b under independence; a floor, since real
    fields correlate their chalk). In a small-field GPP, sharing one of these
    pairs means sharing a big slice of the field's lineups — where uniqueness
    quietly dies. Descriptive duplication-watch data for the strategy; never a
    fade command. Complements field_tendencies' HISTORICAL recurring pairs
    (what the field actually paired in your past contests) with a forward
    read from this slate's own numbers."""
    if projections is None or projections.empty or "ownership" not in projections.columns \
            or "name" not in projections.columns:
        return []
    df = projections.copy()
    own = pd.to_numeric(df["ownership"], errors="coerce")
    chalk = df[own.notna() & (own >= min_own)].copy()
    chalk["__own"] = own[chalk.index]
    chalk = chalk.sort_values("__own", ascending=False).head(10)
    rows = list(zip(chalk["name"].astype(str), chalk["__own"].astype(float)))
    combos = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            (na, oa), (nb, ob) = rows[i], rows[j]
            joint = (oa / 100.0) * (ob / 100.0) * 100.0
            combos.append({"players": [na, nb], "own_a": round(oa, 1),
                           "own_b": round(ob, 1), "joint_pct": round(joint, 1)})
    combos.sort(key=lambda c: -c["joint_pct"])
    return combos[:top_pairs]


def uncovered_candidates(text: str, candidates: pd.DataFrame) -> list[str]:
    """Names from `candidates` NOT mentioned in `text` (case-insensitive, by full
    name OR last-name token). Powers the app's coverage-gap warning."""
    if candidates is None or candidates.empty or not text or "name" not in candidates.columns:
        return []
    low = text.lower()
    missing: list[str] = []
    for name in candidates["name"].astype(str):
        full = name.strip().lower()
        if not full:
            continue
        if full in low:
            continue
        last = full.split()[-1]
        if len(last) >= 4 and last in low:
            continue
        missing.append(name)
    return missing


def anchor_equivalence_check(projections: pd.DataFrame, own_window: float = 5.0) -> list[dict]:
    """Find chalk-tier anchor pairs at similar own%. Returns groups of equivalent anchors.

    The leak: if 2+ chalk-tier anchors at similar own, >=1 lineup must run the alternative.
    """
    df = projections.copy()
    chalk = df[df["ownership"].fillna(0) >= 15].sort_values("ownership", ascending=False)
    if len(chalk) < 2:
        return []

    groups = []
    used = set()
    for i, a in chalk.iterrows():
        if i in used:
            continue
        peers = chalk[
            (chalk.index != i)
            & (~chalk.index.isin(used))
            & ((chalk["ownership"] - a["ownership"]).abs() <= own_window)
        ]
        if len(peers) >= 1:
            members = [a.to_dict()] + peers.to_dict("records")
            used.add(i)
            used.update(peers.index.tolist())
            groups.append({
                "players": [m["name"] for m in members],
                "own_range": (
                    min(m["ownership"] for m in members),
                    max(m["ownership"] for m in members),
                ),
                "rule": "At least one lineup must run the alternative anchor.",
            })
    return groups


# ----------------------------------------------------------------------------
# Golf-GPP breakdowns: surface what a sortable table won't show at a glance.
# ----------------------------------------------------------------------------

def mispricing_table(projections: pd.DataFrame, top_n: int = 12,
                     min_overowned_own: float = 10.0) -> dict[str, pd.DataFrame]:
    """Field blind spots: ceiling rank vs ownership rank.

    edge = own_rank - upside_rank, where rank 1 = best (highest ceiling / highest own).
    Positive edge => UNDEROWNED relative to ceiling (leverage the field is sleeping on).
    Negative edge => OVEROWNED relative to ceiling (chalk paying up in own for less upside).
    The "overowned" side is restricted to genuinely-owned players (>= min_overowned_own%) so
    it surfaces real chalk to fade, not low-owned low-ceiling scrubs.
    Returns {"underowned": df, "overowned": df}.
    """
    df = projections.copy()
    df["upside"] = _upside(df)
    own = df["ownership"].fillna(0)
    # rank: 1 = best. method='min' so ties share the top rank.
    df["upside_rank"] = df["upside"].rank(ascending=False, method="min")
    df["own_rank"] = own.rank(ascending=False, method="min")
    df["edge"] = (df["own_rank"] - df["upside_rank"]).round(0).astype(int)
    cols = ["name", "salary", "proj_points", "upside", "ownership", "edge"]
    cols = [c for c in cols if c in df.columns]
    under = df.sort_values("edge", ascending=False).head(top_n)[cols].reset_index(drop=True)
    over_pool = df[own >= min_overowned_own]
    over = over_pool.sort_values("edge", ascending=True).head(top_n)[cols].reset_index(drop=True)
    return {"underowned": under, "overowned": over}


def _salary_tier(sal: float) -> str:
    if sal >= 10000: return "Studs ($10k+)"
    if sal >= 8000:  return "Upper-mid ($8-10k)"
    if sal >= 7000:  return "Mid ($7-8k)"
    if sal >= 6000:  return "Value ($6-7k)"
    return "Punt (<$6k)"


_TIER_ORDER = ["Studs ($10k+)", "Upper-mid ($8-10k)", "Mid ($7-8k)", "Value ($6-7k)", "Punt (<$6k)"]


def value_by_tier(projections: pd.DataFrame) -> pd.DataFrame:
    """Per salary tier: the best ceiling-per-$1k and proj-per-$1k leader (where to spend /
    cheap leverage the field under-weights)."""
    df = projections.copy()
    real_ceil = has_real_ceiling(df)
    # $0/blank salary = withdrawn or unrosterable (ETR ships WDs at $0) — drop, else
    # they poison the per-$1k math (and pd.NA in an int column crashes .round()).
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df = df[df["salary"] > 0].copy()
    df["upside"] = _upside(df)
    df["ceil_per_1k"] = (df["upside"] / df["salary"] * 1000).round(2)
    df["proj_per_1k"] = (df["proj_points"] / df["salary"] * 1000).round(2)
    df["tier"] = df["salary"].apply(_salary_tier)
    rows = []
    for tier in _TIER_ORDER:
        sub = df[df["tier"] == tier]
        if sub.empty:
            continue
        best_proj = sub.loc[sub["proj_per_1k"].idxmax()]
        row = {"tier": tier, "n": len(sub)}
        if real_ceil:  # only show a ceiling column when it's real, not fabricated
            best_ceil = sub.loc[sub["ceil_per_1k"].idxmax()]
            row["best ceiling/$1k"] = f"{best_ceil['name']} ({best_ceil['ceil_per_1k']})"
        row["best proj/$1k"] = f"{best_proj['name']} ({best_proj['proj_per_1k']})"
        row["avg own%"] = round(float(sub["ownership"].fillna(0).mean()), 1)
        rows.append(row)
    return pd.DataFrame(rows)


def _wave(tee) -> str:
    """Map an 'HH:MM' tee time to AM (<12:00) or PM. '' if unparseable."""
    if not isinstance(tee, str):
        return ""
    s = tee.strip()
    if not s or s.lower() == "nan":
        return ""
    try:
        return "AM" if int(s.split(":")[0]) < 12 else "PM"
    except (ValueError, IndexError):
        return ""


def tee_wave_split(projections: pd.DataFrame) -> pd.DataFrame:
    """AM vs PM wave: player count, summed ownership, avg ceiling, # sub-5% leverage pieces.
    Empty frame if 'tee_time' is missing (caller shows a note)."""
    if "tee_time" not in projections.columns:
        return pd.DataFrame()
    df = projections.copy()
    df["wave"] = df["tee_time"].apply(_wave)
    df = df[df["wave"].isin(["AM", "PM"])]
    if df.empty:
        return pd.DataFrame()
    df["upside"] = _upside(df)
    rows = []
    for wave in ["AM", "PM"]:
        sub = df[df["wave"] == wave]
        if sub.empty:
            continue
        rows.append({
            "wave": wave,
            "players": len(sub),
            "total own%": round(float(sub["ownership"].fillna(0).sum()), 1),
            "avg ceiling": round(float(sub["upside"].mean()), 1),
            "sub-5% leverage": int((sub["ownership"].fillna(0) < 5).sum()),
        })
    return pd.DataFrame(rows)


def volatility_table(projections: pd.DataFrame, top_n: int = 10) -> dict[str, pd.DataFrame]:
    """Boom/bust shape. boom_pct = (ceiling - proj)/proj. Returns:
    - "boom": highest ceiling-volatility (tournament upside), and
    - "fragile_chalk": high-owned (>=15%) players with the LOWEST boom_pct (paying own for a
      capped ceiling — the quiet fade)."""
    df = projections.copy()
    df["upside"] = _upside(df)
    proj = pd.to_numeric(df["proj_points"], errors="coerce").replace(0, float("nan"))
    df["boom_pct"] = ((df["upside"] - df["proj_points"]) / proj * 100).round(1)
    keep = ["name", "salary", "proj_points", "upside", "ownership", "boom_pct"]
    if "make_cut_odds" in df.columns:
        keep.append("make_cut_odds")
    keep = [c for c in keep if c in df.columns]
    boom = df.sort_values("boom_pct", ascending=False).head(top_n)[keep].reset_index(drop=True)
    chalk = df[df["ownership"].fillna(0) >= 15]
    fragile = chalk.sort_values("boom_pct", ascending=True).head(top_n)[keep].reset_index(drop=True)
    return {"boom": boom, "fragile_chalk": fragile}


def breakdown_flags(projections: pd.DataFrame) -> list[str]:
    """Synthesize an 'Edges to notice' bullet list from the breakdowns above."""
    flags: list[str] = []
    df = projections.copy()
    own = df["ownership"].fillna(0)

    # Top mispriced (underowned vs ceiling) — only when there's a REAL ceiling.
    if has_real_ceiling(df):
        _mp = mispricing_table(df, top_n=3)
        mis = _mp["underowned"]
        if not mis.empty:
            names = ", ".join(f"{r['name']} (+{int(r['edge'])})" for _, r in mis.iterrows() if r["edge"] > 0)
            if names:
                flags.append(f"**Most underowned vs ceiling** (field blind spots): {names}")
        over = _mp["overowned"]
        if not over.empty:
            names = ", ".join(f"{r['name']} ({int(r['edge'])})" for _, r in over.iterrows() if r["edge"] < 0)
            if names:
                flags.append(f"**Overowned vs ceiling** (chalk paying up for less upside): {names}")

    # Anchor-equivalence pairs (only tight, actionable groups of 2-4)
    for g in anchor_equivalence_check(df):
        if not (2 <= len(g["players"]) <= 4):
            continue
        lo, hi = g["own_range"]
        flags.append(
            f"**Anchor-equivalence**: {', '.join(g['players'])} at {lo:.0f}-{hi:.0f}% own — "
            "at least one lineup must run the alternative anchor."
        )

    # Chalk concentration (top-6 owned = one lineup's worth)
    conc = float(own.nlargest(min(6, len(df))).sum())
    if conc >= 110:
        flags.append(f"**Chalk concentration**: top-6 owned sum to {conc:.0f}% — the field is piling up; leverage the field's blind side.")

    # Tee-wave imbalance — compare AVG ownership per player (fair across uneven wave sizes)
    waves = tee_wave_split(df)
    if not waves.empty and len(waves) == 2:
        w = waves.set_index("wave")
        am = w.loc["AM", "total own%"] / max(int(w.loc["AM", "players"]), 1)
        pm = w.loc["PM", "total own%"] / max(int(w.loc["PM", "players"]), 1)
        if max(am, pm) > 0 and abs(am - pm) / max(am, pm) >= 0.25:
            heavy = "AM" if am > pm else "PM"
            light = "PM" if heavy == "AM" else "AM"
            flags.append(
                f"**Tee-wave tilt**: the field's ownership/player leans {heavy} "
                f"({am:.1f}% vs {pm:.1f}% avg) — the {light} wave is comparatively underowned."
            )

    # Leverage availability
    if (own < 5).sum() == 0:
        flags.append("**No sub-5% leverage** exists in this pool — every play is at least lightly owned.")
    n_mega = int((own >= 30).sum())
    if n_mega >= 3:
        flags.append(f"**{n_mega} players ≥30% own** — chalk-heavy slate; differentiation comes from the lineup *combination*, not single fades.")

    if not flags:
        flags.append("No standout structural edges — slate looks balanced; lean on ceiling/leverage board above.")
    return flags


# ----------------------------------------------------------------------------
# NFL Classic report-only reads (ETR NFL Classic digest 9/12/26, Section E).
# Everything here is information for the Projections-tab Breakdown and the
# Grade tab: never a rule, never a warning, never a letter-grade cost.
# ----------------------------------------------------------------------------

_TOP10_COLUMN_KEYS = {"top10", "top_10", "top10_count", "top_10_count", "top10s",
                      "top_10s", "top10_finishes", "top_10_finishes"}


def top10_count_column(df: pd.DataFrame) -> str | None:
    """The vendor column carrying a raw count of projected top-10 finishes, or
    None when the vendor ships none (ETR NFL Classic ships none — the panel
    then skips silently). Matched on the normalized header, never fabricated."""
    if df is None:
        return None
    for c in df.columns:
        key = str(c).strip().lower().replace(" ", "_").replace("-", "_")
        if key in _TOP10_COLUMN_KEYS:
            return c
    return None


def chalk_combo_counts(projections: pd.DataFrame, field_size: int | None,
                       min_own: float = 15.0, top_pairs: int = 6) -> list[dict]:
    """`chalky_combos` plus the raw count of lineups expected to carry each
    pair in the DECLARED field: own_a × own_b × field size — the same
    independence math the bundle and the strategy prose cite ("~461 lineups of
    2,450"). ETR reads chalk combos in lineups, not percentages (48 vs 80
    lineups is a different contest). `expected_lineups` is None with no
    declared field. A floor, since real fields correlate their chalk."""
    combos = chalky_combos(projections, min_own=min_own, top_pairs=top_pairs)
    fs = int(field_size) if field_size else 0
    for c in combos:
        c["field_size"] = fs or None
        c["expected_lineups"] = int(round(c["joint_pct"] / 100.0 * fs)) if fs else None
    return combos


def chalk_combo_counts_md(combos: list[dict]) -> str:
    """Plain-language lines for the chalk-pair lineup counts."""
    if not combos:
        return "_No chalk pairs yet — nobody in this file is projected at 15% ownership or more._"
    out = []
    for c in combos:
        line = (f"- **{c['players'][0]} + {c['players'][1]}** — {c['own_a']}% × {c['own_b']}% "
                f"≈ {c['joint_pct']}% of lineups")
        if c.get("expected_lineups") is not None:
            line += (f", about **{c['expected_lineups']:,} lineups** of the "
                     f"{c['field_size']:,} in the declared field")
        else:
            line += " (declare a contest in Slate Strategy to see the lineup count)"
        out.append(line)
    return "\n".join(out)


def _scaled_own(projections: pd.DataFrame, k: float) -> pd.DataFrame:
    """Copy of the frame with ownership × k, capped at 100%."""
    df = projections.copy()
    own = pd.to_numeric(df["ownership"], errors="coerce") * k
    df["ownership"] = own.clip(upper=100.0)
    return df


def _top_stacks(projections: pd.DataFrame, top_qbs: int = 4, mates: int = 2) -> list[dict]:
    """The slate's most-owned QB stacks: each of the top `top_qbs` quarterbacks
    by ownership + his `mates` most-owned pass-catching teammates (RB/WR/TE).
    [] when the frame carries no position/team columns."""
    if projections is None or projections.empty:
        return []
    if not {"position", "team", "name", "ownership"} <= set(projections.columns):
        return []
    from src.nfl_classic_defs import STACK_MATE_POSITIONS, normalize_position, normalize_team
    df = projections.copy()
    df["__pos"] = df["position"].map(normalize_position)
    df["__team"] = df["team"].map(normalize_team)
    df["__own"] = pd.to_numeric(df["ownership"], errors="coerce").fillna(0.0)
    qbs = df[df["__pos"] == "QB"].sort_values("__own", ascending=False).head(top_qbs)
    stacks = []
    for _, qb in qbs.iterrows():
        team = qb["__team"]
        if not team:
            continue
        pool = df[(df["__team"] == team) & (df["__pos"].isin(STACK_MATE_POSITIONS))]
        pool = pool.sort_values("__own", ascending=False).head(mates)
        pieces = [(str(qb["name"]), float(qb["__own"]))] + \
                 [(str(r["name"]), float(r["__own"])) for _, r in pool.iterrows()]
        stacks.append({"qb": str(qb["name"]), "team": team, "pieces": pieces,
                       "stack_own": round(sum(o for _, o in pieces), 1)})
    return stacks


def ownership_stress_test(projections: pd.DataFrame, field_size: int | None = None,
                          scales: tuple = (0.8, 1.2), own_max: float = 10.0) -> dict:
    """The framework's THREE ownership checks, recomputed with every ownership
    number scaled ×0.8 and ×1.2 (the real field always lands off the
    projection), reporting which players FLIP:

      stack   — the top QB stacks' correlated pieces; a flip = a piece whose
                ownership tier (the chalk bins) changes under the scale.
      combo   — the chalk pairs and their expected lineup counts at each
                scale; a flip = a pair that enters or leaves the top-pair list.
      diff    — the differentiation pieces (sub-`own_max`% high-ceiling plays);
                a flip = a player who leaves that set at ×1.2 or joins it at ×0.8.

    Report-only. Returns {"scales", "stack", "stack_flips", "combo",
    "combo_flips", "diff_base", "diff_flips"}."""
    empty = {"scales": list(scales), "stack": [], "stack_flips": [], "combo": [],
             "combo_flips": [], "diff_base": [], "diff_flips": []}
    if projections is None or projections.empty or "ownership" not in projections.columns:
        return empty
    res = dict(empty)
    fs = int(field_size) if field_size else 0

    # (a) correlated pieces — tier flips of the top stacks' pieces
    stacks = _top_stacks(projections)
    res["stack"] = stacks
    flips = []
    for stk in stacks:
        for name, own in stk["pieces"]:
            base_t = _own_tier(own)
            for k in scales:
                new_t = _own_tier(min(own * k, 100.0))
                if new_t != base_t:
                    flips.append({"name": name, "stack": stk["qb"], "base_own": round(own, 1),
                                  "scale": k, "scaled_own": round(min(own * k, 100.0), 1),
                                  "from": base_t, "to": new_t})
    res["stack_flips"] = flips

    # (b) chalk combos — lineup counts at each scale + membership flips
    base = chalk_combo_counts(projections, fs)
    base_keys = {tuple(c["players"]) for c in base}
    combo_rows = []
    for c in base:
        row = dict(c)
        row["expected_by_scale"] = {}
        for k in scales:
            pct = min(c["own_a"] * k, 100.0) / 100.0 * min(c["own_b"] * k, 100.0) / 100.0 * 100.0
            row["expected_by_scale"][k] = int(round(pct / 100.0 * fs)) if fs else None
        combo_rows.append(row)
    res["combo"] = combo_rows
    cflips = []
    for k in scales:
        scaled = chalk_combo_counts(_scaled_own(projections, k), fs)
        keys = {tuple(c["players"]) for c in scaled}
        for c in scaled:
            if tuple(c["players"]) not in base_keys:
                cflips.append({"players": c["players"], "scale": k, "change": "enters",
                               "expected_lineups": c["expected_lineups"]})
        for c in base:
            if tuple(c["players"]) not in keys:
                cflips.append({"players": c["players"], "scale": k, "change": "leaves",
                               "expected_lineups": c["expected_lineups"]})
    res["combo_flips"] = cflips

    # (c) differentiation pieces — sub-own_max membership flips
    base_d = leverage_candidates(projections, own_max=own_max)
    res["diff_base"] = list(base_d["name"].astype(str)) if not base_d.empty else []
    # Flips are THRESHOLD crossings only: membership is taken uncapped, so a
    # player pushed out of the top-12 by a reshuffle never reads as a flip.
    n_all = len(projections)
    base_u = leverage_candidates(projections, own_max=own_max, top_n=n_all)
    base_names = list(base_u["name"].astype(str)) if not base_u.empty else []
    own_map = dict(zip(projections["name"].astype(str),
                       pd.to_numeric(projections["ownership"], errors="coerce")))
    dflips = []
    for k in scales:
        sc = leverage_candidates(_scaled_own(projections, k), own_max=own_max, top_n=n_all)
        names = list(sc["name"].astype(str)) if not sc.empty else []
        for n in names:
            if n not in base_names:
                dflips.append({"name": n, "scale": k, "change": "joins",
                               "base_own": round(float(own_map.get(n, 0.0)), 1),
                               "scaled_own": round(min(float(own_map.get(n, 0.0)) * k, 100.0), 1)})
        for n in base_names:
            if n not in names:
                dflips.append({"name": n, "scale": k, "change": "leaves",
                               "base_own": round(float(own_map.get(n, 0.0)), 1),
                               "scaled_own": round(min(float(own_map.get(n, 0.0)) * k, 100.0), 1)})
    res["diff_flips"] = dflips
    return res


def stress_test_md(res: dict) -> str:
    """Plain-language rendering of `ownership_stress_test`."""
    if not res or not (res.get("stack") or res.get("combo") or res.get("diff_base")):
        return ("_Nothing to stress-test yet — this needs ownership plus position and team "
                "columns (the ETR NFL Classic file has them)._")
    lo, hi = min(res["scales"]), max(res["scales"])
    out = [f"Every ownership number was rerun at ×{lo:g} (the field comes in lighter than "
           f"projected) and ×{hi:g} (heavier). A **flip** is a player or pair whose read "
           f"changes under one of those moves — the spots where a small ownership miss "
           f"changes the slate."]
    out.append("**Check 1 — the correlated pieces (the top QB stacks).**")
    for stk in res.get("stack") or []:
        pcs = ", ".join(f"{n} {o:.0f}%" for n, o in stk["pieces"])
        out.append(f"- {stk['qb']} stack ({stk['team']}): {pcs} — {stk['stack_own']:.0f}% "
                   f"of ownership across the pieces; at ×{lo:g} that is "
                   f"{stk['stack_own'] * lo:.0f}%, at ×{hi:g} {min(stk['stack_own'] * hi, 300):.0f}%.")
    if res.get("stack_flips"):
        for f in res["stack_flips"]:
            out.append(f"  - flip: **{f['name']}** ({f['stack']} stack) moves from {f['from']} to "
                       f"{f['to']} at ×{f['scale']:g} ({f['base_own']}% → {f['scaled_own']}%).")
    elif res.get("stack"):
        out.append("  - no stack piece changes ownership tier under either move.")
    out.append("**Check 2 — the chalk combo (lineups sharing the pair).**")
    for c in res.get("combo") or []:
        by = c.get("expected_by_scale") or {}
        if c.get("expected_lineups") is not None:
            out.append(f"- {c['players'][0]} + {c['players'][1]}: about "
                       f"{c['expected_lineups']:,} lineups as projected; {by.get(lo, 0):,} at "
                       f"×{lo:g}, {by.get(hi, 0):,} at ×{hi:g}.")
        else:
            out.append(f"- {c['players'][0]} + {c['players'][1]}: {c['joint_pct']}% of lineups "
                       f"as projected (declare a contest to see lineup counts).")
    if res.get("combo_flips"):
        for f in res["combo_flips"]:
            out.append(f"  - flip: **{f['players'][0]} + {f['players'][1]}** {f['change']} the "
                       f"chalk-pair list at ×{f['scale']:g}.")
    elif res.get("combo"):
        out.append("  - the chalk-pair list holds under both moves.")
    out.append("**Check 3 — the differentiation pieces (the sub-10% high-ceiling plays).**")
    if res.get("diff_base"):
        out.append(f"- As projected: {', '.join(res['diff_base'])}.")
    else:
        out.append("- As projected: nobody is under 10% with a high ceiling.")
    if res.get("diff_flips"):
        for f in res["diff_flips"]:
            verb = "stops being a differentiation piece" if f["change"] == "leaves" \
                else "becomes a differentiation piece"
            out.append(f"  - flip: **{f['name']}** {verb} at ×{f['scale']:g} "
                       f"({f['base_own']}% → {f['scaled_own']}%).")
    else:
        out.append("  - the differentiation list holds under both moves.")
    return "\n".join(out)
