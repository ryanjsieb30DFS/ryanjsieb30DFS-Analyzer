"""Landscape computations: chalk tiers, leverage, anchor-equivalence, plus
golf-GPP breakdowns (mispricing, value-by-tier, tee-wave, boom/bust, edge flags)
that surface non-obvious edges from a single vendor's projection pool."""
from __future__ import annotations

import pandas as pd


def has_real_ceiling(df: pd.DataFrame) -> bool:
    """True only when the vendor shipped a real `ceiling` column (golf: ETR/Ship It;
    MLB: 95th pct). NASCAR (DailyFan) and names-only vendors ship none — we never
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


def chalk_tiers(projections: pd.DataFrame) -> pd.DataFrame:
    """Bin players by ownership tier."""
    df = projections.copy()
    own = df["ownership"].fillna(0)

    def tier(o):
        if o >= 25: return "Mega-chalk (25%+)"
        if o >= 15: return "Chalk (15-25%)"
        if o >= 8:  return "Mid-own (8-15%)"
        if o >= 3:  return "Low-own (3-8%)"
        return "Punt (<3%)"

    df["tier"] = own.apply(tier)
    return df


def chalk_summary(projections: pd.DataFrame) -> pd.DataFrame:
    """Counts and avg proj/salary per tier."""
    df = chalk_tiers(projections)
    grp = df.groupby("tier").agg(
        n=("name", "count"),
        avg_proj=("proj_points", "mean"),
        avg_salary=("salary", "mean"),
        avg_own=("ownership", "mean"),
    ).round(2).reset_index()
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
    df["upside"] = _upside(df)
    sal = df["salary"].replace(0, pd.NA)
    df["ceil_per_1k"] = (df["upside"] / sal * 1000).round(2)
    df["proj_per_1k"] = (df["proj_points"] / sal * 1000).round(2)
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
    proj = df["proj_points"].replace(0, pd.NA)
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
        mis = mispricing_table(df, top_n=3)["underowned"]
        if not mis.empty:
            names = ", ".join(f"{r['name']} (+{int(r['edge'])})" for _, r in mis.iterrows() if r["edge"] > 0)
            if names:
                flags.append(f"**Most underowned vs ceiling** (field blind spots): {names}")
        over = mispricing_table(df, top_n=3)["overowned"]
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
